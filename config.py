# ==========================================
# AUTONOMOUS VEHICLE SIMULATION CONFIG
# ==========================================

# Simulation
DT = 0.1

# Road
ROAD_WIDTH = 10.0

# Autonomous vehicle dimensions
CAR_WIDTH = 1.8
CAR_LENGTH = 4.0

# Vehicle limits
MAX_SPEED = 22.0
MAX_ACCELERATION = 2.0
MAX_DECELERATION = 8.0

# Sensor
SENSOR_RANGE = 60.0
SENSOR_NOISE = 0.20

# Risk thresholds
BRAKE_RISK_THRESHOLD = 0.45
EMERGENCY_RISK_THRESHOLD = 0.80

# Distance thresholds
SAFE_DISTANCE = 18.0
EMERGENCY_DISTANCE = 7.0

# Time-to-collision thresholds
SAFE_TIME_GAP = 2.5
EMERGENCY_TIME_GAP = 1.2