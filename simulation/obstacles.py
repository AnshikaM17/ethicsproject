from dataclasses import dataclass


@dataclass
class Obstacle:
    """
    Represents another vehicle or obstacle.
    """

    x: float
    y: float
    speed: float

    width: float = 1.8
    length: float = 4.0

    def update(self, dt):
        """
        Move obstacle forward.
        """

        self.x += self.speed * dt