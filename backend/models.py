"""Data models for SmartFarm Manager backend."""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class SensorData(BaseModel):
    sensor_id: str
    temperature: float
    humidity: float
    co2: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class Crop(BaseModel):
    id: int
    name: str
    species: str
    planting_date: datetime
    expected_harvest: datetime

class ControlCommand(BaseModel):
    device_id: str
    command: str
    value: Optional[float] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
