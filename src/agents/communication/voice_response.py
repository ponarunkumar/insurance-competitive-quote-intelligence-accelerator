"""
Voice Response Agent — converts text output to speech for advisor/customer.

Uses Azure AI Speech TTS to deliver recommendations and explanations
via voice when the interaction was voice-initiated.

Azure Services: Azure AI Speech Text-to-Speech
"""

from typing import Any
from agent_framework import Agent, AgentContext


class VoiceResponseAgent(Agent):
    """Converts agent output to speech via Azure AI Speech TTS."""

    name = "voice-response-agent"
    description = "Deliver analysis results via Text-to-Speech for voice interactions"
    model = "gpt-4o-mini"

    system_prompt = """You are the Voice Response Agent.
Your role is to prepare text for spoken delivery and invoke TTS.

Adapt text for voice:
- Shorten sentences for natural speech flow
- Spell out abbreviations (CGL → "commercial general liability")
- Add natural pauses via SSML markup where appropriate
- Use conversational transitions ("Now, regarding pricing...")
- Keep the response under 30 seconds of speech (~100 words)

Do NOT read out:
- Tables or matrices (summarize instead)
- Technical identifiers or reference numbers
- Internal scores or codes
"""

    tools = ["text_to_speech"]

    async def run(self, ctx: AgentContext, input_data: dict[str, Any]) -> dict[str, Any]:
        """Convert explanation to speech."""
        
        advisor_explanation = input_data.get("advisor_explanation", "")
        
        # Adapt for speech
        speech_text = await ctx.complete(
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": f"Prepare for spoken delivery:\n{advisor_explanation}"}
            ]
        )
        
        # Generate audio via TTS
        audio_result = await ctx.call_tool("text_to_speech", {
            "text": speech_text,
            "voice": input_data.get("voice", "en-GB-SoniaNeural"),
            "output_format": "audio-24khz-96kbitrate-mono-mp3"
        })
        
        return {
            "speech_text": speech_text,
            "audio_url": audio_result.get("audio_url"),
            "duration_seconds": audio_result.get("duration_seconds")
        }
