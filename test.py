import time
from alerts.manager import AlertManager

manager = AlertManager()

try:
    #start in test mode
    manager.start(Testing=True)

    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("Stopping...")

finally:
    manager.stop()
    