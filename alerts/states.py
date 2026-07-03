# alerts/states.py

from enum import Enum, auto


class AlertState(Enum):
    IDLE = auto()          # normal scanning mode
    LISTENING = auto()     # receiver active (User Listening)
    #ALERT_DETECTED = auto() # SAME header detected
    ALERT_ACTIVE = auto()  # siren + LED active
    ACKED = auto()         # user acknowledged alert
    #SILENCED = auto()      # temporarily muted