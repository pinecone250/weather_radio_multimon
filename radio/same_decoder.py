# alerts/same_decoder.py

import time


class SAMEEvent:
    def __init__(self, event_type="UNK", raw=None):
        self.event_type = event_type  # SVR, FFW, TST, etc.
        self.raw = raw
        self.timestamp = time.time()

    def __repr__(self):
        return f"<SAMEEvent {self.event_type}>"


class SAMEDecoder:
    def __init__(self):
        print("[SAME] Decoder initialized")

        # simple rolling buffer for future DSP upgrades
        self.buffer = bytearray()

    # -----------------------------
    # MAIN ENTRY POINT
    # -----------------------------
    def analyze_audio(self, audio_chunk):
        """
        Takes raw PCM audio from rtl_fm
        Returns SAMEEvent or None
        """

        if not audio_chunk:
            return None

        # store recent audio (for future FFT / DSP work)
        self.buffer.extend(audio_chunk)

        # keep buffer bounded (important!)
        if len(self.buffer) > 200000:
            self.buffer = self.buffer[-200000:]

        # -----------------------------
        # PHASE 1: SIMPLE HEURISTIC DETECTION
        # -----------------------------
        if self._detect_simple_pattern(audio_chunk):
            return SAMEEvent(event_type="SVR", raw="simulated detection")

        return None

    # -----------------------------
    # SIMPLE DETECTOR (TEMP)
    # -----------------------------
    def _detect_simple_pattern(self, chunk):
        """
        Temporary logic:
        NOT real SAME decoding yet.

        This will later become:
        - FFT analysis
        - tone detection (1050 Hz / FSK patterns)
        """

        # fake trigger for testing pipeline
        # replace later with real DSP logic
        return b"\xAA\xAA" in chunk