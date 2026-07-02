from alerts.manager import AlertManager
#from radio.same_decoder import SAMEEvent
import time

manager = AlertManager()

import time

manager.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    manager.stop()
"""
fake = SAMEEvent(
    event_type="SAME_DECODE",
    raw="ZCZC-WXR-TOR-001001-XXXX"
)

manager.handle_decoder_event(fake)

time.sleep(5)

manager.acknowledge()

time.sleep(2)
manager.stop()
"""