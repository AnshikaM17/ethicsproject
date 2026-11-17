import numpy as np

from config import SENSOR_RANGE


class RiskAssessment:

    def __init__(self, sensor_failure=False):

        self.sensor_failure = sensor_failure
        self.confidence = 1.0

    def calculate(self, detections):

        # No objects detected
        if not detections:

            self.confidence = (
                0.75
                if self.sensor_failure
                else 1.0
            )

            return 0.0

        # Closest detected object
        nearest = detections[0]

        distance = nearest["distance"]

        relative_speed = max(
            0.0,
            nearest["relative_speed"]
        )

        # -----------------------------
        # TIME TO COLLISION
        # -----------------------------

        if relative_speed > 0.1:

            ttc = (
                distance /
                relative_speed
            )

        else:

            ttc = np.inf

        # -----------------------------
        # DISTANCE RISK
        # -----------------------------

        distance_risk = np.clip(
            1.0 -
            distance / SENSOR_RANGE,
            0.0,
            1.0
        )

        # -----------------------------
        # TTC RISK
        # -----------------------------

        if np.isinf(ttc):

            ttc_risk = 0.0

        else:

            ttc_risk = np.clip(
                1.0 -
                ttc / 6.0,
                0.0,
                1.0
            )

        # -----------------------------
        # COMBINED RISK
        # -----------------------------

        risk = (
            0.45 * distance_risk
            +
            0.55 * ttc_risk
        )

        # -----------------------------
        # SENSOR CONFIDENCE
        # -----------------------------

        self.confidence = (
            0.75
            if self.sensor_failure
            else 1.0
        )

        # If sensor confidence is low,
        # make the system more conservative.
        if self.confidence < 0.8:

            risk += 0.15

        risk = np.clip(
            risk,
            0.0,
            1.0
        )

        return float(risk)