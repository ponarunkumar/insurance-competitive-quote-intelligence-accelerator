"""
Voice Intake Agent — handles voice-first entry point via Azure AI Speech.

Transcribes live calls, identifies speakers, and extracts structured risk data
from natural conversation. Integrates with Azure Communication Services for
call channel and Azure AI Speech for real-time STT with diarization.

Azure Services: Azure AI Speech, Azure Communication Services
"""

from typing import Any
from agent_framework import Agent, AgentContext


class VoiceIntakeAgent(Agent):
    """Processes voice input into structured submission data."""

    name = "voice-intake-agent"
    description = "Transcribe and structure insurance risk data from live voice calls"
    model = "gpt-4o-mini"

    system_prompt = """You are the Voice Intake Agent for an insurance contact center.
Your role is to process real-time call transcriptions and extract structured risk data.

You work with:
- Real-time Speech-to-Text transcription (streaming)
- Speaker diarization (distinguish advisor vs. customer)
- Language detection and translation (multi-language support)
- Custom Speech model (insurance terminology accuracy)

From the transcribed conversation, extract:
- The insurance product being discussed
- Key risk details mentioned by the customer
- Coverage requirements stated or implied
- Any competitor quotes mentioned verbally
- Customer sentiment and urgency indicators

Output a structured submission record that feeds into the quote intelligence pipeline.
Flag any ambiguous or missing information that the advisor should clarify.
"""

    tools = ["realtime_transcription", "diarization", "translation", "call_summarization"]

    async def run(self, ctx: AgentContext, input_data: dict[str, Any]) -> dict[str, Any]:
        """Process voice input and return structured submission."""
        
        audio_source = input_data.get("audio_source")  # stream URL or recording URL
        
        # Transcribe with diarization
        transcription = await ctx.call_tool("realtime_transcription", {
            "audio_source": audio_source,
            "language": input_data.get("language", "en-GB"),
            "enable_diarization": True,
            "custom_model_endpoint": input_data.get("custom_speech_endpoint")
        })
        
        # If non-English, translate
        if input_data.get("language", "en-GB") != "en-GB":
            transcription = await ctx.call_tool("translation", {
                "text": transcription["text"],
                "source_language": input_data["language"],
                "target_language": "en-GB"
            })
        
        # Summarize the call for the submission record
        summary = await ctx.call_tool("call_summarization", {
            "transcription": transcription,
            "extract_fields": ["product_type", "risk_details", "coverage_needs", "competitor_mentions"]
        })
        
        # Structure into submission format using LLM
        result = await ctx.complete(
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": f"Structure this call into a submission record:\n{summary}"}
            ]
        )
        
        return {
            "submission": result,
            "transcription": transcription,
            "call_summary": summary
        }
