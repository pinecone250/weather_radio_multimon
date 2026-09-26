import time
import threading
import re

from alerts.states import AlertState
from hardware.speaker import Speaker
from hardware.led import LEDController
from hardware.button import ButtonController
from radio.same_decoder import SAMEDecoder



class AlertManager:
    

    SAME_PATTERN = re.compile(
        r"ZCZC-"
        r"(?P<originator>[A-Z]{3})-"
        r"(?P<event>[A-Z]{3})-"
        r"(?P<locations>\d{6}(?:-\d{6})*)"
        r"\+"
        r"(?P<purge>\d{4})-"
        r"(?P<issued>\d{7})-"
        r"(?P<sender>[A-Z0-9/]+)-"
    )

    def __init__(self):
        self.state = AlertState.IDLE
        self.last_alert_id = None
        self.alert_active = False
        self.lock = threading.Lock()
        self._pending_timer = None

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
    def start(self, Testing: bool = False):
        print("[ALERT MANAGER] Starting system...")

        self.running = True
        self.set_state(AlertState.LISTENING)
        self.button.on_press(self.acknowledge_button)

        self.decoder.on_event(self.handle_decoder_event)
        self.decoder.start(Testing)

        #threading.Thread(target=self._run_loop, daemon=True).start()

    def stop(self):
        print("[ALERT MANAGER] Stopping system...")

        self.running = False
        self.decoder.stop()

        self.speaker.stop()
        self.led.stop()

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
            "originator": match.group("originator"),
            "event": match.group("event"),
            "locations": match.group("locations").split("-"),
            "purge": match.group("purge"),
            "issued": match.group("issued"),
            "sender": match.group("sender"),
            "raw": text
        }

    def _make_alert_id(self, parsed):
        
        #Creates stable deduplication ID.
        
        return f"{parsed['event']}-{parsed['origin']}-{parsed['locations'][0]}"

    # ---------------------------
    # DECODER CALLBACK
    # ---------------------------
    def handle_decoder_event(self, event):

        print("EVENT RECEIVED:", event)
        
        if event ["type"] != "ALERT_HEADER": #alert header is defined as type in same_decoder
            return


        raw_text = event["raw"]

        parsed = self._parse_same(raw_text)
        if not parsed:
            print("Parse failed")
            return

        print("Calling trigger_alert")
        self.trigger_alert(parsed)

        print("reached end")

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

    
    
    
    
    
    
    
    
    
    
    
    
    """
    def _handle_alert_logic(self, parsed):
        if parsed["event"] not in {"TOR", "SVR", "FFW", "EAS", "WXR"}:
            return

        alert_id = self._make_alert_id(parsed)

        if alert_id == self.last_alert_id:
            return

        self.last_alert_id = alert_id

        self.set_state(AlertState.ALERT_ACTIVE)
    """







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
        self.speaker.start_stream()
        self.led.start_blink()

    # ---------------------------
    # USER ACKNOWLEDGE
    # ---------------------------
    def acknowledge(self):
        print("[ALERT] Acknowledged")

        with self.lock:
            self.alert_active = False


        self.set_state(AlertState.ACKED)

        self.speaker.stop()
        self.led.stop()

    # ---------------------------
    # BUTTON LOOP
    # ---------------------------

    def acknowledge_button(self):
        if self.alert_active:
            self.acknowledge()