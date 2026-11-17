from simulation.vehicle import Vehicle
from simulation.environment import create_scenario

from ai.perception import PerceptionSystem
from ai.risk_assessment import RiskAssessment
from ai.decision import DecisionSystem

from safety.safety_monitor import SafetyMonitor

from visualization.dashboard import Dashboard


def run():

    print()
    print("=" * 60)
    print(" AI AUTONOMOUS VEHICLE SIMULATOR")
    print("=" * 60)

    print()
    print("Choose simulation:")
    print()
    print("1. Normal sensor")
    print("2. Sensor failure")
    print()

    choice = input(
        "Enter choice (1/2): "
    ).strip()

    # ----------------------------------
    # SENSOR MODE
    # ----------------------------------

    sensor_failure = (
        choice == "2"
    )

    # ----------------------------------
    # CREATE VEHICLE
    # ----------------------------------

    vehicle = Vehicle()

    # ----------------------------------
    # CREATE ENVIRONMENT
    # ----------------------------------

    obstacles = create_scenario()

    # ----------------------------------
    # CREATE AI
    # ----------------------------------

    perception = PerceptionSystem(
        sensor_noise=0.20,
        sensor_failure=sensor_failure
    )

    risk_system = RiskAssessment(
        sensor_failure=sensor_failure
    )

    decision_system = DecisionSystem()

    # ----------------------------------
    # SAFETY
    # ----------------------------------

    safety = SafetyMonitor()

    # ----------------------------------
    # DASHBOARD
    # ----------------------------------

    dashboard = Dashboard(

        vehicle=vehicle,

        obstacles=obstacles,

        perception=perception,

        risk_system=risk_system,

        decision_system=decision_system,

        safety=safety,

        sensor_failure=sensor_failure
    )

    # ----------------------------------
    # START
    # ----------------------------------

    dashboard.start()


if __name__ == "__main__":

    run()