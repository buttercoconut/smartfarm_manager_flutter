"""CRUD operations for sensor data (in‑memory for demo)."""

from typing import List
from ..models import SensorData

_sensor_db: List[SensorData] = []

async def create(data: SensorData) -> SensorData:
    _sensor_db.append(data)
    return data

async def list(limit: int = 100) -> List[SensorData]:
    return _sensor_db[-limit:]
