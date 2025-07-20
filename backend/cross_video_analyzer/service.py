import logging
import uuid
from typing import List, Dict
from llm import execute_prompt_with_pydantic
from individual_analyzer.schemas import VideoAnalysis, Theme
from .schemas import SharedTheme, Contrast, ConceptOverlap, CrossVideoAnalysis, AnalysisMetadata
from datetime import datetime
from collections import defaultdict
from .prompts import CONTRAST_IDENTIFICATION_PROMPT
import json

logging.basicConfig(level=logging.INFO)

class CrossVideoAnalyzer:
    def analyze_shared_themes(self, analyses: List[VideoAnalysis]) -> List[SharedTheme]:
        """
        Analyze and return shared themes across multiple VideoAnalysis objects.
        Group themes by name (case-insensitive), aggregate participating video_ids, and compute consensus_level.
        """
        logging.info("Analyzing shared themes across videos...")
        theme_groups: Dict[str, Dict] = defaultdict(lambda: {"name": None, "video_ids": set()})
        total_videos = len(analyses)
        for analysis in analyses:
            for theme in analysis.themes:
                key = theme.name.strip().lower()
                if theme_groups[key]["name"] is None:
                    theme_groups[key]["name"] = theme.name.strip()
                theme_groups[key]["video_ids"].add(analysis.video_id)
        shared_themes = []
        for key, group in theme_groups.items():
            try:
                consensus_level = len(group["video_ids"]) / total_videos if total_videos > 0 else 0.0
                shared_theme = SharedTheme(
                    id=str(uuid.uuid4()),
                    name=group["name"],
                    participating_video_ids=list(group["video_ids"]),
                    consensus_level=consensus_level
                )
                shared_themes.append(shared_theme)
            except Exception as e:
                logging.error(f"Error creating SharedTheme for group '{key}': {e}")
        logging.info(f"Shared theme analysis complete. Found {len(shared_themes)} shared themes.")
        return shared_themes

    def identify_contrasts(self, analyses: List[VideoAnalysis]) -> List[Contrast]:
        """
        Use LLM to identify contrasts (opposing insights) across multiple VideoAnalysis objects.
        For each subtopic, gather all related insights and prompt the LLM to find contrasts.
        Maps LLM output fields (summary, insight_ids, video_ids, contrast_type) into the Contrast schema:
        - id: generated here
        - subtopic_id: generated here (from subtopic_key)
        - summary, insight_ids, video_ids, contrast_type: from LLM
        """
        from .schemas import ContrastResponse, Contrast
        logging.info("Identifying contrasts across videos using LLM...")
        subtopic_insights = defaultdict(list)  # key: subtopic name (lower), value: list of (CreatorInsight, video_id)
        for analysis in analyses:
            for subtopic in getattr(analysis, 'subtopics', []):
                for insight in getattr(subtopic, 'insights', []):
                    subtopic_key = subtopic.name.strip().lower()
                    subtopic_insights[subtopic_key].append({
                        "insight_id": insight.id,
                        "content": insight.content,
                        "video_id": analysis.video_id
                    })
        contrasts = []
        for subtopic_key, insights_list in subtopic_insights.items():
            if len(insights_list) < 2:
                continue  # No contrast possible
            try:
                llm_response = execute_prompt_with_pydantic(
                    template=CONTRAST_IDENTIFICATION_PROMPT,
                    data={
                        "subtopic_name": subtopic_key,
                        "insights_json": json.dumps(insights_list, ensure_ascii=False)
                    },
                    pydantic_model=ContrastResponse
                )
                for contrast_obj in llm_response.contrasts:
                    try:
                        contrast = Contrast(
                            id=str(uuid.uuid4()),
                            subtopic_id=subtopic_key,
                            summary=contrast_obj.summary,
                            insight_ids=contrast_obj.insight_ids,
                            video_ids=contrast_obj.video_ids,
                            contrast_type=contrast_obj.contrast_type
                        )
                        contrasts.append(contrast)
                    except Exception as e:
                        logging.error(f"Error mapping LLM contrast result for subtopic '{subtopic_key}': {e}")
            except Exception as e:
                logging.error(f"LLM call failed for subtopic '{subtopic_key}': {e}")
        logging.info(f"Contrast analysis complete. Found {len(contrasts)} contrasts.")
        return contrasts

    def find_conceptual_overlaps(self, analyses: List[VideoAnalysis]) -> List[ConceptOverlap]:
        """
        Use LLM to find conceptual overlaps (semantically similar or related concepts) across videos.
        Gathers all themes and subtopics, prompts the LLM, and parses the result into ConceptOverlap objects.
        """
        from .schemas import ConceptOverlapResponse
        from .prompts import CONCEPTUAL_OVERLAP_PROMPT
        import json
        logging.info("Finding conceptual overlaps across videos using LLM...")
        concepts = []
        for analysis in analyses:
            for theme in getattr(analysis, 'themes', []):
                concepts.append({
                    "name": theme.name,
                    "type": "theme",
                    "video_id": analysis.video_id
                })
            for subtopic in getattr(analysis, 'subtopics', []):
                concepts.append({
                    "name": subtopic.name,
                    "type": "subtopic",
                    "video_id": analysis.video_id
                })
        if len(concepts) < 2:
            return []
        overlaps = []
        try:
            llm_response = execute_prompt_with_pydantic(
                template=CONCEPTUAL_OVERLAP_PROMPT,
                data={"concepts_json": json.dumps(concepts, ensure_ascii=False)},
                pydantic_model=ConceptOverlapResponse
            )
            for overlap in llm_response.overlaps:
                try:
                    if not isinstance(overlap, ConceptOverlap):
                        overlap = ConceptOverlap(**overlap)
                    overlaps.append(overlap)
                except Exception as e:
                    logging.error(f"Error parsing LLM overlap result: {e}")
        except Exception as e:
            logging.error(f"LLM call failed for conceptual overlap: {e}")
        logging.info(f"Conceptual overlap analysis complete. Found {len(overlaps)} overlaps.")
        return overlaps

    def perform_cross_analysis(self, analyses: List[VideoAnalysis]) -> CrossVideoAnalysis:
        """
        Orchestrate cross-video analysis and return a CrossVideoAnalysis object.
        """
        logging.info("Performing full cross-video analysis...")
        shared_themes = self.analyze_shared_themes(analyses)
        contrasts = self.identify_contrasts(analyses)
        concept_overlaps = self.find_conceptual_overlaps(analyses)
        metadata = AnalysisMetadata(
            video_ids=[a.video_id for a in analyses],
            generated_at=datetime.utcnow().isoformat()
        )
        return CrossVideoAnalysis(
            shared_themes=shared_themes,
            contrasts=contrasts,
            concept_overlaps=concept_overlaps,
            analysis_metadata=metadata
        ) 