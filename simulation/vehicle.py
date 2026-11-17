from dataclasses import dataclass

from config import (
    CAR_WIDTH,
    CAR_LENGTH,
    MAX_SPEED,
)


@dataclass
class Vehicle:
    """
    Represents the autonomous vehicle.
    """

    x: float = 0.0
    y: float = 0.0
    speed: float = 16.0
    steering: float = 0.0

    width: float = CAR_WIDTH
    length: float = CAR_LENGTH

    def update(self, acceleration, steering_rate, dt):
        """
        Update vehicle speed, steering and position.
        """

        # Update speed
        self.speed += acceleration * dt

        # Prevent negative speed
        self.speed = max(0.0, self.speed)

        # Limit maximum speed
        self.speed = min(
            self.speed,
            MAX_SPEED
        )

        # Update steering
        self.steering += steering_rate * dt

        # Limit steering
        self.steering = max(
            -1.0,
            min(1.0, self.steering)
        )

        # Move forward
        self.x += self.speed * dt

        # Simplified lateral movement
        self.y += self.steering * 1.8 * dt