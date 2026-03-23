"""
Smart Rail Crossing Safety System
Author: Roaa Sameh Mohamed | Siemens Mobility Fit4Rail Portfolio Project
Description: Python simulation of an automated level crossing safety system.
             Models sensor input, a 4-state finite state machine, and output
             control signals (barrier, LEDs, buzzer, LCD).
"""

import time
import random

# ─────────────────────────────────────────────
#  SYSTEM CONSTANTS
# ─────────────────────────────────────────────
WARNING_DURATION   = 3   # seconds buzzer sounds before barrier drops
CROSSING_TIMEOUT   = 10  # max seconds a train can occupy the crossing
CLEAR_HOLD         = 2   # seconds to hold CLEAR state before returning to IDLE

# ─────────────────────────────────────────────
#  STATES
# ─────────────────────────────────────────────
IDLE     = "IDLE"
WARNING  = "WARNING"
CROSSING = "CROSSING"
CLEAR    = "CLEAR"

# ─────────────────────────────────────────────
#  OUTPUT SIGNALS  (simulated — maps to Proteus components)
# ─────────────────────────────────────────────
class OutputController:
    """Simulates the physical output layer of the crossing system."""

    def set_barrier(self, position: str):
        """position: 'OPEN' (0°) or 'CLOSED' (90°) — servo motor command."""
        symbol = "🔓" if position == "OPEN" else "🔒"
        print(f"  [BARRIER]  {symbol}  → {position}")

    def set_traffic_led(self, color: str):
        """color: 'GREEN' or 'RED' — road signal LEDs."""
        symbol = "🟢" if color == "GREEN" else "🔴"
        print(f"  [LED]      {symbol}  → {color}")

    def set_buzzer(self, active: bool):
        """Audible pedestrian/vehicle alert."""
        state = "ON  🔔" if active else "OFF 🔕"
        print(f"  [BUZZER]   {state}")

    def set_lcd(self, message: str):
        """16×2 LCD status display."""
        print(f"  [LCD]      ┌─────────────────┐")
        print(f"             │ {message:<17}│")
        print(f"             └─────────────────┘")


# ─────────────────────────────────────────────
#  SENSOR SIMULATOR
# ─────────────────────────────────────────────
class SensorArray:
    """
    Simulates three sensors:
      - ir_entry    : IR sensor A — detects train approaching the crossing
      - ir_exit     : IR sensor B — detects train clearing the crossing
      - ultrasonic  : detects pedestrian or vehicle on the crossing
    """

    def __init__(self):
        self.ir_entry   = False
        self.ir_exit    = False
        self.ultrasonic = False

    def simulate_train_approach(self):
        self.ir_entry   = True
        self.ir_exit    = False
        self.ultrasonic = False

    def simulate_train_crossing(self):
        self.ir_entry   = False
        self.ir_exit    = False
        self.ultrasonic = random.choice([True, False])  # pedestrian may be present

    def simulate_train_departed(self):
        self.ir_entry   = False
        self.ir_exit    = True
        self.ultrasonic = False

    def simulate_idle(self):
        self.ir_entry   = False
        self.ir_exit    = False
        self.ultrasonic = False

    def read(self) -> dict:
        return {
            "ir_entry":   self.ir_entry,
            "ir_exit":    self.ir_exit,
            "ultrasonic": self.ultrasonic,
        }


# ─────────────────────────────────────────────
#  FINITE STATE MACHINE
# ─────────────────────────────────────────────
class RailCrossingFSM:
    """
    4-state Finite State Machine for level crossing control.

    Transitions:
      IDLE     → WARNING   : IR sensor A detects incoming train
      WARNING  → CROSSING  : After WARNING_DURATION seconds (barrier drops)
      CROSSING → CLEAR     : IR sensor B detects train has passed
      CLEAR    → IDLE      : After CLEAR_HOLD seconds (system resets)
    """

    def __init__(self):
        self.state   = IDLE
        self.outputs = OutputController()
        self.sensors = SensorArray()
        self._apply_state_outputs()

    # ── State entry actions ──────────────────
    def _apply_state_outputs(self):
        print(f"\n{'═'*45}")
        print(f"  STATE: {self.state}")
        print(f"{'─'*45}")

        if self.state == IDLE:
            self.outputs.set_barrier("OPEN")
            self.outputs.set_traffic_led("GREEN")
            self.outputs.set_buzzer(False)
            self.outputs.set_lcd("CROSSING CLEAR ")

        elif self.state == WARNING:
            self.outputs.set_barrier("OPEN")      # barrier still open during warning
            self.outputs.set_traffic_led("RED")
            self.outputs.set_buzzer(True)
            self.outputs.set_lcd("TRAIN INCOMING!")

        elif self.state == CROSSING:
            self.outputs.set_barrier("CLOSED")
            self.outputs.set_traffic_led("RED")
            self.outputs.set_buzzer(True)
            self.outputs.set_lcd("TRAIN CROSSING ")

        elif self.state == CLEAR:
            self.outputs.set_barrier("OPEN")
            self.outputs.set_traffic_led("GREEN")
            self.outputs.set_buzzer(False)
            self.outputs.set_lcd("SYSTEM CLEAR   ")

    # ── Transition logic ─────────────────────
    def transition(self, new_state: str):
        print(f"\n  ▶ Transition: {self.state} → {new_state}")
        self.state = new_state
        self._apply_state_outputs()

    # ── Main update loop ─────────────────────
    def update(self, sensor_data: dict):
        ir_entry   = sensor_data["ir_entry"]
        ir_exit    = sensor_data["ir_exit"]
        ultrasonic = sensor_data["ultrasonic"]

        if self.state == IDLE and ir_entry:
            self.transition(WARNING)

        elif self.state == WARNING:
            print(f"  ⏳ Waiting {WARNING_DURATION}s before dropping barrier...")
            time.sleep(WARNING_DURATION)
            self.transition(CROSSING)

        elif self.state == CROSSING and ir_exit:
            if ultrasonic:
                print("  ⚠️  Pedestrian/vehicle detected — holding barrier closed!")
                time.sleep(2)   # extra safety hold
            self.transition(CLEAR)

        elif self.state == CLEAR:
            print(f"  ⏳ Holding CLEAR state for {CLEAR_HOLD}s...")
            time.sleep(CLEAR_HOLD)
            self.transition(IDLE)

    def safety_check(self, sensor_data: dict):
        """Override: if ultrasonic detects obstacle while in CROSSING, extend hold."""
        if self.state == CROSSING and sensor_data["ultrasonic"]:
            print("  🚨 SAFETY OVERRIDE — obstacle detected in crossing zone!")
            self.outputs.set_lcd("OBSTCL DETECTED")
            time.sleep(2)


# ─────────────────────────────────────────────
#  SIMULATION RUNNER
# ─────────────────────────────────────────────
def run_simulation():
    print("\n" + "═"*45)
    print("  SMART RAIL CROSSING SAFETY SYSTEM")
    print("  Siemens Mobility — Fit4Rail Project")
    print("  Simulation Mode — Python FSM")
    print("═"*45)

    fsm = RailCrossingFSM()
    sensors = fsm.sensors

    # Simulate one complete train event cycle
    scenarios = [
        ("System idle — no train", sensors.simulate_idle),
        ("Train detected approaching", sensors.simulate_train_approach),
        ("Train on crossing", sensors.simulate_train_crossing),
        ("Train departed crossing", sensors.simulate_train_departed),
        ("System resets", sensors.simulate_idle),
    ]

    for description, scenario_fn in scenarios:
        print(f"\n\n  📍 Scenario: {description}")
        scenario_fn()
        sensor_data = sensors.read()
        print(f"  Sensors → IR-Entry:{sensor_data['ir_entry']} | "
              f"IR-Exit:{sensor_data['ir_exit']} | "
              f"Ultrasonic:{sensor_data['ultrasonic']}")
        fsm.safety_check(sensor_data)
        fsm.update(sensor_data)
        time.sleep(1)

    print("\n\n" + "═"*45)
    print("  ✅ Simulation complete — all states exercised.")
    print("═"*45 + "\n")


if __name__ == "__main__":
    run_simulation()
