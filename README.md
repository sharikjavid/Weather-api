# Weather API with LLM

A FastAPI-based service that provides current weather information along with a human-readable report generated using Google's Gemini LLM.


## Features

- 🌡️ Get current temperature data based on latitude and longitude coordinates
- 💬 Generate natural language weather reports powered by Gemini LLM
- 🔒 Comprehensive error handling and input validation
- 📊 Logging with configurable levels
- 🐳 Docker support for easy deployment

## Tech Stack

- **FastAPI** - Modern, high-performance web framework
- **Google Gemini API** - Advanced LLM for generating human-friendly weather reports
- **Open-Meteo API** - Reliable weather data source
- **Pytest** - Comprehensive test suite
- **Docker** - Containerization for consistent deployment

  ## Project Structure

```
sharikjavid-weather-api/
├── app/
│   ├── api/            # API routes
│   ├── core/           # Core functionality (config, logging)
│   ├── models/         # Pydantic models
│   ├── services/       # External services integration
│   │   ├── llm/        # LLM service integrations
│   │   └── weather/    # Weather service integrations
│   └── main.py         # Application entry point
├── tests/              # Test suite
├── Dockerfile          # Docker configuration
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

## Getting Started

### Prerequisites

- Python 3.11+
- API key for Google Gemini

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/sharikjavid-weather-api.git
   cd sharikjavid-weather-api
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root with the following variables:
   ```
   GEMINI_API_KEY=your_gemini_api_key
   LOG_LEVEL=INFO
   ```

### Running the Application

```bash
uvicorn app.main:app --reload
```

The API will be available at http://127.0.0.1:8000

### Docker Deployment

#### Option 1: Build and Run Locally

1. Build the Docker image:
   ```bash
   docker build -t weather-api .
   ```

2. Run the container:
   ```bash
   docker run -p 8000:8000 -d weather-api
   ```

#### Option 2: Pull from Docker Hub

Pull the pre-built image from Docker Hub:
```bash
docker pull 2424048sha/weather-api
```

Run the container:
```bash
docker run -p 8000:8000 -d 2424048sha/weather-api
```

## Testing

Run the complete test suite with:

```bash
pytest
```

Run specific test cases with verbose output:
```bash
pytest tests/test_api.py -v
```

Example test output:
```
==================== test session starts ====================
platform win32 -- Python 3.12.7, pytest-8.3.5, pluggy-1.5.0
collected 5 items

tests/test_api.py::TestWeatherAPI::test_get_weather_success PASSED [ 20%]
tests/test_api.py::TestWeatherAPI::test_get_weather_llm_failure PASSED [ 40%]
tests/test_api.py::TestWeatherAPI::test_get_weather_invalid_coordinates PASSED [ 60%]
tests/test_api.py::TestWeatherAPI::test_get_weather_missing_parameters PASSED [ 80%]
tests/test_api.py::TestWeatherAPI::test_get_weather_service_error PASSED [100%]

=============== 5 passed in 1.89s ===============
```

## API Documentation

Once the application is running, you can access the automatic API documentation at:
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

### Endpoints

#### GET /weather

Get current weather information and a natural language report.

**Parameters:**
- `latitude` (float, required): Latitude between -90 and 90
- `longitude` (float, required): Longitude between -180 and 180

**Response Example:**
```json
{
  "temperature": 15.2,
  "unit": "°C",
  "report": "The current temperature is 15.2°C, which feels cool and comfortable. Expect partly cloudy skies throughout the day. A light jacket or sweater is recommended for outdoor activities."
}
```



## License

[MIT License](LICENSE)
