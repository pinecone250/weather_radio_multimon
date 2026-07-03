import subprocess
import time
from hardware.speaker import Speaker
from radio.same_decoder import SAMEDecoder
from alerts.manager import AlertManager


speaker = Speaker()
speaker.start_stream()

decoder = SAMEDecoder(callback=print)
decoder.start()

manager = AlertManager()  # LED optional for test


# start audio pipeline from .ogg
cmd = [
    "ffmpeg",
    "-i", "/home/project/Flash_flood_warning_Tennessee.ogg",
    "-f", "s16le",
    "-ar", "22050",
    "-ac", "1",
    "-"
]

p = subprocess.Popen(cmd, stdout=subprocess.PIPE)

print("[TEST] Playing .ogg into system...")

# simulate live stream fanout
while True:
    data = p.stdout.read(1024)
    if not data:
        break

    speaker.write(data)
    decoder.write_audio(data)