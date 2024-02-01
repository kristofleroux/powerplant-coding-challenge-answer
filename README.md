
# FastAPI Powerplant Production Plan API

This project is a FastAPI application designed to calculate the production plan for various power plants based on given load, fuel costs, and power plant specifications.

## Requirements

- Python 3.8+
- FastAPI
- Uvicorn (for running the application locally)
- Docker (optional, for containerized deployment)

## Local Setup and Running

To set up and run the application locally, follow these steps:

1. **Install Dependencies**:
   Make sure you are in the project root directory and run:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8888
   ```
   The API will be available at `http://localhost:8888`.

## Running with Docker

To run the application using Docker, follow these steps:

1. **Build the Docker Image**:
   In the project root directory, run:
   ```bash
   docker build -t ppc:latest .
   ```

2. **Run the Docker Container**:
   ```bash
   docker run -p 8888:8888 -d ppc:latest
   ```
   The application will be available at `http://localhost:8888`.

## API Usage

- **Endpoint**: `/productionplan`
- **Method**: POST
- **Payload**: JSON object containing `load`, `fuels`, and `powerplants` data.

### Sample Payload

```json
{
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
```

## Testing

1. **Install Dependencies**:
   Make sure you are in the project root directory and run:
   ```bash
   pip install -r requirements-dev.txt
   ```
1. **Run the tests**:
   To run the tests, execute the following command in the project root directory:
   ```bash
   pytest
   ```
