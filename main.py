from alerts.same_decoder import SAMEDecoder


def handle_event(event):
    print("ALERT:", event.raw)
    # later:
    # alert_manager.process(event)
    # led.flash()
    # speaker.play_siren()


decoder = SAMEDecoder()
decoder.on_event(handle_event)
decoder.start()

while True:
    pass