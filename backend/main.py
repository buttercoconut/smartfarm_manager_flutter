"""FastAPI application entry point for SmartFarm Manager backend."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import sensor, crop, control

app = FastAPI(title="SmartFarm Manager API")

# Allow CORS for Flutter app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sensor.router, prefix="/api/sensor", tags=["sensor"])
app.include_router(crop.router, prefix="/api/crop", tags=["crop"])
app.include_router(control.router, prefix="/api/control", tags=["control"])

@app.get("/")
async def root():
    return {"message": "SmartFarm Manager API is running."}
