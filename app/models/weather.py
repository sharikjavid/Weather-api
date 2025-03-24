from pydantic import BaseModel, Field

class WeatherResponse(BaseModel):
    temperature: float = Field(..., description="Current temperature")
    unit: str = Field("°C", description="Temperature unit (Celsius)")
    report: str = Field(..., description="Human-readable weather report")