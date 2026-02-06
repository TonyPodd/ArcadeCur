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
        self.pattern_timer = 0.6
        self.pattern_index = 0
        self.pattern_cooldown = 1.2
        self.orbit_dir = random.choice([-1, 1])
        self.pending_pattern = None
        self.prep_timer = 0.0
        self.dash_timer = 0.0
        self.dash_vx = 0.0
        self.dash_vy = 0.0
        self.target_distance = 360
        self.pattern_scripts = {
            1: ["fan", "burst", "fan", "burst"],
            2: ["ring", "fan", "dash", "burst"],
            3: ["beam", "slam", "ring", "dash", "fan", "beam"],
        }

    def update_phase(self):
        hp_ratio = self.hp / max(self.max_hp_value(), 1)
        if hp_ratio > 0.65:
            self.phase = 1
            self.pattern_cooldown = 1.2
            self.target_distance = 380
        elif hp_ratio > 0.35:
            self.phase = 2
            self.pattern_cooldown = 1.0
            self.target_distance = 320
        else:
            self.phase = 3
            self.pattern_cooldown = 0.8
            self.target_distance = 260

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
        if self.pending_pattern:
            self.prep_timer -= delta_time
            if self.prep_timer <= 0:
                self.execute_pattern(self.pending_pattern)
                self.pending_pattern = None
                self.pattern_timer = self.pattern_cooldown
            return

        self.pattern_timer -= delta_time
        if self.pattern_timer > 0:
            return

        pattern = self.next_pattern()
        if pattern in ("slam", "beam", "dash"):
            self.pending_pattern = pattern
            self.prep_timer = 0.5 if self.phase == 1 else 0.4 if self.phase == 2 else 0.3
            return
        self.execute_pattern(pattern)
        self.pattern_timer = self.pattern_cooldown

    def next_pattern(self):
        script = self.pattern_scripts.get(self.phase, ["fan", "burst"])
        pattern = script[self.pattern_index % len(script)]
        self.pattern_index += 1
        return pattern

    def execute_pattern(self, pattern):
        if pattern == "fan":
            count = 9 if self.phase >= 2 else 7
            spread = 90 if self.phase >= 2 else 70
            self.spawn_fan(count, spread)
        elif pattern == "burst":
            shots = 5 if self.phase >= 3 else 4
            spread = 12 if self.phase >= 2 else 10
            self.spawn_burst(shots, spread)
        elif pattern == "ring":
            count = 18 if self.phase >= 3 else 14
            self.spawn_ring(count)
        elif pattern == "slam":
            count = 12 if self.phase >= 3 else 9
            radius = 70 if self.phase >= 3 else 56
            self.spawn_slam(count, radius)
        elif pattern == "beam":
            self.spawn_beam(6 if self.phase >= 2 else 4)
        elif pattern == "dash":
            self.start_dash()

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

    def spawn_beam(self, waves):
        base_angle = degrees(atan2(self.player.center_y - self.center_y, self.player.center_x - self.center_x))
        for i in range(waves):
            ang = base_angle + random.uniform(-4, 4)
            b = self.spawn_bullet(ang, 14 + i * 0.6, 6, 20, "magic")
            self.spawned_bullets.append(b)

    def start_dash(self):
        if self.player is None:
            return
        dx = self.player.center_x - self.center_x
        dy = self.player.center_y - self.center_y
        dist = hypot(dx, dy) or 1.0
        speed = 420 if self.phase >= 2 else 360
        self.dash_vx = (dx / dist) * speed
        self.dash_vy = (dy / dist) * speed
        self.dash_timer = 0.35 if self.phase >= 2 else 0.3

    def update(self, delta_time):
        if self.is_dead:
            return

        self.update_phase()
        self.update_state(delta_time)

        if self.dash_timer > 0:
            self.dash_timer -= delta_time
            self.center_x += self.dash_vx * delta_time
            self.center_y += self.dash_vy * delta_time
            if self.dash_timer <= 0:
                self.spawn_ring(10 if self.phase >= 2 else 8)
        elif self.state == "chase":
            self.move_to(*self.player.position)
        elif self.state == "attack":
            self.stop()
            self.handle_attack(delta_time)
            # держим дистанцию и орбитим
            dx = self.player.center_x - self.center_x
            dy = self.player.center_y - self.center_y
            dist = hypot(dx, dy) or 1.0
            desired = self.target_distance
            if dist < desired * 0.7:
                self.center_x -= (dx / dist) * self.max_speed * 0.7
                self.center_y -= (dy / dist) * self.max_speed * 0.7
            elif dist > desired * 1.3:
                self.center_x += (dx / dist) * self.max_speed * 0.7
                self.center_y += (dy / dist) * self.max_speed * 0.7
            else:
                angle = atan2(dy, dx) + 1.1 * self.orbit_dir
                self.center_x += (self.max_speed * 0.6) * cos(angle)
                self.center_y += (self.max_speed * 0.6) * sin(angle)
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

    def draw_item(self):
        if self.is_dead:
            return
        # аура босса вместо оружия
        radius = max(self.width, self.height) * 0.6
        alpha = 60 + 20 * self.phase
        arcade.draw_circle_outline(self.center_x, self.center_y, radius, (255, 120, 160, alpha), 4)
        arcade.draw_circle_outline(self.center_x, self.center_y, radius * 0.7, (255, 200, 220, alpha), 2)
