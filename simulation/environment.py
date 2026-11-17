from simulation.obstacles import Obstacle


def create_scenario():
    """
    Create vehicles/obstacles for our simulation.
    """

    obstacles = [

        # Slow vehicle directly ahead
        Obstacle(
            x=55.0,
            y=0.0,
            speed=8.0
        ),

        # Second slow vehicle
        Obstacle(
            x=125.0,
            y=0.2,
            speed=5.0
        ),

        # Vehicle in another lane
        Obstacle(
            x=190.0,
            y=-3.0,
            speed=10.0
        ),

        # Another vehicle
        Obstacle(
            x=245.0,
            y=0.0,
            speed=7.0
        ),
    ]

    return obstacles