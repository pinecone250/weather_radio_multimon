import threading
import time


class LEDController:
    def __init__(self, pin=17):

        self.pin = pin
        self._running = False
        self.is_raspberry_pi = self._detect_pi()

        if self.is_raspberry_pi:
            from gpiozero import LED
            self._led = LED(pin)
            print("[LED] GPIO mode enabled")
        else:
            print("[LED] SIMULATION mode")

    def _detect_pi(self):
        try:
            with open("/proc/device-tree/model") as f:
                return "Raspberry Pi" in f.read()
        except:
            return False

    def start_blink(self, on_time=0.5, off_time=0.5):
        if self._running:
            return

        self._running = True

        def run():
            while self._running:

                if self.is_raspberry_pi:
                    self._led.on()
                    print("[LED] ON")
                #else:
                    print("[LED] ON")

                time.sleep(on_time)

                if self.is_raspberry_pi:
                    self._led.off()
                    #print("[LED] OFF")
                #else:
                    #print("[LED] OFF")

                time.sleep(off_time)

        threading.Thread(target=run, daemon=True).start()

    def stop(self):
        self._running = False

        if self.is_raspberry_pi:
            self._led.off()