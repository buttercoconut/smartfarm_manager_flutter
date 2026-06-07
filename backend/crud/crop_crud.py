"""CRUD operations for crop data (in‑memory for demo)."""

from typing import List
from ..models import Crop

_crop_db: List[Crop] = []

async def create(data: Crop) -> Crop:
    _crop_db.append(data)
    return data

async def list(limit: int = 100) -> List[Crop]:
    return _crop_db[-limit:]
