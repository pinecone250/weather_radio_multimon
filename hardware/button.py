# hardware/button.py

import sys
import threading


class ButtonController:
    def __init__(self, pin=27):

        self.pin = pin
        self._callback = None
        self._listening = False

        # detect if we're on Raspberry Pi
        self.is_raspberry_pi = self._detect_pi()

        if self.is_raspberry_pi:
            self._setup_gpio()
        else:
            print("[BUTTON] Running in SIMULATION mode")

    def _detect_pi(self):
        try:
            with open("/proc/device-tree/model") as f:
                return "Raspberry Pi" in f.read()
        except:
            return False

    # -------------------------
    # Raspberry Pi mode
    # -------------------------
    def _setup_gpio(self):
        from gpiozero import Button

        self._button = Button(self.pin)
        print("[BUTTON] GPIO mode enabled")

    def on_press(self, callback):
        self._callback = callback

        if self.is_raspberry_pi:
            self._button.when_pressed = callback
        else:
            self._listening = True
            thread = threading.Thread(target=self._simulate_input, daemon=True)
            thread.start()

    # -------------------------
    # Simulation mode (Windows)
    # -------------------------
    def _simulate_input(self):
        while self._listening:
            cmd = input("[BUTTON] Press ENTER (q to quit): ")

            if cmd.lower() == "q":
                break

            print("[BUTTON] PRESSED")
            if self._callback:
                self._callback()

    def stop(self):
        self._listening = False