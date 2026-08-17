"""
Speech and voice-related data models for the contact center integration.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class TranscriptionSegment(BaseModel):
    """A single segment of a transcription with speaker and timing."""
    speaker: str = Field(description="Speaker label (advisor, customer, unknown)")
    text: str
    start_time_seconds: float
    end_time_seconds: float
    confidence: float
    language: str = "en-GB"


class TranscriptionResult(BaseModel):
    """Full transcription output from Speech-to-Text."""
    call_id: str
    full_text: str
    segments: list[TranscriptionSegment]
    speakers_detected: int
    primary_language: str
    duration_seconds: float
    custom_model_used: bool = False
    transcription_timestamp: datetime = Field(default_factory=datetime.utcnow)


class TTSRequest(BaseModel):
    """Text-to-Speech synthesis request."""
    text: str
    voice: str = "en-GB-SoniaNeural"
    output_format: str = "audio-24khz-96kbitrate-mono-mp3"
    speaking_rate: float = Field(default=1.0, ge=0.5, le=2.0)
    pitch: float = Field(default=0, ge=-50, le=50)


class TTSResult(BaseModel):
    """Text-to-Speech synthesis output."""
    audio_url: str
    duration_seconds: float
    characters_processed: int
    voice_used: str


class TranslationResult(BaseModel):
    """Translation output."""
    source_text: str
    translated_text: str
    source_language: str
    target_language: str
    confidence: float


class CallRecord(BaseModel):
    """Contact center call record."""
    call_id: str
    advisor_id: str
    customer_id: Optional[str] = None
    start_time: datetime
    end_time: Optional[datetime] = None
    duration_seconds: Optional[float] = None
    recording_url: Optional[str] = None
    transcription: Optional[TranscriptionResult] = None
    disposition: Optional[str] = None
    product_discussed: Optional[str] = None
    outcome: Optional[str] = None
