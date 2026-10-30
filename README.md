# NOAA Emergency Weather Receiver

A Raspberry Pi-based emergency weather receiver that continuously receives NOAA Weather Radio broadcasts, decodes Specific Area Message Encoding (SAME) alerts, and uses audio and visual indicators to notify users when an alert is received.

## Features

- Continuously receives NOAA Weather Radio broadcasts.
- Decodes SAME emergency alerts.
- Uses audio and visual indicators to notify users of broadcasted alerts.
- Allows users to acknowledge/silence alerts using a physical button.
- Allows users to listen to NOAA broadcast even when no alert is detected.

## Hardware

 - Raspberry Pi 5
 - Nooelec RTL-SDR v5 
 - Wire antenna 
 - Waveshare USB Sound Card and Speakers
 - FILN Momentary Push Button Switch
 - MOSFET driver board

## Software

- **Python** – Main application logic and alert management
- **rtl_fm** – Receives and demodulates radio signals
- **multimon-ng** – Decodes SAME alert messages
- **gpiozero** – Controls GPIO-connected hardware
- **ffmpeg / ffplay** – Handles audio playback and processing
- **aplay** - Audio playback

## How It Works

1. The RTL-SDR receives NOAA Weather Radio broadcasts.
2. `rtl_fm` demodulates the received signal and produces audio.
3. `multimon-ng` monitors the audio for SAME alert messages
4. Python processes decoded alerts and manages the receiver's response, including audio playback, the siren, and visual indicators.
5. Users can interact with alerts using the physical button, or listen to the broadcast directly when no alert is active.
