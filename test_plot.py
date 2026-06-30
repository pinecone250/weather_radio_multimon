import subprocess
import numpy as np
import matplotlib.pyplot as plt

cmd = [
    "rtl_fm",
    "-f", "162.550e6",
    "-M", "fm",
    "-s", "22050",
    "-r", "22050"
]

process = subprocess.Popen(
    cmd,
    stdout=subprocess.PIPE,
    stderr=subprocess.DEVNULL
)

print("Reading SDR audio...")

audio_chunk = process.stdout.read(44100)

samples = np.frombuffer(audio_chunk, dtype=np.int16)

plt.plot(samples[:2000])
plt.title("NOAA SDR Waveform (SSH Pi)")

plt.savefig("waveform.png")
print("Saved waveform.png")