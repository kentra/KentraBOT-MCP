from kentrabot_mcp.robot import Robot
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("kentrabot.dummy")

class DummyRobot(Robot):
    """Dummy Robot driver that logs actions instead of moving motors."""

    def __init__(self):
        self.left_speed = 0.0
        self.right_speed = 0.0
        logger.info("Dummy Robot Initialized")

    def set_motors(self, left_speed: float, right_speed: float) -> None:
        self.left_speed = max(min(left_speed, 1.0), -1.0)
        self.right_speed = max(min(right_speed, 1.0), -1.0)
        logger.info(f"MOTORS SET: Left={self.left_speed:.2f}, Right={self.right_speed:.2f}")

    def stop(self) -> None:
        self.left_speed = 0.0
        self.right_speed = 0.0
        logger.info("MOTORS STOPPED")
