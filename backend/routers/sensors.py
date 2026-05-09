"""Sensor router – ingestion and retrieval.

Endpoints:
- POST /sensors/{device_id}/ingest – ingest a single sensor reading.
- GET /sensors/{device_id} – retrieve readings for a device, optionally
  filtered by start/end timestamps.
"""

from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, HTTPException, Query, status

from ..crud import ingest_sensor_data, get_sensor_data
from ..schemas import SensorDataCreate, SensorData as SensorDataSchema

router = APIRouter()


@router.post("/{device_id}/ingest", response_model=SensorDataSchema, status_code=status.HTTP_201_CREATED)
async def ingest_sensor_endpoint(device_id: int, data_in: SensorDataCreate) -> SensorDataSchema:
    try:
        return await ingest_sensor_data(device_id, data_in)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{device_id}", response_model=List[SensorDataSchema])
async def get_sensor_data_endpoint(
    device_id: int,
    start: Optional[datetime] = Query(None, description="ISO‑8601 start time"),
    end: Optional[datetime] = Query(None, description="ISO‑8601 end time"),
) -> List[SensorDataSchema]:
    try:
        return await get_sensor_data(device_id, start, end)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


__all__ = ["router"]
