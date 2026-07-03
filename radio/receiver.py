"""
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
        #Start NOAA FM reception

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

        self.running = True


    def read_audio(self, chunk_size=4096):
        
        #Returns raw audio bytes from rtl_fm stream
        
        if self.process and self.process.stdout:
            return self.process.stdout.read(chunk_size)
        return None

    def stop(self):
        #Stop NOAA reception
        if not self.running:
            return

        print("[RECEIVER] Stopping stream...")

        try:
            os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)
        except Exception as e:
            print(f"[RECEIVER] Stop error: {e}")

        self.running = False

"""

import subprocess
import threading
import os
import signal


class SDRReceiver:
    def __init__(self, frequency=162.550e6, decoder=None, speaker=None):
        self.frequency = frequency
        self.decoder = decoder      # SAMEDecoder instance
        self.speaker = speaker      # Speaker controller (optional wrapper)
        self.rtl_process = None
        self.running = False

        print(f"[SDR] Initialized at {self.frequency/1e6:.3f} MHz")

    def start(self):
        if self.running:
            return

        print("[SDR] Starting rtl_fm...")

        self.rtl_process = subprocess.Popen(
            [
                "rtl_fm",
                "-f", str(self.frequency),
                "-M", "fm",
                "-s", "22050",
                "-r", "22050"
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            preexec_fn=os.setsid
        )

        self.running = True

        threading.Thread(target=self._fanout, daemon=True).start()

    def _fanout(self):
        """
        Single audio source → duplicated to:
        - Speaker (aplay)
        - SAMEDecoder (multimon-ng)
        """
        while self.running:
            data = self.rtl_process.stdout.read(1024)
            if not data:
                continue

            # ---- send to speaker ----
            if self.speaker:
                try:
                    self.speaker.write(data)
                except Exception:
                    pass

            # ---- send to SAME decoder ----
            if self.decoder:
                try:
                    self.decoder.write_audio(data)
                except Exception:
                    pass

    def stop(self):
        print("[SDR] Stopping...")

        self.running = False

        try:
            if self.rtl_process:
                os.killpg(os.getpgid(self.rtl_process.pid), signal.SIGTERM)
        except Exception as e:
            print(f"[SDR] Stop error: {e}")