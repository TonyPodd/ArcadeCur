import arcade
import random
from math import atan2, cos, sin, degrees, radians, hypot

import config
from .enemy import Enemy
from .bullet import Bullet


class Boss(Enemy):
    def __init__(self, x: float, y: float, difficulty: float = 1.0):
        super().__init__(x, y, type="boss", difficulty=difficulty)
        self.max_hp = self.hp
        self.phase = 1
        self.pattern_timer = 0.0
        self.last_pattern = None
        self.pattern_cooldown = 1.4
        self.orbit_dir = 1

    def update_phase(self):
        hp_ratio = self.hp / max(self.max_hp_value(), 1)
        if hp_ratio > 0.65:
            self.phase = 1
            self.pattern_cooldown = 1.4
        elif hp_ratio > 0.35:
            self.phase = 2
            self.pattern_cooldown = 1.1
        else:
            self.phase = 3
            self.pattern_cooldown = 0.9

    def max_hp_value(self):
        # HealthLine uses current hp, so keep a snapshot
        return self.max_hp

    def update_state(self, delta_time):
        if self.player is None:
            self.state = "idle"
            return
        dist = hypot(self.player.center_x - self.center_x, self.player.center_y - self.center_y)
        if dist <= self.agr_radius:
            self.state = "attack"
        else:
            self.state = "chase"

    def handle_attack(self, delta_time):
        self.pattern_timer -= delta_time
        if self.pattern_timer > 0:
            return

        patterns = ["fan", "burst"]
        if self.phase >= 2:
            patterns.append("ring")
        if self.phase >= 3:
            patterns.append("slam")

        pattern = random.choice(patterns)
        if pattern == self.last_pattern and len(patterns) > 1:
            pattern = random.choice(patterns)
        self.last_pattern = pattern

        if pattern == "fan":
            self.spawn_fan(7, 70)
        elif pattern == "burst":
            self.spawn_burst(4, 10)
        elif pattern == "ring":
            self.spawn_ring(14)
        elif pattern == "slam":
            self.spawn_slam(9, 46)

        self.pattern_timer = self.pattern_cooldown

    def spawn_bullet(self, angle_deg, speed, radius, damage, damage_type="magic"):
        b = Bullet()
        b.center_x = self.center_x
        b.center_y = self.center_y
        b.angle = angle_deg
        b.damage = damage
        b.damage_type = damage_type
        b.bullet_radius = radius
        b.bullet_speed = speed
        b.variant = "boss"
        b.apply_stats()
        b.update_texture()
        return b

    def spawn_burst(self, count, spread):
        base_angle = degrees(atan2(self.player.center_y - self.center_y, self.player.center_x - self.center_x))
        for _ in range(count):
            ang = base_angle + random.uniform(-spread, spread)
            self.spawned_bullets.append(self.spawn_bullet(ang, 9.5, 6, 16, "magic"))

    def spawn_fan(self, count, spread):
        base_angle = degrees(atan2(self.player.center_y - self.center_y, self.player.center_x - self.center_x))
        step = spread / max(1, count - 1)
        start = base_angle - spread / 2
        for i in range(count):
            ang = start + step * i
            self.spawned_bullets.append(self.spawn_bullet(ang, 8.5, 5, 14, "magic"))

    def spawn_ring(self, count):
        step = 360 / count
        for i in range(count):
            ang = i * step
            self.spawned_bullets.append(self.spawn_bullet(ang, 7.5, 5, 12, "magic"))

    def spawn_slam(self, count, radius):
        step = 360 / count
        for i in range(count):
            ang = i * step
            b = self.spawn_bullet(ang, 0, 10, 20, "hit")
            b.life_frames = 6
            b.center_x = self.center_x + cos(radians(ang)) * radius
            b.center_y = self.center_y + sin(radians(ang)) * -radius
            self.spawned_bullets.append(b)

    def update(self, delta_time):
        if self.is_dead:
            return

        self.update_phase()
        self.update_state(delta_time)

        if self.state == "chase":
            self.move_to(*self.player.position)
        elif self.state == "attack":
            self.stop()
            self.handle_attack(delta_time)
            # орбитальное движение
            dx = self.player.center_x - self.center_x
            dy = self.player.center_y - self.center_y
            angle = atan2(dy, dx) + 1.2 * self.orbit_dir
            self.center_x += (self.max_speed * 0.5) * cos(angle)
            self.center_y += (self.max_speed * 0.5) * sin(angle)
        else:
            self.idle_move(delta_time)

        if self.player:
            target_angle = atan2(self.player.center_y - self.center_y, self.player.center_x - self.center_x)
            self.weapon_angle = target_angle
            self.view_angle = target_angle

        angel = -degrees(self.weapon_angle)
        self.weapon.direct_angle = angel
        self.weapon.angle = angel + 90

        if self.player:
            self.weapon.center_x = self.center_x
            self.weapon.center_y = self.center_y
            self.weapon.player = self

        self.health_line.set_current_hp(self.hp)
        self.health_line.set_coords(self.left, self.bottom)
        self.update_animation(delta_time)
