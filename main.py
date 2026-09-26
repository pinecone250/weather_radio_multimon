import time
from alerts.manager import AlertManager

manager = AlertManager()

try:
    #start manager
    manager.start(Testing=False)

    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("Stopping...")

finally:
    manager.stop()
    