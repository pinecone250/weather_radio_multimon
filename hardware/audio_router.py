"""class AudioRouter:
    def __init__(self, speaker, sdr_stream):
        self.mode = "LISTENING"
        self.speaker = speaker
        self.sdr = sdr_stream

    def to_alert(self):
        self.mode = "ALERT"
        self.sdr.enable()

    def to_listening(self):
        self.mode = "LISTENING"
        self.sdr.enable()
"""





class AudioRouter:
    LISTENING = "LISTENING"
    ALERT = "ALERT"

    def __init__(self):
        self.mode = self.LISTENING

    def to_alert(self):
        self.mode = self.ALERT

    def to_listening(self):
        self.mode = self.LISTENING

    def is_alert(self):
        return self.mode == self.ALERT

    def is_listening(self):
        return self.mode == self.LISTENING