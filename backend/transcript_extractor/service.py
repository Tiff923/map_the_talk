from .youtube_api import fetch_transcript
from .parser import parse_transcript
from .exceptions import TranscriptNotFoundException


def get_transcript(video_id: str):
    raw_transcript = fetch_transcript(video_id)
    if not raw_transcript:
        raise TranscriptNotFoundException(f"Transcript not found for video {video_id}")
    # For now, assume language is 'en' and type is 'auto-generated'
    return parse_transcript(raw_transcript, video_id=video_id, language="en", transcript_type="auto-generated") 