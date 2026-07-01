import time
import threading
import re

from alerts.states import AlertState
from hardware.speaker import Speaker
from hardware.led import LEDController
from hardware.button import ButtonController
from radio.same_decoder import SAMEDecoder
from hardware.audio_router import AudioRouter


class AlertManager:
    """
    Production-style NOAA alert controller.

    Responsibilities:
    - Receive decoded multimon-ng output
    - Parse SAME headers
    - Manage alert state machine
    - Trigger hardware safely
    """

    SAME_PATTERN = re.compile(
    r"ZCZC-(?P<prefix>[A-Z]{3})-(?P<event>[A-Z]{3})-(?P<locations>[A-Z0-9,]+)-(?P<origin>[A-Z0-9]{4})"
    )

    def __init__(self):
        self.state = AlertState.IDLE
        self.last_alert_id = None
        self.alert_active = False
        self.lock = threading.Lock()
        self._pending_timer = None
        self.audio_router = AudioRouter()

        # hardware
        self.speaker = Speaker()
        self.led = LEDController()
        self.button = ButtonController()

        # decoder (event-driven)
        self.decoder = SAMEDecoder()

        self.running = False

        print("[ALERT MANAGER] Initialized")

    # ---------------------------
    # START / STOP
    # ---------------------------
    def start(self):
        print("[ALERT MANAGER] Starting system...")

        self.running = True
        self.set_state(AlertState.LISTENING)
        self.button.on_press(self.acknowledge_button)

        self.decoder.on_event(self.handle_decoder_event)
        self.decoder.start()

        #threading.Thread(target=self._run_loop, daemon=True).start()

    def stop(self):
        print("[ALERT MANAGER] Stopping system...")

        self.running = False
        self.decoder.stop()

        self.speaker.stop()
        self.led.off()

        self.set_state(AlertState.IDLE)

    # ---------------------------
    # STATE MACHINE
    # ---------------------------
    def set_state(self, new_state):
        if self.state != new_state:
            print(f"[STATE] {self.state.name} → {new_state.name}")
            self.state = new_state

    # ---------------------------
    # SAME PARSING
    # ---------------------------
    def _parse_same(self, text):
        """
        Extract structured SAME header info.
        Returns dict or None.
        """
        match = self.SAME_PATTERN.search(text)
        if not match:
            return None

        return {
            "prefix": match.group("prefix"),
            "event": match.group("event"),
            "locations": match.group("locations").split("-"),
            "origin": match.group("origin"),
            "raw": text
        }

    #def _is_valid_same(self, text):
        #return text.startswith("ZCZC")

    def _make_alert_id(self, parsed):
        """
        Creates stable deduplication ID.
        """
        return f"{parsed['event']}-{parsed['origin']}-{parsed['locations'][0]}"

    # ---------------------------
    # DECODER CALLBACK
    # ---------------------------
    def handle_decoder_event(self, event):
        
        if event ["type"] != "ALERT_HEADER": #alert header is defined as type in same_decoder
            return


        raw_text = event["raw"]

        parsed = self._parse_same(raw_text)
        if not parsed:
            return

        """
        # hazard filter (IMPORTANT)
        if parsed["event"] not in {"TOR", "SVR", "FFW", "EAS", "WXR"}:
            return

        alert_id = self._make_alert_id(parsed)

        if alert_id == self.last_alert_id:
            return

        self.last_alert_id = alert_id

        print(f"[DECODED] EVENT={parsed['event']} LOC={parsed['locations']}")

        self.set_state(AlertState.ALERT_DETECTED)

        # cancel previous pending trigger
        if self._pending_timer:
            self._pending_timer.cancel()

        self._pending_timer = threading.Timer(
            0.3,
            self.trigger_alert,
            args=[parsed]
        )
        self._pending_timer.start()
        """

    def _handle_alert_logic(self, parsed):
        if parsed["event"] not in {"TOR", "SVR", "FFW", "EAS", "WXR"}:
            return

        alert_id = self._make_alert_id(parsed)

        if alert_id == self.last_alert_id:
            return

        self.last_alert_id = alert_id

        self.set_state(AlertState.ALERT_ACTIVE)







    # ---------------------------
    # ALERT EXECUTION
    # ---------------------------
    def trigger_alert(self, parsed):
        with self.lock:
            if self.alert_active:
                return

            self.alert_active = True

        print(f"[ALERT] ACTIVE → {parsed['event']} {parsed['locations']}")

        self.set_state(AlertState.ALERT_ACTIVE)

        self.speaker.play_siren()
        self.led.start_blink()
        self.audio_router.to_alert()

    # ---------------------------
    # USER ACKNOWLEDGE
    # ---------------------------
    def acknowledge(self):
        print("[ALERT] Acknowledged")

        with self.lock:
            self.alert_active = False


        self.set_state(AlertState.ACKED)

        self.speaker.stop()
        self.led.off()

        self.audio_router.to_listening()

    # ---------------------------
    # BUTTON LOOP
    # ---------------------------
    """def _run_loop(self):
        print("[ALERT MANAGER] Loop started")

        while self.running:
            

            time.sleep(0.1)

        print("[ALERT MANAGER] Loop stopped")
        """

    def acknowledge_button(self):
        if self.alert_active:
            self.acknowledge()