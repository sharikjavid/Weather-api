import pytest
import asyncio
from app.services.weather.openmeteo import OpenMeteoAPI
from app.services.llm.gemini import GeminiClient

@pytest.fixture
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
async def openmeteo_api():
    """Create a test instance of OpenMeteoAPI."""
    return OpenMeteoAPI()

@pytest.fixture
async def gemini_client():
    """Create a test instance of GeminiClient with a mock API key."""
    return GeminiClient(api_key="test_api_key")