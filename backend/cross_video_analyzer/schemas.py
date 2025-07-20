from pydantic import BaseModel
from typing import List, Optional

class SharedTheme(BaseModel):
    id: str
    name: str
    participating_video_ids: List[str]
    consensus_level: float  # 0-1

class Contrast(BaseModel):
    id: str
    subtopic_id: str
    summary: str
    insight_ids: List[str]
    video_ids: List[str]
    contrast_type: str

class ConceptOverlap(BaseModel):
    id: str
    primary_concept: str
    primary_type: str  # 'theme' or 'subtopic'
    overlapping_concepts: List[str]
    overlapping_types: List[str]  # List of 'theme' or 'subtopic' for each
    should_merge: bool
    semantic_similarity: float  # 0-1

class AnalysisMetadata(BaseModel):
    video_ids: List[str]
    generated_at: str

class CrossVideoAnalysis(BaseModel):
    shared_themes: List[SharedTheme]
    contrasts: List[Contrast]
    concept_overlaps: List[ConceptOverlap]
    analysis_metadata: AnalysisMetadata 

class ContrastResponse(BaseModel):
    contrasts: List[Contrast]

class ConceptOverlapResponse(BaseModel):
    overlaps: List[ConceptOverlap] 