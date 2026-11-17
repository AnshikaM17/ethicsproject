# AI Autonomous Vehicle Risk Mitigation Simulator

A 2D, real-time simulation of a self-driving car that **perceives** the vehicles around it, **scores collision risk**, **decides** how to drive, and **acts** on that decision — under both normal and degraded (failing) sensor conditions.

The project demonstrates the core idea behind autonomous-vehicle safety: a car should not just react to obstacles, it should *estimate how dangerous the situation is* and become *more cautious when it is less sure about what it sees*.

---

## What the project is trying to show

1. **Self-driving is a pipeline, not a single "AI".**
   Every autonomous vehicle repeats the same loop many times a second:
   `Sense → Assess risk → Decide → Act → Monitor safety`.
   Each stage in this project is a separate module so the loop is easy to see.

2. **Risk can be measured, not guessed.**
   The car turns raw sensor readings into a single risk score between 0 and 1 using two standard measures from driver-assistance systems:
   - **Distance** to the vehicle ahead
   - **Time-to-collision (TTC)** – how many seconds until impact if nothing changes

3. **Decisions should scale with risk.**
   Low risk → keep driving. Medium risk → brake gently. High risk → emergency brake. This mirrors how real Adaptive Cruise Control and Automatic Emergency Braking (AEB) work.

4. **Sensors fail, and the system must stay safe anyway.**
   In *Sensor failure* mode the car sometimes misses the closest vehicle (25% of the time). The system responds by lowering its confidence and adding a safety margin to its risk score, so it brakes earlier. This is the idea of **fail-safe / degraded-mode operation** used in real AV safety standards (e.g. ISO 26262, SOTIF).

5. **Safety must be monitored independently.**
   A separate safety monitor counts collisions, emergency brakes and near-misses, so the system's behaviour can be evaluated, not just watched.

---

## How it works

```
 ┌─────────────┐   ┌──────────────┐   ┌─────────────┐   ┌──────────┐   ┌───────────────┐
 │ Perception  │──▶│ Risk         │──▶│ Decision    │──▶│ Control  │──▶│ Safety        │
 │ (sensors +  │   │ Assessment   │   │ (rules)     │   │ (speed & │   │ Monitor       │
 │  noise)     │   │ (0–1 score)  │   │             │   │ steering)│   │ (collisions)  │
 └─────────────┘   └──────────────┘   └─────────────┘   └──────────┘   └───────────────┘
        ▲                                                                     │
        └──────────────────────── repeats every 0.1 s ────────────────────────┘
```

| Stage | File | What it does |
|---|---|---|
| Scenario | `simulation/environment.py` | Places 4 slower vehicles on the road ahead (one in the other lane). The autonomous car starts at 58 km/h. |
| Vehicle model | `simulation/vehicle.py`, `simulation/obstacles.py` | Simple physics: speed, steering and position updated every time step. |
| Perception | `ai/perception.py` | Detects vehicles within 60 m ahead. Adds random noise to distance and speed (real sensors are never perfect). In failure mode, drops the nearest detection 25% of the time. |
| Risk assessment | `ai/risk_assessment.py` | `risk = 0.45 × distance_risk + 0.55 × TTC_risk`. If sensor confidence is low (failure mode, confidence = 0.75), adds **+0.15** to be more conservative. |
| Decision | `ai/decision.py` | Rule-based choice of action (see table below). |
| Control | `visualization/dashboard.py` | Converts the action into acceleration and steering. |
| Safety monitor | `safety/safety_monitor.py` | Records collisions, emergency brakes and near-misses (< 10 m). |
| Settings | `config.py` | All limits and thresholds in one place. |

### Decision rules

| Action | Triggered when | Effect |
|---|---|---|
| `EMERGENCY_BRAKE` | gap < 7 m **or** TTC < 1.2 s **or** risk ≥ 0.80 | −8 m/s² |
| `BRAKE` | gap < 18 m **or** TTC < 2.5 s **or** risk ≥ 0.45 | −4.5 m/s², re-centre |
| `STEER_LEFT` / `STEER_RIGHT` | vehicle within 30 m directly ahead | slight slow-down + steer away |
| `CRUISE` | nothing threatening | accelerate gently, re-centre |

### Risk levels shown on screen

| Risk | Status |
|---|---|
| < 0.30 | LOW |
| 0.30 – 0.45 | MODERATE |
| 0.45 – 0.80 | HIGH (brake) |
| ≥ 0.80 | CRITICAL (emergency brake) |

---

## Running it

**Requirements:** Python 3.10+ with `numpy` and `matplotlib`.

```powershell
cd autonomous_vehicle_ai
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install numpy matplotlib
.\.venv\Scripts\python.exe main.py
```

(macOS/Linux: `source .venv/bin/activate` then `python main.py`.)

When asked, type:
- `1` – **Normal sensor**
- `2` – **Sensor failure** (degraded sensing)

A window opens with:
- **Top panel:** the road — blue square = autonomous car, red squares = other vehicles, cyan line = 60 m sensor range. The info box shows speed, gap, TTC, risk, confidence, current action and sensor status.
- **Bottom panel:** live risk graph with the brake (orange) and emergency (red) thresholds.

The animation keeps running until you close the window.

> Note: the `venv/` folder shipped with the project was created on a different computer and will not work elsewhere — create a fresh `.venv` as shown above.

---

## Results

50 runs of 60 simulated seconds in each mode (different random noise each run):

| | Normal sensor | Sensor failure |
|---|---|---|
| Collisions | **0 / 50** | **0 / 50** |
| Emergency brakes | 0 | 0 |
| Average peak risk | 0.59 | 0.53 |
| Average distance travelled | 401 m | 392 m |

**Takeaway:** the risk-based braking kept the car collision-free in every run, even when the sensor was randomly missing the vehicle ahead. Normal braking always acted early enough that the emergency brake was never needed.

---

## Limitations (and possible future work)

- **Rule-based, not learned.** The "AI" is a set of hand-designed formulas and thresholds; no model is trained. A next step would be to learn the risk function or driving policy from data (e.g. reinforcement learning).
- **No real overtaking.** Steering produces a small sideways movement and the car re-centres; it follows slower vehicles rather than passing them, sometimes slowing to a stop.
- **Confidence is fixed** (1.0 or 0.75) rather than estimated from sensor behaviour.
- **Simplified world:** straight road, constant-speed traffic, point-mass physics, single noisy sensor (no camera/LiDAR/radar fusion).
- Missed detections can make the risk score look *lower* than reality (average peak risk was lower in failure mode) — which is exactly why redundant sensors matter in real vehicles.

---

## Project structure

```
autonomous_vehicle_ai/
├── main.py                    # Entry point – choose mode, start simulation
├── config.py                  # All thresholds and limits
├── requirements.txt
├── ai/
│   ├── perception.py          # Noisy sensor + failure simulation
│   ├── risk_assessment.py     # Distance + TTC risk score, confidence
│   └── decision.py            # Rule-based driving decisions
├── safety/
│   └── safety_monitor.py      # Collisions, emergency brakes, near-misses
├── simulation/
│   ├── vehicle.py             # Autonomous car physics
│   ├── obstacles.py           # Other vehicles
│   └── environment.py         # Traffic scenario
├── visualization/
│   └── dashboard.py           # Live animated dashboard + control loop
└── results/
```
