# hardware/speaker.py


"""
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
        #Play siren sound (non-blocking).
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

"""

import os
import platform
import subprocess
import threading


class Speaker:
    def __init__(self):
        self.system = platform.system()
        self.stream_process = None
        self.siren_process = None
        self.muted = True

        self.siren_file = "sounds/siren.wav"

        print(f"[SPEAKER] Initialized on {self.system}")

    # ---------------------------
    # LIVE AUDIO STREAM (rtl_fm)
    # ---------------------------
    def start_stream(self):
        """
        Called by SDRReceiver fanout via stdin pipe
        """
        if self.stream_process:
            return

        self.stream_process = subprocess.Popen(
            ["aplay", "-r", "22050", "-f", "S16_LE"],
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

    def write(self, data: bytes):
        """
        Continuous audio from SDRReceiver
        """
        if self.muted or not self.stream_process:
            return

        try:
            self.stream_process.stdin.write(data)
            self.stream_process.stdin.flush()
        except Exception:
            pass

    # ---------------------------
    # ALERT SOUNDS (siren etc.)
    # ---------------------------
    def play_siren(self):
        threading.Thread(target=self._play_file, args=(self.siren_file,), daemon=True).start()

    def _play_file(self):
        if not os.path.exists(self.siren_file):
            print(f"[SPEAKER] Missing file: {self.siren_file}")
            return

        try:
            self.siren_process = subprocess.Popen(["aplay", self.siren_file])
            self.siren_process.wait()
            self.siren_process = None
        except Exception as e:
            print(f"[SPEAKER] Error playing siren: {e}")

    def stop_stream(self):
        if self.stream_process:
            self.stream_process.terminate()
            self.stream_process = None

    def stop(self):
        self.stop_stream()

        if self.siren_process and self.siren_process.poll() is None:
            self.siren_process.terminate()
            self.siren_process = None

        if self.siren_process and self.siren_process.poll() is None:
            self.siren_process.terminate()
            self.siren_process = None



    def mute_stream(self):
        self.muted = True
        print("[SPEAKER] Stream muted")

    def unmute_stream(self):
        self.muted = False
        print("[SPEAKER] Stream unmuted")