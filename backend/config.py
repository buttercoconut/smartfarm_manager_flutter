"""Configuration module for the SmartFarm backend.

This module centralises all configuration values so that they can be
imported from anywhere in the application without creating circular
imports.  The values are read from environment variables with sensible
defaults for local development.

The configuration is intentionally simple – for a production system you
might want to use a library such as `pydantic-settings` or `dynaconf`.
"""

from __future__ import annotations

import os
from pathlib import Path

# ---------------------------------------------------------------------------
# General settings
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent

# ---------------------------------------------------------------------------
# Database settings
# ---------------------------------------------------------------------------
# PostgreSQL connection string.  TimescaleDB is a PostgreSQL extension, so
# the same connection string works.
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/smartfarm")

# ---------------------------------------------------------------------------
# MQTT settings
# ---------------------------------------------------------------------------
MQTT_BROKER_HOST = os.getenv("MQTT_BROKER_HOST", "localhost")
MQTT_BROKER_PORT = int(os.getenv("MQTT_BROKER_PORT", "1883"))
MQTT_KEEPALIVE = int(os.getenv("MQTT_KEEPALIVE", "60"))
MQTT_TOPICS = os.getenv("MQTT_TOPICS", "sensors/#")  # subscribe to all sensor topics

# ---------------------------------------------------------------------------
# FastAPI settings
# ---------------------------------------------------------------------------
API_TITLE = os.getenv("API_TITLE", "SmartFarm Manager API")
API_DESCRIPTION = os.getenv("API_DESCRIPTION", "API for managing smart farm devices and sensor data.")
API_VERSION = os.getenv("API_VERSION", "0.1.0")

# ---------------------------------------------------------------------------
# Logging settings
# ---------------------------------------------------------------------------
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# ---------------------------------------------------------------------------
# Miscellaneous
# ---------------------------------------------------------------------------
# Number of seconds to keep MQTT messages in memory before discarding
MQTT_MESSAGE_CACHE_TTL = int(os.getenv("MQTT_MESSAGE_CACHE_TTL", "300"))

# ---------------------------------------------------------------------------
# Exported dictionary for easy use in FastAPI's settings
# ---------------------------------------------------------------------------
settings = {
    "database_url": DATABASE_URL,
    "mqtt_broker_host": MQTT_BROKER_HOST,
    "mqtt_broker_port": MQTT_BROKER_PORT,
    "mqtt_keepalive": MQTT_KEEPALIVE,
    "mqtt_topics": MQTT_TOPICS,
    "api_title": API_TITLE,
    "api_description": API_DESCRIPTION,
    "api_version": API_VERSION,
    "log_level": LOG_LEVEL,
    "mqtt_message_cache_ttl": MQTT_MESSAGE_CACHE_TTL,
}
