# radio/receiver.py

import subprocess
import threading
import signal
import os


class SDRReceiver:
    def __init__(self, frequency=162.550e6):
        self.frequency = frequency
        self.process = None
        self.running = False

        print(f"[RECEIVER] Initialized at {self.frequency/1e6:.3f} MHz")

    def start(self):
        """Start NOAA FM reception"""

        if self.running:
            print("[RECEIVER] Already running")
            return

        cmd = [
            "rtl_fm",
            "-f", str(self.frequency),
            "-M", "fm",
            "-s", "22050",
            "-r", "22050"
        ]

        print("[RECEIVER] Starting stream...")

        self.process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            preexec_fn=os.setsid  # lets us kill the whole process group
        )

        # Pipe audio to speaker in background
        self.audio_thread = threading.Thread(target=self._play_audio, daemon=True)
        self.audio_thread.start()

        self.running = True

    def _play_audio(self):
        """Send rtl_fm output to speaker"""
        subprocess.run(
            ["aplay", "-r", "22050", "-f", "S16_LE"],
            stdin=self.process.stdout
        )

    def stop(self):
        """Stop NOAA reception"""
        if not self.running:
            return

        print("[RECEIVER] Stopping stream...")

        try:
            os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)
        except Exception as e:
            print(f"[RECEIVER] Stop error: {e}")

        self.running = False