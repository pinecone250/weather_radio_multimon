import subprocess
import threading



class SAMEDecoder:
    def __init__(self, frequency="162.550M"):
        self.frequency = frequency
        self.callback = None
        self.process = None


    def on_event(self, callback):
        self.callback = callback


    def start(self, testing=False):
        
        #Comment out cmd for testing! Remove Later!
        
        if self.process is not None:
            print("[DECODER] Already running")
            return

        if testing:
            cmd = (
                "ffmpeg -i /home/project/Flash_flood_warning_Tennessee.ogg "
                "-f s16le -ar 22050 -ac 1 - | "
                "tee >(aplay -D pulse -r 22050 -f S16_LE) | "
                "multimon-ng -t raw -a EAS -"
            )


            """
            cmd = (
                "ffmpeg -i /home/project/Flash_flood_warning_Tennessee.ogg "
                "-f s16le -ar 22050 -ac 1 - | "
                "multimon-ng -t raw -a EAS -"
                
            )
            """
        
        else: cmd = (
            f"rtl_fm -f {self.frequency} "
            f"-M fm -s 22050 -r 22050 -E deemp - | "
            f"tee >(aplay -D pulse -r 22050 -f S16_LE) | "
            f"multimon-ng -t raw -a EAS -"
        )




        """
        else:
            cmd = (
                f"rtl_fm -f {self.frequency} -M fm -s 24000 -r 24000 -E deemp - "
                f"| sox -t raw -r 24000 -e signed -b 16 -c 1 - "
                f"-t raw -r 22050 -e signed -b 16 -c 1 - "
                f"| multimon-ng -t raw -a EAS -"
                
            )
        """

        print("[DECODER] Starting radio pipeline:")
        print(cmd)

        self.process = subprocess.Popen(
            ["bash", "-c", cmd],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )

        threading.Thread(target=self._reader, daemon=True).start()

    def _reader(self):
        for line in self.process.stdout:
            line = line.strip()

            print("[RAW]", line)

            event = self._parse(line)

            if event and self.callback:
                print("[CALLBACK FIRED]")
                self.callback(event)

    def _parse(self, line: str):
        
        #reads terminal output for valid SAME code
        

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