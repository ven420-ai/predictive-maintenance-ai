from fastapi.testclient import TestClient
from src.api import app

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Predictive Maintenance AI API is running"


def test_predict():
    response = client.post(
        "/predict",
        params={
            "temperature": 92,
            "vibration": 8.5,
            "pressure": 88,
            "voltage": 2.9,
            "operating_hours": 8500
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "prediction" in data
    assert "failure_probability" in data