"""MQTT client for real‑time sensor data ingestion."""

import asyncio
import json
from typing import Callable

import paho.mqtt.client as mqtt

class MQTTClient:
    def __init__(self, broker: str, port: int, topic: str, on_message: Callable[[dict], None]):
        self.broker = broker
        self.port = port
        self.topic = topic
        self.on_message = on_message
        self.client = mqtt.Client()
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message

    def _on_connect(self, client, userdata, flags, rc):
        print(f"Connected to MQTT broker with result code {rc}")
        client.subscribe(self.topic)

    def _on_message(self, client, userdata, msg):
        payload = json.loads(msg.payload.decode())
        self.on_message(payload)

    def start(self):
        self.client.connect(self.broker, self.port, 60)
        loop = asyncio.get_event_loop()
        loop.run_in_executor(None, self.client.loop_forever)
