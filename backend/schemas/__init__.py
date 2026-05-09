"""Pydantic schemas for request/response validation.

The schemas are split into *request* and *response* models to keep the
API contracts explicit.  They are intentionally lightweight – you can
extend them with additional fields as the application grows.
"""

from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


# ---------- Device schemas ----------
class DeviceBase(BaseModel):
    name: str = Field(..., example="Irrigation Pump 1")
    type: str = Field(..., example="irrigation_pump")
    location: Optional[str] = Field(None, example="Field A, Row 3")
    active: Optional[bool] = Field(True, example=True)


class DeviceCreate(DeviceBase):
    pass


class Device(DeviceBase):
    id: int

    class Config:
        orm_mode = True


# ---------- Sensor data schemas ----------
class SensorDataBase(BaseModel):
    value: float = Field(..., example=23.5)
    unit: Optional[str] = Field("C", example="C")


class SensorDataCreate(SensorDataBase):
    timestamp: Optional[datetime] = Field(None, example="2024-01-01T12:00:00Z")


class SensorData(SensorDataBase):
    device_id: int
    timestamp: datetime

    class Config:
        orm_mode = True


# ---------- Control command schemas ----------
class ControlCommandBase(BaseModel):
    command: str = Field(..., example="start")
    payload: Optional[str] = Field(None, example="{"\"duration\": 30}")


class ControlCommandCreate(ControlCommandBase):
    device_id: int


class ControlCommand(ControlCommandBase):
    id: int
    device_id: int
    timestamp: datetime

    class Config:
        orm_mode = True


# ---------- List responses ----------
class SensorDataList(BaseModel):
    data: List[SensorData]

class DeviceList(BaseModel):
    devices: List[Device]

# ---------- Token usage placeholder ----------
class TokenUsage(BaseModel):
    input_tokens: int
    output_tokens: int
    total_tokens: int

    class Config:
        orm_mode = True
