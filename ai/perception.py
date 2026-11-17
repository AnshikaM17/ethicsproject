import numpy as np

from config import SENSOR_RANGE


class PerceptionSystem:

    def __init__(
        self,
        sensor_noise=0.20,
        sensor_failure=False
    ):

        self.sensor_noise = sensor_noise
        self.sensor_failure = sensor_failure

    def detect(self, vehicle, obstacles):

        detections = []

        for obstacle in obstacles:

            # Distance in front of vehicle
            dx = obstacle.x - vehicle.x

            # Distance sideways
            dy = obstacle.y - vehicle.y

            # Ignore objects behind us
            if dx <= 0:
                continue

            # Ignore objects beyond sensor range
            if dx > SENSOR_RANGE:
                continue

            # Ignore objects far away laterally
            if abs(dy) > 5:
                continue

            # Approximate distance between vehicles
            distance = (
                dx
                - vehicle.length / 2
                - obstacle.length / 2
            )

            distance = max(
                0.1,
                distance
            )

            # Relative speed
            relative_speed = (
                vehicle.speed
                - obstacle.speed
            )

            # Simulate sensor noise
            measured_distance = (
                distance
                + np.random.normal(
                    0,
                    self.sensor_noise
                )
            )

            measured_relative_speed = (
                relative_speed
                + np.random.normal(
                    0,
                    self.sensor_noise
                )
            )

            detections.append({

                "distance":
                    max(
                        0.1,
                        measured_distance
                    ),

                "relative_speed":
                    measured_relative_speed,

                "lateral_offset":
                    dy,

                "obstacle":
                    obstacle
            })

        # Closest obstacle first
        detections.sort(
            key=lambda item:
            item["distance"]
        )

        # Simulated sensor failure
        if (
            self.sensor_failure
            and detections
            and np.random.random() < 0.25
        ):

            # Pretend that the closest object
            # was not detected.
            detections.pop(0)

        return detections