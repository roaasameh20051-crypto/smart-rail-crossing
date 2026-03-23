# 🚆 Smart Rail Crossing Safety System

> **Portfolio project** — developed as part of a Siemens Mobility Fit4Rail internship application.  
> Demonstrates core mechatronics competencies: embedded control logic, sensor integration, safety-critical system design, and digital simulation.

---

## 📌 Overview

An automated level crossing safety system that detects incoming trains via IR sensors, controls road barriers and traffic signals, and alerts pedestrians through buzzers and an LCD display — all managed by a **4-state Finite State Machine (FSM)** implemented in Python.

The physical circuit is designed and simulated in **Proteus Design Suite**, with the control logic modelled in Python for clarity and portability.

---

## 🎯 Relevance to Siemens Mobility

| Siemens Pillar | How This Project Addresses It |
|---|---|
| Rail safety | Fail-safe barrier logic with pedestrian override |
| Automation | Sensor-driven FSM — no manual intervention needed |
| Electrification | DC motor, servo, and LED control modelling |
| Digitalization | Python simulation bridges physical and digital design |

---

## 🏗️ System Architecture

```
┌─────────────────── SENSOR LAYER ───────────────────┐
│  IR Sensor A          IR Sensor B      Ultrasonic   │
│  (train entry)        (train exit)     (pedestrian) │
└────────────────────────┬───────────────────────────┘
                         │ sensor data
                         ▼
┌─────────────────── CONTROL LAYER ──────────────────┐
│            Python Finite State Machine              │
│   IDLE → WARNING → CROSSING → CLEAR → IDLE         │
└──────┬──────────┬──────────┬──────────┬────────────┘
       │          │          │          │
       ▼          ▼          ▼          ▼
┌──────────── OUTPUT LAYER ──────────────────────────┐
│  Servo motor   Traffic LEDs   Buzzer   LCD display  │
│  (barrier)     (Red/Green)   (alert)  (status)      │
└────────────────────────────────────────────────────┘
```

---

## 🔄 State Machine

```
         IR-A detects train
IDLE ──────────────────────► WARNING
 ▲                              │
 │                   3s warning period
 │                              │
 │                              ▼
CLEAR ◄──────────────────── CROSSING
         IR-B detects             │
         train departed     Barrier CLOSED
                            Red LED ON
                            Buzzer ON
```

### State outputs

| State | Barrier | Traffic LED | Buzzer | LCD |
|---|---|---|---|---|
| IDLE | OPEN | GREEN | OFF | CROSSING CLEAR |
| WARNING | OPEN | RED | ON | TRAIN INCOMING! |
| CROSSING | CLOSED | RED | ON | TRAIN CROSSING |
| CLEAR | OPEN | GREEN | OFF | SYSTEM CLEAR |

---

## 🔌 Proteus Circuit Components

| Component | Model | Function |
|---|---|---|
| IR sensor (×2) | TSOP1738 module | Train detection |
| Ultrasonic sensor | HC-SR04 | Pedestrian/vehicle detection |
| Servo motor | SG90 | Barrier arm (0° open, 90° closed) |
| Red LED | LED-RED | Road stop signal |
| Green LED | LED-GREEN | Road go signal |
| Buzzer | BUZZER | Audible warning |
| LCD | LM016L (16×2) | Status display |
| Microcontroller | Arduino UNO (logic host) | Signal routing in Proteus |

---

## 🚀 Running the Python Simulation

```bash
# Clone the repo
git clone https://github.com/your-username/smart-rail-crossing.git
cd smart-rail-crossing

# No dependencies needed — pure Python 3
python rail_crossing.py
```

### Sample output

```
═════════════════════════════════════════════
  SMART RAIL CROSSING SAFETY SYSTEM
  Siemens Mobility — Fit4Rail Project
═════════════════════════════════════════════

  STATE: IDLE
  [BARRIER]  🔓  → OPEN
  [LED]      🟢  → GREEN
  [BUZZER]   OFF 🔕
  [LCD]      ┌─────────────────┐
             │ CROSSING CLEAR  │
             └─────────────────┘

  📍 Scenario: Train detected approaching
  ▶ Transition: IDLE → WARNING
  [LED]      🔴  → RED
  [BUZZER]   ON  🔔
  ...
```

---

## 📁 Repository Structure

```
smart-rail-crossing/
├── rail_crossing.py          # Python FSM simulation
├── proteus/
│   └── rail_crossing.pdsprj  # Proteus schematic & simulation
├── docs/
│   ├── circuit_diagram.pdf   # Exported Proteus schematic
│   └── project_report.pdf    # Full technical report
├── demo/
│   └── demo_video.mp4        # Proteus simulation screen recording
└── README.md
```

---

## 🛡️ Safety Features

- **Pedestrian override**: If the ultrasonic sensor detects an obstacle on the crossing while a train is passing, the barrier remains closed for an additional hold period.
- **Fail-safe default**: On power loss or sensor failure, the system defaults to `CROSSING` state (barriers down, red lights on).
- **Timeout protection**: If IR-B never triggers after `CROSSING_TIMEOUT` seconds, the system logs an alert (extensible to remote notification).

---

## 👤 Author

**Roaa Sameh Mohamed**  
Mechatronics Engineering — Menoufia University, Year 2  
Built for Siemens Mobility Fit4Rail Internship 2026

---

## 📄 License

MIT — free to use, study, and build upon.
