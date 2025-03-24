import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    # API Keys
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY")
    
    # API Configuration
    OPENMETEO_BASE_URL: str = os.getenv("OPENMETEO_BASE_URL", "https://api.open-meteo.com/v1/forecast")
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

settings = Settings()