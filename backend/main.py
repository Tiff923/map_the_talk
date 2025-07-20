from fastapi import FastAPI, HTTPException, Body
from transcript_extractor.service import get_transcript
from transcript_extractor.schemas import TranscriptResponse
from transcript_extractor.exceptions import TranscriptNotFoundException
from individual_analyzer.service import IndividualVideoAnalyser
from individual_analyzer.schemas import VideoAnalysis
from cross_video_analyzer.service import CrossVideoAnalyzer
from cross_video_analyzer.schemas import CrossVideoAnalysis
from typing import List
import logging

app = FastAPI()

@app.get("/transcript/{video_id}", response_model=TranscriptResponse)
def fetch_transcript_endpoint(video_id: str):
    try:
        transcript = get_transcript(video_id)
        return transcript
    except TranscriptNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.post("/analyze/{video_id}", response_model=VideoAnalysis)
def analyze_video_endpoint(video_id: str):
    try:
        transcript_response = get_transcript(video_id)
        transcript_text = " ".join([seg.text for seg in transcript_response.segments])
        analyzer = IndividualVideoAnalyser()
        analysis = analyzer.analyze_video(video_id, transcript_text)
        return analysis
    except TranscriptNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/cross-analyze", response_model=CrossVideoAnalysis)
def cross_video_analyze_endpoint(video_ids: List[str] = Body(..., embed=True)):
    try:
        analyzer = IndividualVideoAnalyser()
        analyses = []
        for video_id in video_ids:
            try:
                transcript_response = get_transcript(video_id)
                transcript_text = " ".join([seg.text for seg in transcript_response.segments])
                analysis = analyzer.analyze_video(video_id, transcript_text)
                analyses.append(analysis)
            except Exception as e:
                # Log and skip videos that fail
                logging.error(f"Failed to analyze video {video_id}: {e}")
                continue
        if not analyses:
            raise HTTPException(status_code=400, detail="No valid video analyses could be performed.")
        cross_analyzer = CrossVideoAnalyzer()
        cross_analysis = cross_analyzer.perform_cross_analysis(analyses)
        return cross_analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 