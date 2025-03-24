import logging
from app.services.llm.gemini import GeminiClient

logger = logging.getLogger(__name__)
gemini_client = GeminiClient()

async def generate_weather_report(temperature: float) -> str:
    """
    Generate a human-friendly weather report from the current temperature using Gemini.
    """
    prompt = f"Using the current temperature of {temperature}°C, write a concise, professional‑tone weather report. Include key details such as feels‑like temperature, general sky conditions, and a brief recommendation (e.g., dress advice), formatted as a short paragraph.”"
    
    try:
        return await gemini_client.generate_content(prompt)
    except Exception as e:
        logger.error(f"Failed to generate weather report: {e}", exc_info=True)
        return "Weather report is not available at the moment."