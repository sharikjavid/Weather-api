import httpx
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

class OpenMeteoAPI:
    """A wrapper class for the Open-Meteo API."""
    
    def __init__(self, base_url: str = settings.OPENMETEO_BASE_URL):
        self.base_url = base_url
        
    async def get_current_temperature(self, latitude: float, longitude: float) -> float:
        """
        Get the current temperature for the specified coordinates.
        """
        if not (-90 <= latitude <= 90):
            raise ValueError("Latitude must be between -90 and 90.")
        if not (-180 <= longitude <= 180):
            raise ValueError("Longitude must be between -180 and 180.")
        
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current_weather": "true"
        }
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(self.base_url, params=params)
                response.raise_for_status()
                data = response.json()
        except httpx.RequestError as e:
            logger.error("Error connecting to the weather service.", exc_info=True)
            raise Exception("Error connecting to the weather service.") from e
        except httpx.HTTPStatusError as e:
            logger.error("HTTP error occurred.", exc_info=True)
            raise Exception(f"Received HTTP error: {e.response.status_code}.") from e

        if "current_weather" not in data or "temperature" not in data["current_weather"]:
            logger.error("Temperature data not available in API response: %s", data)
            raise Exception("Temperature data not available in the API response.")
            
        return data["current_weather"]["temperature"]