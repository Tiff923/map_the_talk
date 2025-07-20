import unittest
from unittest.mock import patch
from transcript_extractor import service
from transcript_extractor.schemas import TranscriptResponse, TranscriptSegment
from transcript_extractor.exceptions import TranscriptNotFoundException

class TestTranscriptService(unittest.TestCase):
    @patch('transcript_extractor.service.fetch_transcript')
    def test_get_transcript_success(self, mock_fetch):
        # Mock transcript data as returned by youtube-transcript-api
        mock_fetch.return_value = [
            {"start": 0.0, "duration": 5.0, "text": "Hello world."},
            {"start": 5.0, "duration": 4.0, "text": "This is a test."}
        ]
        video_id = "dummy_id"
        result = service.get_transcript(video_id)
        self.assertIsInstance(result, TranscriptResponse)
        self.assertEqual(result.video_id, video_id)
        self.assertEqual(len(result.segments), 2)
        self.assertEqual(result.segments[0].text, "Hello world.")

    @patch('transcript_extractor.service.fetch_transcript')
    def test_get_transcript_not_found(self, mock_fetch):
        mock_fetch.return_value = None
        with self.assertRaises(TranscriptNotFoundException):
            service.get_transcript("invalid_id")

if __name__ == '__main__':
    unittest.main() 