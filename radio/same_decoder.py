# alerts/same_decoder.py

import time


class SAMEEvent:
    def __init__(self, event_type="UNKNOWN", message=""):
        self.event_type = event_type  # e.g. SVR, FFW, TST
        self.message = message
        self.timestamp = time.time()

    def __repr__(self):
        return f"<SAMEEvent {self.event_type} at {self.timestamp}>"


class SAMEDecoder:
    def __init__(self):
        print("[SAME] Decoder initialized")

    def analyze_audio(self, audio_chunk):
        #Placeholder function.
        #Later: real DSP / tone detection.
        

        # TEMP SIMULATION RULE
        # (you will replace this later with real signal processing)

        if b"ALERT" in audio_chunk:
            return SAMEEvent(event_type="SVR", message="Simulated Alert")

        return None