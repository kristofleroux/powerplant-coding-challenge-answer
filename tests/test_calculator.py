from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_production_plan():
    payload = {
        "load": 480,
        "fuels": {
            "gas(euro/MWh)": 13.4,
            "kerosine(euro/MWh)": 50.8,
            "co2(euro/ton)": 20,
            "wind(%)": 60
        },
        "powerplants": [
            {"name": "gasfiredbig1", "type": "gasfired", "efficiency": 0.53, "pmax": 460, "pmin": 100},
            {"name": "turbinebig1", "type": "turbojet", "efficiency": 0.3, "pmax": 400},
            {"name": "windpark1", "type": "windturbine", "efficiency": 1.0, "pmax": 150}
        ]
    }

    response = client.post("/productionplan", json=payload)
    assert response.status_code == 200

    data = response.json()
    total_production = sum(item['p'] for item in data)
    assert total_production == payload['load']


def test_complex_production_plan():
    payload = {
        "load": 910,
        "fuels":
        {
            "gas(euro/MWh)": 13.4,
            "kerosine(euro/MWh)": 50.8,
            "co2(euro/ton)": 20,
            "wind(%)": 60
        },
        "powerplants": [
            {
            "name": "gasfiredbig1",
            "type": "gasfired",
            "efficiency": 0.53,
            "pmin": 100,
            "pmax": 460
            },
            {
            "name": "gasfiredbig2",
            "type": "gasfired",
            "efficiency": 0.53,
            "pmin": 100,
            "pmax": 460
            },
            {
            "name": "gasfiredsomewhatsmaller",
            "type": "gasfired",
            "efficiency": 0.37,
            "pmin": 40,
            "pmax": 210
            },
            {
            "name": "tj1",
            "type": "turbojet",
            "efficiency": 0.3,
            "pmin": 0,
            "pmax": 16
            },
            {
            "name": "windpark1",
            "type": "windturbine",
            "efficiency": 1,
            "pmin": 0,
            "pmax": 150
            },
            {
            "name": "windpark2",
            "type": "windturbine",
            "efficiency": 1,
            "pmin": 0,
            "pmax": 36
            }
        ]
    }

    response = client.post("/productionplan", json=payload)
    assert response.status_code == 200

    data = response.json()
    total_production = sum(item['p'] for item in data)
    assert total_production == payload['load']

def test_invalid_payload():
    payload = {} 
    response = client.post("/productionplan", json=payload)
    assert response.status_code == 422
