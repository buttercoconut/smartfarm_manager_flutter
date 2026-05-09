"""ORM models for the SmartFarm backend.

The database schema is intentionally minimal – it can be extended as
needed.  TimescaleDB is a PostgreSQL extension that adds time‑series
capabilities; the `sensor_data` table is created as a hypertable in the
startup script.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from .database import Base


class Device(Base):
    """Represents a physical device in the farm.

    * `id` – primary key.
    * `name` – human‑readable name.
    * `type` – e.g. "irrigation_pump", "temperature_sensor".
    * `location` – optional description of where the device is.
    * `active` – whether the device is currently online.
    """

    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    type = Column(String, nullable=False)
    location = Column(String, nullable=True)
    active = Column(Boolean, default=True)

    # One‑to‑many relationship to sensor data – a device can produce many
    # sensor readings.
    sensor_data = relationship("SensorData", back_populates="device")

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Device {self.id} {self.name} ({self.type})>"


class SensorData(Base):
    """Time‑series data produced by a device.

    TimescaleDB will store this as a hypertable.  The `timestamp` column
    is the primary key together with `device_id` – this guarantees that
    each device can only have one reading per timestamp.
    """

    __tablename__ = "sensor_data"

    device_id = Column(Integer, ForeignKey("devices.id"), primary_key=True)
    timestamp = Column(DateTime, primary_key=True, default=datetime.utcnow)
    value = Column(Float, nullable=False)
    unit = Column(String, nullable=True)

    device = relationship("Device", back_populates="sensor_data")

    def __repr__(self) -> str:  # pragma: no cover
        return f"<SensorData {self.device_id} {self.timestamp} {self.value}{self.unit or ''}>"


class ControlCommand(Base):
    """Commands sent to devices.

    The command is stored so that we can audit what was sent and when.
    """

    __tablename__ = "control_commands"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("devices.id"), nullable=False)
    command = Column(String, nullable=False)
    payload = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    device = relationship("Device")

    def __repr__(self) -> str:  # pragma: no cover
        return f"<ControlCommand {self.id} {self.command} to {self.device_id}>"
