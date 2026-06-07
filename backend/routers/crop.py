"""Router for crop endpoints."""

from fastapi import APIRouter, HTTPException
from typing import List

from ..models import Crop
from ..crud import crop_crud

router = APIRouter()

@router.post("/", response_model=Crop)
async def create_crop(data: Crop):
    return await crop_crud.create(data)

@router.get("/", response_model=List[Crop])
async def read_crops(limit: int = 100):
    return await crop_crud.list(limit)
