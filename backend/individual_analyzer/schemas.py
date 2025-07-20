from pydantic import BaseModel
from typing import List

# Pydantic models for LLM structured output
class ThemeItem(BaseModel):
    name: str
    description: str
    confidence: float

class ThemeExtractionResponse(BaseModel):
    themes: List[ThemeItem]

class SubtopicItem(BaseModel):
    name: str
    explanation: str
    relation_to_theme: str

class SubtopicExtractionResponse(BaseModel):
    subtopics: List[SubtopicItem]

class InsightItem(BaseModel):
    content: str
    value: str
    type: str
    related_subtopic_name: str

class InsightExtractionResponse(BaseModel):
    insights: List[InsightItem]

# Existing models for normalized output
class Theme(BaseModel):
    id: str
    video_id: str
    name: str
    description: str
    confidence: float

class Subtopic(BaseModel):
    id: str
    video_id: str
    name: str
    explanation: str
    parent_theme_id: str

class CreatorInsight(BaseModel):
    id: str
    video_id: str
    content: str
    related_subtopic_id: str
    insight_type: str
    value: str

class VideoAnalysis(BaseModel):
    video_id: str
    themes: List[Theme]
    subtopics: List[Subtopic]
    creator_insights: List[CreatorInsight]
    extracted_at: str 