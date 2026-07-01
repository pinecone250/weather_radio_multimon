# hardware/button.py

import sys
import threading
from gpiozero import Button


class ButtonController:
    def __init__(self, pin=27):
        self.button = Button(pin)
    
    def on_press(self, callback):
        self.button.when_pressed = callback