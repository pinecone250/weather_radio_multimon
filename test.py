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
    