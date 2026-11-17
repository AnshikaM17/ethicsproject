import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Rectangle

from config import (
    ROAD_WIDTH,
    DT,
)


class Dashboard:

    def __init__(
        self,
        vehicle,
        obstacles,
        perception,
        risk_system,
        decision_system,
        safety,
        sensor_failure=False,
    ):

        self.vehicle = vehicle
        self.obstacles = obstacles

        self.perception = perception
        self.risk_system = risk_system
        self.decision_system = decision_system
        self.safety = safety

        self.sensor_failure = sensor_failure

        # Risk history
        self.times = []
        self.risks = []

        self.simulation_time = 0

        # ----------------------------------
        # CREATE FIGURE
        # ----------------------------------

        self.fig = plt.figure(
            figsize=(14, 8)
        )

        self.ax_road = self.fig.add_subplot(
            2,
            1,
            1
        )

        self.ax_risk = self.fig.add_subplot(
            2,
            1,
            2
        )

        self.setup_road()
        self.setup_risk_graph()

    # ======================================
    # ROAD
    # ======================================

    def setup_road(self):

        self.ax_road.set_xlim(
            -10,
            100
        )

        self.ax_road.set_ylim(
            -6,
            6
        )

        self.ax_road.set_title(
            "AI Autonomous Vehicle "
            "Risk Mitigation System",
            fontsize=18,
            fontweight="bold"
        )

        self.ax_road.set_xlabel(
            "Distance (m)"
        )

        self.ax_road.set_ylabel(
            "Lane position"
        )

        # Road
        self.ax_road.axhspan(
            -ROAD_WIDTH / 2,
            ROAD_WIDTH / 2,
            color="gray",
            alpha=0.3
        )

        # Road boundaries
        self.ax_road.axhline(
            ROAD_WIDTH / 2,
            color="black",
            linewidth=2
        )

        self.ax_road.axhline(
            -ROAD_WIDTH / 2,
            color="black",
            linewidth=2
        )

        # Lane markings
        self.ax_road.axhline(
            0,
            color="white",
            linestyle="--",
            linewidth=2
        )

        # Vehicle
        self.vehicle_plot = self.ax_road.scatter(
            [],
            [],
            s=500,
            color="blue",
            marker="s",
            label="Autonomous Vehicle"
        )

        # Obstacles
        self.obstacle_plot = self.ax_road.scatter(
            [],
            [],
            s=400,
            color="red",
            marker="s",
            label="Other Vehicle"
        )

        # Sensor detection line
        self.sensor_line, = self.ax_road.plot(
            [],
            [],
            color="cyan",
            linewidth=2,
            alpha=0.7,
            label="Sensor Range"
        )

        self.ax_road.legend(
            loc="upper left"
        )

        # Information box
        self.info_text = self.ax_road.text(
            0.98,
            0.95,
            "",
            transform=self.ax_road.transAxes,
            ha="right",
            va="top",
            fontsize=11,
            bbox=dict(
                boxstyle="round",
                facecolor="white",
                alpha=0.9
            )
        )

    # ======================================
    # RISK GRAPH
    # ======================================

    def setup_risk_graph(self):

        self.ax_risk.set_xlim(
            0,
            30
        )

        self.ax_risk.set_ylim(
            0,
            1
        )

        self.ax_risk.set_title(
            "Real-Time AI Collision Risk"
        )

        self.ax_risk.set_xlabel(
            "Time (seconds)"
        )

        self.ax_risk.set_ylabel(
            "Risk"
        )

        # Brake threshold
        self.ax_risk.axhline(
            0.45,
            color="orange",
            linestyle="--",
            label="Brake threshold"
        )

        # Emergency threshold
        self.ax_risk.axhline(
            0.80,
            color="red",
            linestyle="--",
            label="Emergency threshold"
        )

        self.risk_line, = self.ax_risk.plot(
            [],
            [],
            color="purple",
            linewidth=3
        )

        self.ax_risk.legend(
            loc="upper left"
        )

    # ======================================
    # UPDATE
    # ======================================

    def update(self, frame):

        # ----------------------------------
        # MOVE OBSTACLES
        # ----------------------------------

        for obstacle in self.obstacles:

            obstacle.update(DT)

        # ----------------------------------
        # PERCEPTION
        # ----------------------------------

        detections = self.perception.detect(
            self.vehicle,
            self.obstacles
        )

        # ----------------------------------
        # RISK
        # ----------------------------------

        risk = self.risk_system.calculate(
            detections
        )

        # ----------------------------------
        # DECISION
        # ----------------------------------

        action = self.decision_system.decide(
            self.vehicle,
            detections,
            risk
        )

        # ----------------------------------
        # SAFETY
        # ----------------------------------

        self.safety.record_action(
            action
        )

        self.safety.record_near_miss(
            detections
        )

        collision = self.safety.check_collision(
            self.vehicle,
            self.obstacles
        )

        # ----------------------------------
        # CONTROL
        # ----------------------------------

        if action == "CRUISE":

            acceleration = 1.0
            steering = (
                -0.5 *
                self.vehicle.y
            )

        elif action == "BRAKE":

            acceleration = -4.5
            steering = (
                -0.5 *
                self.vehicle.y
            )

        elif action == "EMERGENCY_BRAKE":

            acceleration = -8.0
            steering = 0

        elif action == "STEER_LEFT":

            acceleration = -1.0
            steering = 1.5

        elif action == "STEER_RIGHT":

            acceleration = -1.0
            steering = -1.5

        else:

            acceleration = 0
            steering = 0

        # Update vehicle
        self.vehicle.update(
            acceleration,
            steering,
            DT
        )

        # ----------------------------------
        # TIME
        # ----------------------------------

        self.simulation_time += DT

        # ----------------------------------
        # RISK HISTORY
        # ----------------------------------

        self.times.append(
            self.simulation_time
        )

        self.risks.append(
            risk
        )

        # Keep last 300 points
        self.times = self.times[-300:]
        self.risks = self.risks[-300:]

        # ----------------------------------
        # VEHICLE DISPLAY
        # ----------------------------------

        self.vehicle_plot.set_offsets(
            [[
                self.vehicle.x,
                self.vehicle.y
            ]]
        )

        # ----------------------------------
        # OBSTACLE DISPLAY
        # ----------------------------------

        visible_obstacles = [
            obstacle
            for obstacle in self.obstacles
            if (
                self.vehicle.x - 10
                <= obstacle.x
                <= self.vehicle.x + 100
            )
        ]

        self.obstacle_plot.set_offsets(
            [
                [
                    obstacle.x,
                    obstacle.y
                ]
                for obstacle
                in visible_obstacles
            ]
        )

        # ----------------------------------
        # SENSOR RANGE
        # ----------------------------------

        self.sensor_line.set_data(
            [
                self.vehicle.x,
                self.vehicle.x + 60
            ],
            [
                self.vehicle.y,
                self.vehicle.y
            ]
        )

        # ----------------------------------
        # CAMERA FOLLOW
        # ----------------------------------

        self.ax_road.set_xlim(
            self.vehicle.x - 10,
            self.vehicle.x + 90
        )

        # ----------------------------------
        # TTC
        # ----------------------------------

        if detections:

            nearest = detections[0]

            distance = nearest[
                "distance"
            ]

            relative_speed = max(
                0,
                nearest[
                    "relative_speed"
                ]
            )

            if relative_speed > 0.1:

                ttc = (
                    distance /
                    relative_speed
                )

            else:

                ttc = float("inf")

        else:

            distance = float("inf")
            ttc = float("inf")

        # ----------------------------------
        # RISK COLOR
        # ----------------------------------

        if risk < 0.30:

            risk_status = "LOW"

        elif risk < 0.45:

            risk_status = "MODERATE"

        elif risk < 0.80:

            risk_status = "HIGH"

        else:

            risk_status = "CRITICAL"

        # ----------------------------------
        # INFO PANEL
        # ----------------------------------

        ttc_text = (
            f"{ttc:.2f} s"
            if ttc != float("inf")
            else "∞"
        )

        distance_text = (
            f"{distance:.1f} m"
            if distance != float("inf")
            else "No obstacle"
        )

        sensor_status = (
            "DEGRADED"
            if self.sensor_failure
            else "NORMAL"
        )

        self.info_text.set_text(

            f"AI STATUS\n"
            f"──────────────\n"
            f"Speed: "
            f"{self.vehicle.speed * 3.6:.1f} km/h\n"
            f"Obstacle: "
            f"{distance_text}\n"
            f"TTC: "
            f"{ttc_text}\n"
            f"Risk: "
            f"{risk:.2f} ({risk_status})\n"
            f"Confidence: "
            f"{self.risk_system.confidence:.2f}\n"
            f"Action: "
            f"{action}\n"
            f"Sensor: "
            f"{sensor_status}"
        )

        # ----------------------------------
        # RISK GRAPH
        # ----------------------------------

        self.risk_line.set_data(
            self.times,
            self.risks
        )

        if self.simulation_time > 30:

            self.ax_risk.set_xlim(
                self.simulation_time - 30,
                self.simulation_time
            )

        # ----------------------------------
        # STOP ON COLLISION
        # ----------------------------------

        if collision:

            self.ax_road.set_title(
                "⚠ COLLISION DETECTED",
                color="red",
                fontsize=20,
                fontweight="bold"
            )

            return (
                self.vehicle_plot,
                self.obstacle_plot,
                self.sensor_line,
                self.risk_line,
                self.info_text
            )

        # Stop after 60 seconds
        if self.simulation_time >= 60:

            return (
                self.vehicle_plot,
                self.obstacle_plot,
                self.sensor_line,
                self.risk_line,
                self.info_text
            )

        return (
            self.vehicle_plot,
            self.obstacle_plot,
            self.sensor_line,
            self.risk_line,
            self.info_text
        )

    # ======================================
    # START
    # ======================================

    def start(self):

        self.animation = FuncAnimation(
            self.fig,
            self.update,
            interval=DT * 1000,
            blit=False,
            cache_frame_data=False
        )

        plt.tight_layout()

        plt.show()