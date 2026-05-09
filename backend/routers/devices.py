"""Device router – CRUD for devices.

Endpoints:
- POST /devices/ – create a new device.
- GET /devices/ – list all devices.
- GET /devices/{id} – retrieve a single device.
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from ..crud import create_device, get_device, list_devices
from ..schemas import DeviceCreate, Device as DeviceSchema

router = APIRouter()


@router.post("/", response_model=DeviceSchema, status_code=status.HTTP_201_CREATED)
async def create_device_endpoint(device_in: DeviceCreate) -> DeviceSchema:
    return await create_device(device_in)


@router.get("/", response_model=list[DeviceSchema])
async def list_devices_endpoint() -> list[DeviceSchema]:
    return await list_devices()


@router.get("/{device_id}", response_model=DeviceSchema)
async def get_device_endpoint(device_id: int) -> DeviceSchema:
    try:
        return await get_device(device_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


__all__ = ["router"]
