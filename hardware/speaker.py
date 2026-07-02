# hardware/speaker.py

import os
import platform
import subprocess
import threading


class Speaker:
    def __init__(self):
        self.system = platform.system()
        self.process = None

        self.siren_file = "sounds/siren.wav"  # you can switch to mp3 later

        print(f"[SPEAKER] Initialized on {self.system}")

    def play_siren(self):
        """Play siren sound (non-blocking)."""
        thread = threading.Thread(target=self._play, args=(self.siren_file,), daemon=True)
        thread.start()

    def _play(self, file_path):
        if not os.path.exists(file_path):
            print(f"[SPEAKER] File not found: {file_path}")
            return

        # Raspberry Pi / Linux playback
        try:
            # Preferred lightweight CLI player
            self.process = subprocess.Popen(["aplay", file_path])
            self.process.wait()
            self.process = None

        except FileNotFoundError:
            print("[SPEAKER] aplay not found. Install ALSA utils:")
            print("sudo apt install alsa-utils")

    def play_startup(self):
        print("[SPEAKER] Startup sound (not implemented yet)")



    def stop(self):
        if self.process and self.process.poll() is None:
            self.process.terminate()
            self.process.wait()
            self.process = None