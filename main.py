from hardware.led import LEDController
import time

led = LEDController()

led.start_blink(0.2, 0.2)

time.sleep(3)

led.stop()

time.sleep(1)

led.on()

time.sleep(1)

led.off()



from hardware.button import ButtonController

def on_ack():
    print("[SYSTEM] ALERT ACKNOWLEDGED")

button = ButtonController()

button.on_press(on_ack)

while True:
    pass