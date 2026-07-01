import subprocess
import threading
import time


class SAMEEvent:
    def __init__(self, event_type="SAME", raw=""):
        self.event_type = event_type
        self.raw = raw
        self.timestamp = time.time()

    def __repr__(self):
        return f"<SAMEEvent {self.event_type}: {self.raw}>"


class SAMEDecoder:
    def __init__(self, frequency=162.550):
        self.frequency = frequency
        self.process = None
        self.running = False
        self.callbacks = []

    # -------------------------
    # START PIPELINE
    # -------------------------
    def start(self):
        cmd = (
            f"rtl_fm -f {self.frequency}M "
            "-M fm -s 240k -r 22050 -g 20 -E deemp - | "
            "multimon-ng -t raw -a AFSK1200 -a EAS -"
        )

        self.process = subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )

        self.running = True

        threading.Thread(target=self._read_loop, daemon=True).start()

    # -------------------------
    # READ OUTPUT LOOP
    # -------------------------
    def _read_loop(self):
        print("[SAME] Listening for alerts...")

        while self.running and self.process:
            line = self.process.stdout.readline()

            if not line:
                continue

            line = line.strip()

            if self._is_valid_same_line(line):
                event = SAMEEvent(
                    event_type="SAME_DECODE",
                    raw=line
                )
                self._emit(event)

    # -------------------------
    # FILTER VALID OUTPUT
    # -------------------------
    def _is_valid_same_line(self, line):
        return (
            "ZCZC" in line or
            "EAS" in line or
            "WXR" in line or
            "TOR" in line or
            "SVR" in line or
            "FFW" in line
        )

    # -------------------------
    # EVENT SYSTEM
    # -------------------------
    def on_event(self, callback):
        self.callbacks.append(callback)

    def _emit(self, event):
        for cb in self.callbacks:
            try:
                cb(event)
            except Exception as e:
                print(f"[SAME] Callback error: {e}")

    # -------------------------
    # STOP CLEANLY
    # -------------------------
    def stop(self):
        self.running = False

        if self.process:
            try:
                self.process.terminate()
                self.process.wait(timeout=2)
            except Exception:
                self.process.kill()

        self.process = None