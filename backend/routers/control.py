"""Router for control commands."""

from fastapi import APIRouter
from ..models import ControlCommand
from ..crud import control_crud

router = APIRouter()

@router.post("/", response_model=ControlCommand)
async def send_command(cmd: ControlCommand):
    return await control_crud.execute(cmd)
