from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound, VideoUnavailable


def fetch_transcript(video_id: str):
    try:
        # Try to fetch the transcript (official or auto-generated)
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        # transcript is a list of dicts: [{"text": ..., "start": ..., "duration": ...}, ...]
        return transcript
    except (TranscriptsDisabled, NoTranscriptFound, VideoUnavailable):
        return None
    except Exception as e:
        # Log or handle unexpected errors as needed
        return None 