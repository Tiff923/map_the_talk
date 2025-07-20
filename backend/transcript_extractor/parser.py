from .schemas import TranscriptSegment, TranscriptResponse
from typing import List, Dict, Any

def parse_transcript(raw_transcript: List[Dict[str, Any]], video_id: str = None, language: str = "en", transcript_type: str = "auto-generated"):
    # Convert the list of dicts into TranscriptSegment objects
    segments = [
        TranscriptSegment(
            start=segment.get("start", 0.0),
            duration=segment.get("duration", 0.0),
            text=segment.get("text", "")
        )
        for segment in raw_transcript
    ]
    return TranscriptResponse(
        video_id=video_id or "",
        language=language,
        type=transcript_type,
        segments=segments,
        metadata={}
    ) 