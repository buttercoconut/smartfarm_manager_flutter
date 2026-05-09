"""FastAPI application entry point.

The app includes routers for devices and sensors, starts the MQTT
client on startup, and creates the database tables.  The code is
structured so that it can be imported by a test suite without
side‑effects.
"""

from __future__ import annotations

import logging
from fastapi import FastAPI

from .config import settings
from .crud import create_hypertable, init_models
from .mqtt import start_mqtt, stop_mqtt
from .routers.devices import router as devices_router
from .routers.sensors import router as sensors_router

# Configure logging – in production you might want a more sophisticated
# logger configuration.
logging.basicConfig(level=settings["log_level"], format="[%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("smartfarm_backend")

app = FastAPI(
    title=settings["api_title"],
    description=settings["api_description"],
    version=settings["api_version"],
)

# Register routers
app.include_router(devices_router, prefix="/devices", tags=["devices"])
app.include_router(sensors_router, prefix="/sensors", tags=["sensors"])


@app.on_event("startup")
async def startup() -> None:
    logger.info("Starting SmartFarm backend")
    # Create tables and hypertable
    await init_models()
    await create_hypertable()
    # Start MQTT client
    start_mqtt(app)


@app.on_event("shutdown")
def shutdown() -> None:
    logger.info("Shutting down SmartFarm backend")
    stop_mqtt()


# Expose the app for ASGI servers
__all__ = ["app"]
