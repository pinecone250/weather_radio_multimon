# hardware/speaker.py

import os
import platform
import subprocess
import threading
import signal


class Speaker:
    def __init__(self, frequency="162.550M"):
        self.system = platform.system()
        self.siren_process = None
        self.stream_process = None
        self.frequency = frequency
        self.radio_muted = False

        self.siren_file = "sounds/siren.wav"

        print(f"[SPEAKER] Initialized on {self.system}")

    """
    def toggle_radio(self):
        subprocess.run(
            ["amixer", "sset", "Speaker", "toggle"],
            check=False
        )

        self.radio_muted = not self.radio_muted

        print(
            f"[SPEAKER] Radio audio "
            f"{'MUTED' if self.radio_muted else 'UNMUTED'}"
        )

    """

    def toggle_radio(self):
        if self.radio_muted:
            subprocess.run(
                ["amixer", "sset", "Speaker", "on"],
                check=False
            )
            self.radio_muted = False
            print("[SPEAKER] Radio audio UNMUTED")
        else:
            subprocess.run(
                ["amixer", "sset", "Speaker", "off"],
                check=False
            )
            self.radio_muted = True
            print("[SPEAKER] Radio audio MUTED")

    def mute_radio(self): 
        subprocess.run( 
            ["amixer", "sset", "Speaker", "off"],
             check=False 
        ) 
        self.radio_muted = True
        print("[SPEAKER] Radio audio MUTED")


    def unmute_radio(self):
        if self.radio_muted:
            self.toggle_radio()



    """
    def play_siren(self):
        #Play siren sound (non-blocking).
        thread = threading.Thread(target=self._play, args=(self.siren_file,), daemon=True)
        thread.start()
    """

    def play_siren(self):
        self._play(self.siren_file)

    def _play(self, file_path):
        if not os.path.exists(file_path):
            print(f"[SPEAKER] File not found: {file_path}")
            return

        # Raspberry Pi / Linux playback
        try:
            self.siren_process = subprocess.Popen(
            [
                "ffplay",
                "-nodisp",
                "-autoexit",
                #"-loglevel", "quiet",
                file_path
            ]
        )

            
            # Preferred lightweight CLI player
            #self.siren_process = subprocess.Popen(["aplay", file_path])
            self.siren_process.wait()
            self.siren_process = None
            

        except FileNotFoundError:
            print("[SPEAKER] ffplay not found.")
            


    def start_stream(self):
        print("[SPEAKER] Stream is provided by SAMEDecoder")
        
        """
        #Starts a new rtl_fm -> aplay pipeline.
        #Safe to call multiple times.
        
        if self.stream_process is not None:
            print("self.stream_process is not None")
            return


        #cmd = (
        #    f"rtl_fm -f {self.frequency} -M fm -s 22050 -r 22050 -E deemp - "
        #    f"| aplay -r 22050 -f S16_LE"
        #)

        cmd = (
            f"rtl_fm -f {self.frequency} -M fm -s 22050 -r 22050 -E deemp - "
            f"| aplay -D plug:default -r 22050 -f S16_LE"
        )

        print(f"[SPEAKER] Starting: {cmd}")

        self.stream_process = subprocess.Popen(
            ["bash", "-c", cmd],
            preexec_fn=os.setsid,
            #stdout=subprocess.DEVNULL,
            #stderr=subprocess.DEVNULL,
        )

        print("[SPEAKER] Broadcast stream started")
        """


    def stop_stream(self):
        print("[SPEAKER] Stream is managed by SAMEDecoder")

        """
        Stops the rtl_fm -> aplay pipeline.
        
        if self.stream_process is None:
            return

        try:
            os.killpg(os.getpgid(self.stream_process.pid), signal.SIGTERM)
            self.stream_process.wait(timeout=2)
        except Exception as e:
            print(f"[SPEAKER] Error stopping stream: {e}")

        self.stream_process = None

        print("[SPEAKER] Broadcast stream stopped")
        """


    def stop(self):
        self.stop_stream()

        if self.siren_process and self.siren_process.poll() is None:
            self.siren_process.terminate()
            self.siren_process.wait()
            self.siren_process = None