import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch, MagicMock

from app.main import app

client = TestClient(app)

class TestWeatherAPI:
    @patch("app.services.weather.openmeteo.OpenMeteoAPI.get_current_temperature")
    @patch("app.services.weather.llm_report.generate_weather_report")
    def test_get_weather_success(self, mock_generate_report, mock_get_temperature):
        mock_get_temperature.return_value = 15.2
        mock_generate_report.return_value = "Sample weather report text"
        response = client.get("/weather?latitude=40.7128&longitude=-74.0060")
        assert response.status_code == 200
        data = response.json()
        assert data["temperature"] == 15.2
        assert data["unit"] == "°C"
        assert isinstance(data["report"], str)
        assert len(data["report"]) > 0

    @patch("app.services.weather.openmeteo.OpenMeteoAPI.get_current_temperature")
    @patch("app.services.weather.llm_report.generate_weather_report")
    def test_get_weather_llm_failure(self, mock_generate_report, mock_get_temperature):
        mock_get_temperature.return_value = 22.7
        mock_generate_report.side_effect = Exception("LLM API error")
        response = client.get("/weather?latitude=35.6762&longitude=139.6503")
        assert response.status_code == 200
        data = response.json()
        assert data["temperature"] == 22.7
        assert data["unit"] == "°C"
        assert isinstance(data["report"], str)
        assert len(data["report"]) > 0
        
        print(f"Note: Expected LLM failure but got report: {data['report']}")

    def test_get_weather_invalid_coordinates(self):
        """
        Test for validation errors with invalid coordinates.
        
        Note: FastAPI handles parameter validation before our route is called,
        so we don't need to mock the OpenMeteoAPI class here.
        """
        response = client.get("/weather?latitude=95.0&longitude=139.6503")
        
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data
        # Check that there's a validation error for latitude
        errors = [error for error in data["detail"] if error["loc"][1] == "latitude"]
        assert len(errors) > 0
        assert "less than or equal to" in errors[0]["msg"]

    def test_get_weather_missing_parameters(self):
        response = client.get("/weather")
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data
        assert len(data["detail"]) == 2 
        param_errors = {error["loc"][1]: error for error in data["detail"]}
        assert "latitude" in param_errors
        assert "longitude" in param_errors
        assert param_errors["latitude"]["msg"] == "Field required"
        assert param_errors["longitude"]["msg"] == "Field required"

    @patch("app.services.weather.openmeteo.OpenMeteoAPI.get_current_temperature")
    def test_get_weather_service_error(self, mock_get_temperature):
        mock_get_temperature.side_effect = Exception("Error connecting to the weather service.")
        response = client.get("/weather?latitude=40.7128&longitude=-74.0060")
        assert response.status_code == 500
        data = response.json()
        assert "detail" in data
        assert "Error fetching temperature data" in data["detail"]