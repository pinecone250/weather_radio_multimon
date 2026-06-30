# alerts/same_decoder.py

import time
import numpy as np


class SAMEEvent:
    def __init__(self, event_type="UNK", raw=None, strength=None):
        self.event_type = event_type
        self.raw = raw
        self.strength = strength
        self.timestamp = time.time()

    def __repr__(self):
        return f"<SAMEEvent {self.event_type} strength={self.strength:.4f}>"


class SAMEDecoder:
    def __init__(self):
        print("[SAME] DSP Decoder initialized")

        self.buffer = np.array([], dtype=np.int16)

    # -----------------------------
    # MAIN ENTRY POINT
    # -----------------------------
    def analyze_audio(self, audio_chunk):
        """
        Convert rtl_fm bytes → numpy samples → DSP analysis
        """

        if not audio_chunk:
            return None

        # --------------------------------------------------
        # STEP 1: Convert raw PCM bytes → int16 samples
        # --------------------------------------------------
        samples = np.frombuffer(audio_chunk, dtype=np.int16)

        if len(samples) == 0:
            return None

        # --------------------------------------------------
        # STEP 2: Compute signal strength (RMS energy)
        # --------------------------------------------------
        strength = self._compute_rms(samples)

        # --------------------------------------------------
        # STEP 3: Store rolling buffer (future FFT use)
        # --------------------------------------------------
        self.buffer = np.concatenate((self.buffer, samples))

        # keep buffer bounded
        if len(self.buffer) > 200000:
            self.buffer = self.buffer[-200000:]

        # --------------------------------------------------
        # STEP 4: Simple "activity detection"
        # --------------------------------------------------
        if strength > 500:   # threshold (you will tune this)
            return SAMEEvent(
                event_type="AUDIO_ACTIVE",
                raw="rms_trigger",
                strength=strength
            )

        return None

    # -----------------------------
    # DSP UTILITY
    # -----------------------------
    def _compute_rms(self, samples):
        """
        Root Mean Square (signal power)
        """
        return np.sqrt(np.mean(samples.astype(np.float32) ** 2))