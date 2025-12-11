import asyncio
import os
import logging
from typing import Optional
from bleak import BleakClient

from kentrabot_mcp.robot import Robot

logger = logging.getLogger("kentrabot.ble")

class BleRobot(Robot):
    def __init__(self):
        self.device_uuid = os.environ.get("KENTRABOT_BLE_DEVICE_UUID")
        self.char_uuid = os.environ.get("KENTRABOT_BLE_CHAR_UUID")
        
        if not self.device_uuid:
            logger.warning("KENTRABOT_BLE_DEVICE_UUID not set. BLE driver will fail to connect.")
        if not self.char_uuid:
            logger.warning("KENTRABOT_BLE_CHAR_UUID not set. BLE driver will fail to write.")

    def _to_signed_byte(self, val: int) -> int:
        # Clamp -100 to 100
        val = max(min(int(val), 100), -100)
        # Convert to unsigned byte (0-255) representing the signed value (2's complement)
        return val & 0xFF 

    def _build_packet(self, speed_a: int, speed_b: int, speed_c: int = 0, speed_d: int = 0) -> bytes:
        # Calculate Checksum
        # Based on user logic: simple sum of the bytes
        # Note: User code had `value[-1]` which implied some structure, but the core logic
        # is likely just summing the byte values of the speeds.
        
        sa = self._to_signed_byte(speed_a)
        sb = self._to_signed_byte(speed_b)
        sc = self._to_signed_byte(speed_c)
        sd = self._to_signed_byte(speed_d)

        checksum = (sa + sb + sc + sd) & 0xFF
        
        # Header AB CD 01 ...
        return bytes([
            0xAB,
            0xCD,
            0x01,
            sa,
            sb,
            sc,
            sd,
            checksum,
        ])

    async def _send(self, data: bytes) -> None:
        if not self.device_uuid or not self.char_uuid:
            logger.error("Cannot send: Missing BLE UUIDs configuration.")
            return

        try:
            # Note: Creating a new connection for every command has high latency.
            # Ideally, we would maintain a persistent connection.
            async with BleakClient(self.device_uuid) as client:
                await client.write_gatt_char(self.char_uuid, data)
                logger.info(f"BLE Write: {data.hex()}")
        except Exception as e:
            logger.error(f"BLE communication error: {e}")

    async def set_motors(self, left_speed: float, right_speed: float) -> None:
        """
        Sets motor speeds.
        Converts float -1.0..1.0 to int -100..100
        """
        # Map Left -> Motor A, Right -> Motor B (Assumption)
        l_int = int(left_speed * 100)
        r_int = int(right_speed * 100)
        
        packet = self._build_packet(speed_a=l_int, speed_b=r_int)
        await self._send(packet)

    async def stop(self) -> None:
        packet = self._build_packet(0, 0)
        await self._send(packet)
