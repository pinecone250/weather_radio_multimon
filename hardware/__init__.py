def mute_radio(self):
    if not self.radio_muted:
        subprocess.run(
            ["amixer", "sset", "Speaker", "off"],
            check=False
        )
        self.radio_muted = True
        print("[SPEAKER] Radio audio MUTED")