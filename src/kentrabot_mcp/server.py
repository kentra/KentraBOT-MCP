from fastmcp import FastMCP
from kentrabot_mcp.drivers.dummy import DummyRobot
# from kentrabot_mcp.drivers.real import RealRobot # TODO: Implement when hardware known

# Initialize Robot Driver
# In the future, we can swap this based on env var or config
robot = DummyRobot()

# Initialize MCP Server
mcp = FastMCP("KentraBOT")

# Logic functions (for easy testing)
def move_logic(left_speed: float, right_speed: float) -> str:
    robot.set_motors(left_speed, right_speed)
    return f"Moved: Left={left_speed}, Right={right_speed}"

def stop_logic() -> str:
    robot.stop()
    return "STOPPED"

def drive_logic(direction: str, speed: float = 0.5) -> str:
    s = max(0.0, min(abs(speed), 1.0))
    if direction == "forward":
        robot.set_motors(s, s)
    elif direction == "backward":
        robot.set_motors(-s, -s)
    elif direction == "left":
        robot.set_motors(-s, s)
    elif direction == "right":
        robot.set_motors(s, -s)
    else:
        return f"Unknown direction: {direction}"
    return f"Driving {direction} at speed {s}"

# Tool Definitions
@mcp.tool()
def move(left_speed: float, right_speed: float) -> str:
    """
    Control independent track speeds.
    
    Args:
        left_speed: Speed for left track (-1.0 to 1.0). Negative is backward.
        right_speed: Speed for right track (-1.0 to 1.0). Negative is backward.
    """
    return move_logic(left_speed, right_speed)

@mcp.tool()
def stop() -> str:
    """
    Emergency stop. Halts both motors immediately.
    """
    return stop_logic()

@mcp.tool()
def drive(direction: str, speed: float = 0.5) -> str:
    """
    High level drive command.
    
    Args:
        direction: 'forward', 'backward', 'left', 'right'
        speed: 0.0 to 1.0 (default 0.5)
    """
    return drive_logic(direction, speed)

def main():
    mcp.run()

if __name__ == "__main__":
    main()
