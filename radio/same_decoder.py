import subprocess
import threading



class SAMEDecoder:
    def __init__(self, callback=None):
        #self.frequency = frequency
        self.callback = callback
        self.process = None
        


    def on_event(self, callback):
        self.callback = callback


    def start(self):
        # Stable NOAA pipeline:
        # rtl_fm → sox (format lock) → multimon-ng
        
        """ Comment out cmd for testing! Remove Later!
        cmd = (
            f"rtl_fm -f {self.frequency} -M fm -s 24000 -r 24000 -E deemp - "
            f"| sox -t raw -r 24000 -e signed -b 16 -c 1 - "
            f"-t raw -r 22050 -e signed -b 16 -c 1 - "
            f"| multimon-ng -t raw -a EAS -"
        )
        """

        #In the future, this command should be run:
        #cmd = ["multimon-ng", "-t", "raw", "-a", "EAS", "-"]

        
        #Start multimon-ng ONLY (no rtl_fm here)
        

        self.process = subprocess.Popen(
            ["multimon-ng", "-t", "raw", "-a", "EAS", "-"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )

        """ For testing 

        cmd = (
            "ffmpeg -i /home/project/Flash_flood_warning_Tennessee.ogg "
            "-f s16le -ar 22050 -ac 1 - | "
            "multimon-ng -t raw -a EAS -"
        )

        self.process = subprocess.Popen(
            ["bash", "-c", cmd],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )

        """

        threading.Thread(target=self._reader, daemon=True).start()


    def write_audio(self, data: bytes):
        """
        Called by SDRReceiver fanout
        """
        if not self.process:
            return

        try:
            self.process.stdin.write(data)
            self.process.stdin.flush()
        except Exception:
            pass

    

    def _reader(self):
        for line in self.process.stdout:
            line = line.strip()

            print("[RAW]", line)

            event = self._parse(line)

            if event and self.callback:
                print("[CALLBACK FIRED]")
                self.callback(event)

    def _parse(self, line: str):
        """
        ONLY converts decoder output → structured events.
        No decision making here.
        """

        if not line:
            return None

        # START of SAME/EAS alert
        if "ZCZC" in line:
            return {
                "type": "ALERT_HEADER",
                "raw": line
            }

        # END of alert
        if "NNNN" in line:
            return {
                "type": "ALERT_END",
                "raw": line
            }

        # Optional: pass-through for debugging
        if "EAS" in line or "WXR" in line:
            return {
                "type": "INFO",
                "raw": line
            }

        return None

    def stop(self):
        if self.process:
            self.process.terminate()