"""Router for sensor data endpoints."""

from fastapi import APIRouter, HTTPException
from typing import List

from ..models import SensorData
from ..crud import sensor_crud

router = APIRouter()

@router.post("/", response_model=SensorData)
async def create_sensor_data(data: SensorData):
    return await sensor_crud.create(data)

@router.get("/", response_model=List[SensorData])
async def read_sensor_data(limit: int = 100):
    return await sensor_crud.list(limit)
