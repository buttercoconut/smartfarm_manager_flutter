"""Control command execution (demo)."""

from ..models import ControlCommand

async def execute(cmd: ControlCommand) -> ControlCommand:
    # In a real system this would publish to MQTT or send to device
    print(f"Executing command: {cmd}")
    return cmd
