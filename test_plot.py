import subprocess
import numpy as np
import matplotlib.pyplot as plt

# Start rtl_fm
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

print("Reading audio...")

# Read a chunk
audio_chunk = process.stdout.read(44100)  # ~2 seconds of audio

# Convert to samples
samples = np.frombuffer(audio_chunk, dtype=np.int16)

# Plot waveform
plt.plot(samples)
plt.title("NOAA SDR Audio Waveform")
plt.xlabel("Sample")
plt.ylabel("Amplitude")
plt.show()