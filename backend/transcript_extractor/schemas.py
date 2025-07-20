from pydantic import BaseModel
from typing import List, Dict, Any

class TranscriptSegment(BaseModel):
    start: float
    duration: float
    text: str

class TranscriptResponse(BaseModel):
    video_id: str
    language: str
    type: str  # 'official' or 'auto-generated'
    segments: List[TranscriptSegment]
    metadata: Dict[str, Any] = {} 