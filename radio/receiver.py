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
import os
import signal


class SDRReceiver:
    def __init__(self, frequency=162.550e6):
        self.frequency = frequency
        self.rtl_process = None
        self.aplay_process = None
        self.running = False
        self.muted = False

    def start(self):
        if self.running:
            return

        print("[SDR] Starting rtl_fm pipeline...")

        rtl_cmd = [
            "rtl_fm",
            "-f", str(self.frequency),
            "-M", "fm",
            "-s", "22050",
            "-r", "22050"
        ]

        # Start rtl_fm
        self.rtl_process = subprocess.Popen(
            rtl_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            preexec_fn=os.setsid
        )

        # Audio output via aplay
        self.aplay_process = subprocess.Popen(
            ["aplay", "-r", "22050", "-f", "S16_LE"],
            stdin=self.rtl_process.stdout,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        self.running = True

    def mute(self):
        """Instant silence without stopping rtl_fm"""
        if self.aplay_process:
            self.aplay_process.terminate()
            self.aplay_process = None

        self.muted = True

    def unmute(self):
        """Restore audio instantly"""
        if not self.running or not self.muted:
            return

        print("[SDR] Unmuting audio...")

        self.aplay_process = subprocess.Popen(
            ["aplay", "-r", "22050", "-f", "S16_LE"],
            stdin=self.rtl_process.stdout,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        self.muted = False

    def stop(self):
        print("[SDR] Stopping...")

        try:
            if self.aplay_process:
                self.aplay_process.terminate()

            if self.rtl_process:
                os.killpg(os.getpgid(self.rtl_process.pid), signal.SIGTERM)

        finally:
            self.running = False
            self.muted = False