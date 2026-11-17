from config import (
    BRAKE_RISK_THRESHOLD,
    EMERGENCY_RISK_THRESHOLD,
    SAFE_DISTANCE,
    EMERGENCY_DISTANCE,
    SAFE_TIME_GAP,
    EMERGENCY_TIME_GAP,
)


class DecisionSystem:

    def decide(
        self,
        vehicle,
        detections,
        risk
    ):

        # No obstacle detected
        if not detections:

            return "CRUISE"

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

            ttc = float("inf")

        # -----------------------------
        # EMERGENCY BRAKING
        # -----------------------------

        if (
            distance < EMERGENCY_DISTANCE
            or
            ttc < EMERGENCY_TIME_GAP
            or
            risk >= EMERGENCY_RISK_THRESHOLD
        ):

            return "EMERGENCY_BRAKE"

        # -----------------------------
        # NORMAL BRAKING
        # -----------------------------

        if (
            distance < SAFE_DISTANCE
            or
            ttc < SAFE_TIME_GAP
            or
            risk >= BRAKE_RISK_THRESHOLD
        ):

            return "BRAKE"

        # -----------------------------
        # LANE CHANGE
        # -----------------------------

        if (
            distance < 30
            and
            abs(
                nearest["lateral_offset"]
            ) < 1.0
        ):

            if vehicle.y <= 0:

                return "STEER_LEFT"

            return "STEER_RIGHT"

        # -----------------------------
        # NORMAL DRIVING
        # -----------------------------

        return "CRUISE"