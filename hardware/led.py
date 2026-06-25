# hardware/led.py

import threading
import time


class LEDController:
    def __init__(self, pin=17):
        # pin kept for Raspberry Pi compatibility later
        self.pin = pin

        self._running = False
        self._thread = None

        self.state = False  # simulated LED state

    def start_blink(self, on_time=0.5, off_time=0.5):
        """Start blinking LED in background thread."""

        if self._running:
            return  # already blinking

        self._running = True

        def run():
            print("[LED] blink started")

            while self._running:
                self._set_state(True)
                time.sleep(on_time)

                self._set_state(False)
                time.sleep(off_time)

            self._set_state(False)
            print("[LED] blink stopped")

        self._thread = threading.Thread(target=run, daemon=True)
        self._thread.start()

    def stop(self):
        """Stop blinking and turn LED off."""
        self._running = False

    def on(self):
        self._running = False
        self._set_state(True)

    def off(self):
        self._running = False
        self._set_state(False)

    def _set_state(self, value: bool):
        self.state = value

        if value:
            print("[LED] ON")
        else:
            print("[LED] OFF")