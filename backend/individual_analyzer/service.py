import uuid
import logging
from typing import List
from llm import execute_prompt_with_pydantic
from .prompts import THEME_EXTRACTION_PROMPT, SUBTOPIC_EXTRACTION_PROMPT, INSIGHT_EXTRACTION_PROMPT
from .schemas import (
    Theme, Subtopic, CreatorInsight, VideoAnalysis,
    ThemeExtractionResponse, SubtopicExtractionResponse, InsightExtractionResponse
)
from datetime import datetime

# Set up logging to file and console
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[
        logging.FileHandler('analysis.log', mode='a'),
        logging.StreamHandler()
    ]
)

class IndividualVideoAnalyser:
    def __init__(self, api_key: str = None, endpoint: str = None):
        self.api_key = api_key
        self.endpoint = endpoint

    def extract_themes(self, transcript: str, video_id: str) -> List[Theme]:
        logging.info("Starting theme extraction...")
        themes = []
        try:
            result = execute_prompt_with_pydantic(
                template=THEME_EXTRACTION_PROMPT,
                data={"transcript": transcript},
                pydantic_model=ThemeExtractionResponse
            )
            for theme_item in result.themes:
                try:
                    theme_id = str(uuid.uuid4())
                    theme = Theme(
                        id=theme_id,
                        video_id=video_id,
                        name=theme_item.name,
                        description=theme_item.description,
                        confidence=theme_item.confidence
                    )
                    themes.append(theme)
                except Exception as e:
                    logging.error(f"Error creating Theme object: {e}")
        except Exception as e:
            logging.error(f"Error extracting themes: {e}")
        logging.info(f"Theme extraction complete. Extracted {len(themes)} themes.")
        return themes

    def extract_subtopics(self, theme: Theme, context: str, video_id: str) -> List[Subtopic]:
        logging.info(f"Extracting subtopics for theme '{theme.name}'...")
        subtopics = []
        try:
            result = execute_prompt_with_pydantic(
                template=SUBTOPIC_EXTRACTION_PROMPT,
                data={
                    "theme_name": theme.name,
                    "theme_description": theme.description,
                    "context": context
                },
                pydantic_model=SubtopicExtractionResponse
            )
            for subtopic_item in result.subtopics:
                try:
                    subtopic_id = str(uuid.uuid4())
                    subtopic = Subtopic(
                        id=subtopic_id,
                        video_id=video_id,
                        name=subtopic_item.name,
                        explanation=subtopic_item.explanation,
                        parent_theme_id=theme.id
                    )
                    subtopics.append(subtopic)
                except Exception as e:
                    logging.error(f"Error creating Subtopic object for theme '{theme.name}': {e}")
        except Exception as e:
            logging.error(f"Error extracting subtopics for theme '{theme.name}': {e}")
        logging.info(f"Subtopic extraction complete for theme '{theme.name}'. Extracted {len(subtopics)} subtopics.")
        return subtopics

    def extract_insights(self, transcript: str, subtopics: List[Subtopic], video_id: str) -> List[CreatorInsight]:
        logging.info("Starting insight extraction...")
        insights = []
        try:
            subtopic_list = "\n".join(f"- {s.name}" for s in subtopics)
            result = execute_prompt_with_pydantic(
                template=INSIGHT_EXTRACTION_PROMPT,
                data={
                    "transcript": transcript,
                    "subtopic_list": subtopic_list
                },
                pydantic_model=InsightExtractionResponse
            )
            subtopic_name_to_id = {s.name: s.id for s in subtopics}
            for insight_item in result.insights:
                try:
                    insight_id = str(uuid.uuid4())
                    related_subtopic_name = insight_item.related_subtopic_name
                    if related_subtopic_name not in subtopic_name_to_id:
                        logging.warning(f"LLM returned unknown subtopic name: {related_subtopic_name}")
                        continue
                    related_subtopic_id = subtopic_name_to_id[related_subtopic_name]
                    insight = CreatorInsight(
                        id=insight_id,
                        video_id=video_id,
                        content=insight_item.content,
                        related_subtopic_id=related_subtopic_id,
                        insight_type=insight_item.type,
                        value=insight_item.value
                    )
                    insights.append(insight)
                except Exception as e:
                    logging.error(f"Error creating CreatorInsight object: {e}")
        except Exception as e:
            logging.error(f"Error extracting insights: {e}")
        logging.info(f"Insight extraction complete. Extracted {len(insights)} insights.")
        return insights

    def analyze_video(self, video_id: str, transcript: str) -> VideoAnalysis:
        logging.info(f"Starting full analysis for video {video_id}...")
        themes = self.extract_themes(transcript, video_id)
        all_subtopics = []
        for theme in themes:
            subtopics = self.extract_subtopics(theme, transcript, video_id)
            all_subtopics.extend(subtopics)
        insights = self.extract_insights(transcript, all_subtopics, video_id)
        logging.info(f"Analysis complete for video {video_id}.")
        return VideoAnalysis(
            video_id=video_id,
            themes=themes,
            subtopics=all_subtopics,
            creator_insights=insights,
            extracted_at=datetime.utcnow().isoformat()
        ) 