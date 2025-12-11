from abc import ABC, abstractmethod

class Robot(ABC):
    """Abstract Base Class for Robot Hardware Abstraction Layer."""

    @abstractmethod
    def set_motors(self, left_speed: float, right_speed: float) -> None:
        """
        Set motor speeds.
        :param left_speed: Speed for left motor (-1.0 to 1.0)
        :param right_speed: Speed for right motor (-1.0 to 1.0)
        """
        pass

    @abstractmethod
    def stop(self) -> None:
        """Stop all motors immediately."""
        pass
