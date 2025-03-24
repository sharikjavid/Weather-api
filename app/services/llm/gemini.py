import asyncio
import google.generativeai as genai
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

class GeminiClient:
    """Client for accessing Gemini API."""
    
    def __init__(self, api_key: str = settings.GEMINI_API_KEY):
        genai.configure(api_key=api_key)
        
    async def generate_content(self, prompt: str, model: str = "gemini-2.0-flash") -> str:
        """Generate content using Gemini API."""
        try:
            model = genai.GenerativeModel(model)
            response = await asyncio.to_thread(
                model.generate_content,
                prompt
            )
            
            text = response.text
            if asyncio.iscoroutine(text):
                text = await text
            return text.strip()
        except Exception as e:
            logger.error(f"Error generating content with Gemini: {e}", exc_info=True)
            raise