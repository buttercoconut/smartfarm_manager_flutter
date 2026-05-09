"""CRUD helper functions.

These functions encapsulate the database logic so that the routers stay
clean.  All functions are async and use the `get_session` context
manager from `database.py`.
"""

from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from sqlalchemy import select, insert, update, delete
from sqlalchemy.exc import NoResultFound

from .database import get_session
from .models import Device, SensorData, ControlCommand
from .schemas import (
    DeviceCreate,
    Device as DeviceSchema,
    SensorDataCreate,
    SensorData as SensorDataSchema,
    ControlCommandCreate,
    ControlCommand as ControlCommandSchema,
)


# ---------- Device CRUD ----------
async def create_device(device_in: DeviceCreate) -> DeviceSchema:
    async with get_session() as session:
        device = Device(**device_in.dict())
        session.add(device)
        await session.commit()
        await session.refresh(device)
        return DeviceSchema.from_orm(device)


async def get_device(device_id: int) -> DeviceSchema:
    async with get_session() as session:
        result = await session.execute(select(Device).where(Device.id == device_id))
        device = result.scalar_one_or_none()
        if not device:
            raise NoResultFound(f"Device {device_id} not found")
        return DeviceSchema.from_orm(device)


async def list_devices() -> List[DeviceSchema]:
    async with get_session() as session:
        result = await session.execute(select(Device))
        devices = result.scalars().all()
        return [DeviceSchema.from_orm(d) for d in devices]


# ---------- Sensor data CRUD ----------
async def ingest_sensor_data(device_id: int, data_in: SensorDataCreate) -> SensorDataSchema:
    async with get_session() as session:
        sensor = SensorData(
            device_id=device_id,
            timestamp=data_in.timestamp or datetime.utcnow(),
            value=data_in.value,
            unit=data_in.unit,
        )
        session.add(sensor)
        await session.commit()
        await session.refresh(sensor)
        return SensorDataSchema.from_orm(sensor)


async def get_sensor_data(
    device_id: int, start: Optional[datetime] = None, end: Optional[datetime] = None
) -> List[SensorDataSchema]:
    async with get_session() as session:
        stmt = select(SensorData).where(SensorData.device_id == device_id)
        if start:
            stmt = stmt.where(SensorData.timestamp >= start)
        if end:
            stmt = stmt.where(SensorData.timestamp <= end)
        result = await session.execute(stmt.order_by(SensorData.timestamp.desc()))
        rows = result.scalars().all()
        return [SensorDataSchema.from_orm(r) for r in rows]


# ---------- Control command CRUD ----------
async def send_control_command(command_in: ControlCommandCreate) -> ControlCommandSchema:
    async with get_session() as session:
        cmd = ControlCommand(
            device_id=command_in.device_id,
            command=command_in.command,
            payload=command_in.payload,
        )
        session.add(cmd)
        await session.commit()
        await session.refresh(cmd)
        return ControlCommandSchema.from_orm(cmd)


# ---------- Utility: create hypertable ----------
async def create_hypertable() -> None:
    """Create the sensor_data hypertable if it does not exist.

    TimescaleDB requires a separate SQL command to convert a regular
    table into a hypertable.  This function should be called once at
    application startup.
    """
    from sqlalchemy import text

    async with get_session() as session:
        await session.execute(
            text(
                """
                SELECT create_hypertable('sensor_data', 'timestamp', if_not_exists => true);
                """
            )
        )
        await session.commit()


# ---------- Exports ----------
__all__ = [
    "create_device",
    "get_device",
    "list_devices",
    "ingest_sensor_data",
    "get_sensor_data",
    "send_control_command",
    "create_hypertable",
]
