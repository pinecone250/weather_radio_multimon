# alerts/manager.py

import time
import threading

from alerts.states import AlertState
from radio.receiver import SDRReceiver
from hardware.speaker import Speaker
from hardware.led import LEDController
from hardware.button import ButtonController


class AlertManager:
    def __init__(self):
        # Core system state
        self.state = AlertState.IDLE

        # Hardware + radio
        self.receiver = SDRReceiver()
        self.speaker = Speaker()
        self.led = LEDController()
        self.button = ButtonController()

        self.running = False

        print("[ALERT MANAGER] Initialized")

    # ---------------------------
    # SYSTEM CONTROL
    # ---------------------------

    def start(self):
        #Boot the weather radio system.
        print("[ALERT MANAGER] Starting system...")

        self.running = True
        self.set_state(AlertState.LISTENING)

        self.receiver.start()

        # background loop (future: SAME detection, etc.)
        threading.Thread(target=self._run_loop, daemon=True).start()

    def stop(self):
        #Shutdown system safely.
        print("[ALERT MANAGER] Stopping system...")

        self.running = False
        self.receiver.stop()
        self.led.off()

        self.set_state(AlertState.IDLE)

    # ---------------------------
    # STATE HANDLING
    # ---------------------------

    def set_state(self, new_state):
        print(f"[STATE] {self.state.name} → {new_state.name}")
        self.state = new_state

    # ---------------------------
    # EVENT HANDLERS (SIMPLIFIED)
    # ---------------------------

    def trigger_alert(self):
        #Simulated alert trigger (later from SAME decoder).
        print("[ALERT] Triggered!")

        self.set_state(AlertState.ALERT_ACTIVE)

        self.speaker.play_siren()
        self.led.blink()

    def acknowledge(self):
        #User pressed button.#
        print("[ALERT] Acknowledged")

        self.set_state(AlertState.ACKED)

        self.speaker.stop()   # optional later
        self.led.off()

    # ---------------------------
    # MAIN LOOP
    # ---------------------------

    def _run_loop(self):
        """Background system loop."""
        print("[ALERT MANAGER] Loop started")

        while self.running:
            # Placeholder for future logic:
            # - SAME detection
            # - audio monitoring
            # - alert parsing

            time.sleep(1)

        print("[ALERT MANAGER] Loop stopped")