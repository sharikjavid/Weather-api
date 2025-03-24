from fastapi import APIRouter, HTTPException, Query
import logging

from app.models.weather import WeatherResponse
from app.services.weather.openmeteo import OpenMeteoAPI
from app.services.weather.llm_report import generate_weather_report

logger = logging.getLogger(__name__)
router = APIRouter()

weather_api = OpenMeteoAPI()

@router.get("/weather", response_model=WeatherResponse)
async def get_weather(
    latitude: float = Query(..., ge=-90.0, le=90.0, description="Latitude between -90 and 90"),
    longitude: float = Query(..., ge=-180.0, le=180.0, description="Longitude between -180 and 180")
):
    """
    Get the current temperature and report for the specified coordinates.

    """
    try:
        temperature = await weather_api.get_current_temperature(latitude, longitude)
    except ValueError as ve:
        logger.warning("Invalid input: %s", ve)
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error("Error fetching temperature: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail="Error fetching temperature data.")
    
    try:
        report = await generate_weather_report(temperature)
    except Exception as e:
        logger.error("LLM generation failed: %s", e, exc_info=True)
        report = "Weather report is not available at the moment."
    
    return WeatherResponse(temperature=temperature, report=report)