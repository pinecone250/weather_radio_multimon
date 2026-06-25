# hardware/button.py

import threading
import time


class ButtonController:
    def __init__(self, pin=27):
        self.pin = pin  # for future Raspberry Pi use

        self._callback = None
        self._listening = False

    def on_press(self, callback):
        """
        Register function to call when button is "pressed"
        """
        self._callback = callback
        self._listening = True

        print("[BUTTON] Listening for press events (simulated)")

        # Start background simulation thread
        thread = threading.Thread(target=self._simulate_input, daemon=True)
        thread.start()

    def _simulate_input(self):
        """
        Windows simulation:
        user types ENTER to simulate button press
        """
        while self._listening:
            cmd = input("[BUTTON] Press ENTER to simulate press (or 'q'): ")

            if cmd.lower() == "q":
                print("[BUTTON] Stopped listening")
                break

            if self._callback:
                print("[BUTTON] PRESSED")
                self._callback()

    def stop(self):
        """Stop listening for button presses"""
        self._listening = False