import asyncio
import os
from fastmcp import FastMCP
from kentrabot_mcp.drivers.dummy import DummyRobot
from kentrabot_mcp.drivers.ble import BleRobot

# Initialize Robot Driver based on configuration
if os.environ.get("KENTRABOT_USE_BLE") == "1":
    print("Initializing BLE Driver...")
    robot = BleRobot()
else:
    print("Initializing Dummy Driver (set KENTRABOT_USE_BLE=1 to use BLE)...")
    robot = DummyRobot()

# Initialize MCP Server
mcp = FastMCP("KentraBOT")

# Logic functions (async)
async def move_logic(left_speed: float, right_speed: float) -> str:
    await robot.set_motors(left_speed, right_speed)
    return f"Moved: Left={left_speed}, Right={right_speed}"

async def stop_logic() -> str:
    await robot.stop()
    return "STOPPED"

async def drive_logic(direction: str, speed: float = 0.5) -> str:
    s = max(0.0, min(abs(speed), 1.0))
    if direction == "forward":
        await robot.set_motors(s, s)
    elif direction == "backward":
        await robot.set_motors(-s, -s)
    elif direction == "left":
        await robot.set_motors(-s, s)
    elif direction == "right":
        await robot.set_motors(s, -s)
    else:
        return f"Unknown direction: {direction}"
    return f"Driving {direction} at speed {s}"

# Tool Definitions
@mcp.tool()
async def move(left_speed: float, right_speed: float) -> str:
    """
    Control independent track speeds.
    
    Args:
        left_speed: Speed for left track (-1.0 to 1.0). Negative is backward.
        right_speed: Speed for right track (-1.0 to 1.0). Negative is backward.
    """
    return await move_logic(left_speed, right_speed)

@mcp.tool()
async def stop() -> str:
    """
    Emergency stop. Halts both motors immediately.
    """
    return await stop_logic()

@mcp.tool()
async def drive(direction: str, speed: float = 0.5) -> str:
    """
    High level drive command.
    
    Args:
        direction: 'forward', 'backward', 'left', 'right'
        speed: 0.0 to 1.0 (default 0.5)
    """
    return await drive_logic(direction, speed)

def main():
    mcp.run()

if __name__ == "__main__":
    main()
