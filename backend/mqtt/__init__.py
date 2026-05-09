"""MQTT client that forwards sensor messages to the database.

The client subscribes to the topics defined in `config.MQTT_TOPICS`.
When a message arrives it is parsed as JSON and the relevant fields
are extracted.  The message is then passed to `crud.ingest_sensor_data`.

The client runs in a background task started by FastAPI's startup
event.
"""

from __future__ import annotations

import json
import logging
from typing import Any

import paho.mqtt.client as mqtt
from fastapi import FastAPI

from .config import settings
from .crud import ingest_sensor_data

logger = logging.getLogger("mqtt_client")

# Global client instance – we keep it simple for this example.
mqtt_client: mqtt.Client | None = None


def _on_connect(client: mqtt.Client, userdata: Any, flags: Any, rc: int) -> None:
    if rc == 0:
        logger.info("Connected to MQTT broker")
        # Subscribe to all sensor topics.
        client.subscribe(settings["mqtt_topics"])
    else:
        logger.error("Failed to connect to MQTT broker, rc=%s", rc)


def _on_message(client: mqtt.Client, userdata: Any, msg: mqtt.MQTTMessage) -> None:
    try:
        payload = json.loads(msg.payload.decode("utf-8"))
        # Expected payload format: {"device_id": int, "value": float, "unit": str}
        device_id = int(payload["device_id"])
        value = float(payload["value"])
        unit = payload.get("unit")
        # Ingest into DB – we ignore the timestamp from MQTT and use DB time.
        # In a real system you might preserve the original timestamp.
        import asyncio

        asyncio.create_task(
            ingest_sensor_data(device_id, payload)
        )
        logger.debug("Ingested sensor data for device %s", device_id)
    except Exception as e:
        logger.exception("Failed to process MQTT message: %s", e)


def start_mqtt(app: FastAPI) -> None:
    global mqtt_client
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = _on_connect
    mqtt_client.on_message = _on_message
    mqtt_client.connect(settings["mqtt_broker_host"], settings["mqtt_broker_port"], settings["mqtt_keepalive"])
    # Run the network loop in a separate thread.
    mqtt_client.loop_start()
    logger.info("MQTT client started")


def stop_mqtt() -> None:
    global mqtt_client
    if mqtt_client:
        mqtt_client.loop_stop()
        mqtt_client.disconnect()
        logger.info("MQTT client stopped")


__all__ = ["start_mqtt", "stop_mqtt"]
