
from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from application.calculator import calculate_production_plan


app = FastAPI()

class PowerPlant(BaseModel):
    name: str
    type: str
    efficiency: float
    pmax: float
    pmin: float = 0

class Fuels(BaseModel):
    gas_euro_per_mwh: float = Field(..., alias='gas(euro/MWh)')
    kerosine_euro_per_mwh: float = Field(..., alias='kerosine(euro/MWh)')
    co2_euro_per_ton: float = Field(..., alias='co2(euro/ton)')
    wind_percentage: float = Field(..., alias='wind(%)')

class Payload(BaseModel):
    load: float
    fuels: Fuels
    powerplants: List[PowerPlant]


@app.post("/productionplan")
async def production_plan(payload: Payload):
    try:
        result = calculate_production_plan(payload.load, payload.fuels.dict(), [plant.dict() for plant in payload.powerplants])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    return result