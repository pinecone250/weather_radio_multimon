# hardware/speaker.py

import os
import platform
import subprocess
import threading


class Speaker:
    def __init__(self):
        self.system = platform.system()

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

        # Windows fallback (simulation)
        if self.system == "Windows":
            print(f"[SPEAKER] (SIM) Playing: {file_path}")
            return

        # Raspberry Pi / Linux playback
        try:
            # Preferred lightweight CLI player
            subprocess.run(["aplay", file_path], check=False)

        except FileNotFoundError:
            print("[SPEAKER] aplay not found. Install ALSA utils:")
            print("sudo apt install alsa-utils")

    def play_startup(self):
        print("[SPEAKER] Startup sound (not implemented yet)")