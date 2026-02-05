import random
import time
from pathlib import Path

import arcade
import config


class SoundManager:
    def __init__(self):
        base = Path(__file__).resolve().parent.parent / "assets" / "sfx" / "8bit" / "8-Bit Sound Library" / "Wav"
        self.sounds = {
            "shoot": self._load_list(base, ["Shoot_00.wav", "Shoot_01.wav", "Shoot_02.wav", "Shoot_03.wav"]),
            "enemy_attack": self._load_list(base, ["Shoot_00.wav", "Shoot_01.wav", "Shoot_02.wav", "Shoot_03.wav"]),
            "enemy_melee": self._load_list(base, ["Hit_00.wav", "Hit_01.wav", "Hit_02.wav", "Hit_03.wav"]),
            "melee": self._load_list(base, ["Hit_00.wav", "Hit_01.wav", "Hit_02.wav", "Hit_03.wav"]),
            "hit": self._load_list(base, ["Hit_00.wav", "Hit_01.wav", "Hit_02.wav", "Hit_03.wav"]),
            "pickup": self._load_list(base, ["Pickup_00.wav", "Pickup_01.wav", "Pickup_02.wav", "Pickup_03.wav", "Pickup_04.wav"]),
            "open": self._load_list(base, ["Open_00.wav", "Open_01.wav"]),
            "dash": self._load_list(base, ["Jump_00.wav", "Jump_01.wav", "Jump_02.wav", "Jump_03.wav"]),
            "coin": self._load_list(base, ["Collect_Point_00.wav", "Collect_Point_01.wav", "Collect_Point_02.wav"]),
            "death": self._load_list(base, ["Hero_Death_00.wav"]),
        }
        self.last_played = {}
        self.cooldowns = {
            "shoot": 0.05,
            "melee": 0.08,
            "hit": 0.05,
            "pickup": 0.1,
            "open": 0.15,
            "dash": 0.2,
            "coin": 0.08,
            "death": 0.5,
        }
        self.volume = getattr(config, "SFX_VOLUME", 0.5)

    def _load_list(self, base: Path, files: list[str]):
        sounds = []
        for name in files:
            path = base / name
            if path.exists():
                sounds.append(arcade.load_sound(str(path)))
        return sounds

    def play(self, name: str, volume: float | None = None):
        sounds = self.sounds.get(name)
        if not sounds:
            return
        now = time.time()
        cooldown = self.cooldowns.get(name, 0)
        if now - self.last_played.get(name, 0) < cooldown:
            return
        self.last_played[name] = now
        sound = random.choice(sounds)
        arcade.play_sound(sound, volume if volume is not None else self.volume)
