class SafetyMonitor:

    def __init__(self):

        self.collision = False

        self.emergency_brakes = 0

        self.near_misses = 0

    def check_collision(
        self,
        vehicle,
        obstacles
    ):

        for obstacle in obstacles:

            longitudinal_distance = abs(
                obstacle.x -
                vehicle.x
            )

            lateral_distance = abs(
                obstacle.y -
                vehicle.y
            )

            # Simplified collision boundary
            if (
                longitudinal_distance < 4.0
                and
                lateral_distance < 1.8
            ):

                self.collision = True

                return True

        return False

    def record_action(self, action):

        if action == "EMERGENCY_BRAKE":

            self.emergency_brakes += 1

    def record_near_miss(
        self,
        detections
    ):

        if detections:

            distance = (
                detections[0]["distance"]
            )

            if distance < 10:

                self.near_misses += 1