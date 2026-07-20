import time
from alerts.manager import AlertManager

manager = AlertManager()

try:
    manager.start()

    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("Stopping...")

finally:
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