import arcade
from math import atan2, cos, sin, degrees, pi
import random

import config
from .weapon import Weapon
from scripts.gui import HealthLine

class Enemy(arcade.Sprite):
    def __init__(self, x: float, y: float, type = "grunt"):
        super().__init__()

        # settings
        self.type = type
        self.is_dead = False  # Умер ли енеми
        enemy_cfg = config.ENEMY_TYPES[self.type]

        self.hp = enemy_cfg['hp']
        self.max_speed = enemy_cfg['speed']
        self.agr_radius = enemy_cfg['agr_range']
        self.attack_radius = enemy_cfg['attack_range']
        self.weapon_name = enemy_cfg['weapon']
        self.weapon_type = config.WEAPON_TYPES[self.weapon_name]['weapon_type']
        self.weapon = Weapon(center_x=int(self.center_x), center_y= int(self.center_y), type=self.weapon_name, clas= self.weapon_type)

        self.last_seen = None
        self.reaction_time = enemy_cfg['reaction_time']
        self.attack_cooldown = enemy_cfg['attack_cooldown']
        self.burst_size = enemy_cfg['burst_size']
        self.burst_pause = enemy_cfg['burst_pause']
        self.spread = enemy_cfg['spread']

        self.reaction_timer = 0.0
        self.cooldown_timer = 0.0
        self.burst_left = self.burst_size
        self.spawned_bullets = []  # пули, созданные врагом в этом кадре
        self.prev_state = None
        self.idle_target = None
        self.idle_timer = 0.0
        self.view_angle = 0

        self.walls = None

        self.state = 'idle'
        self.player = None

        self.bullets_hitted = arcade.SpriteList()  # Пули которые попали во врага, (чтобы не было повторного урона)

        self.is_player_visible = False


        # Временный квадрат вместо спрайта
        self.texture = arcade.make_soft_square_texture(40, arcade.color.RED, outer_alpha=255)
        self._hit_box._points = ((-20, -15), (20, -15), (20, 15), (-20, 15))
        self.health_line = HealthLine(
            self.width,
            self.hp,
            self.left,
            self.bottom
        )

        self.dist_to_player = 0

        self.center_x = x
        self.center_y = y
        self.view_angle = 0.0
        self.weapon_angle = 0.0
        self.turn_speed = 6.0  # рад/сек, скорость поворота оружия
        self.idle_speed_factor = 0.4
        self.idle_wait_time = 0.5
        self.idle_stuck_time = 0.6
        self._idle_stuck_timer = 0.0
        self._last_pos = (self.center_x, self.center_y)

    def update_state(self, delta):
        if self.player is None or self.walls is None:
            self.state = 'idle'
            return


        self.dist_to_player = arcade.get_distance_between_sprites(self, self.player)
        if self.dist_to_player > self.agr_radius:
            self.is_player_visible = False

        else:
            self.is_player_visible = arcade.has_line_of_sight(
                (self.center_x, self.center_y),
                (self.player.center_x, self.player.center_y),
                self.walls,
                max_distance=self.agr_radius
            )

            if self.is_player_visible:
                self.last_seen = (self.player.center_x, self.player.center_y)

        if self.last_seen == (self.center_x, self.center_y):
            self.last_seen = None

        if self.is_player_visible and self.dist_to_player < self.attack_radius:
            self.state = "attack"
        elif self.is_player_visible:
            self.state = "chase"
        elif self.last_seen:
            self.state = "alert"
        else:
            self.state = "idle"


    def move_to(self, x, y):
        dx = x - self.center_x
        dy = y - self.center_y
        dist = (dx * dx + dy * dy) ** 0.5
        if dist < 4:
            self.change_x = 0
            self.change_y = 0
            return True
        self.view_angle = atan2(dy, dx)
        self.change_x = self.max_speed * cos(self.view_angle)
        self.change_y = self.max_speed * sin(self.view_angle)
        return False

    def smooth_angle(self, current, target, speed, dt):
        # Плавный поворот по кратчайшему пути
        diff = (target - current + pi) % (2 * pi) - pi
        step = speed * dt
        if abs(diff) <= step:
            return target
        return current + step * (1 if diff > 0 else -1)

    def idle_move(self, delta_time):
        # ждём, выбираем цель, идём к ней без рывков
        if self.idle_timer > 0:
            self.idle_timer -= delta_time
            self.change_x = 0
            self.change_y = 0
            return

        if self.idle_target is None:
            offset_x = random.randint(-60, 60)
            offset_y = random.randint(-60, 60)
            self.idle_target = (self.center_x + offset_x, self.center_y + offset_y)

        dx = self.idle_target[0] - self.center_x
        dy = self.idle_target[1] - self.center_y
        dist = (dx * dx + dy * dy) ** 0.5
        if dist < 4:
            self.idle_target = None
            self.idle_timer = self.idle_wait_time
            self.change_x = 0
            self.change_y = 0
            self._idle_stuck_timer = 0.0
            return

        target_angle = atan2(dy, dx)
        self.view_angle = self.smooth_angle(self.view_angle, target_angle, self.turn_speed, delta_time)
        speed = self.max_speed * self.idle_speed_factor
        self.change_x = speed * cos(self.view_angle)
        self.change_y = speed * sin(self.view_angle)

        # если позиция не меняется, сбрасываем цель
        cur_pos = (self.center_x, self.center_y)
        if cur_pos == self._last_pos:
            self._idle_stuck_timer += delta_time
            if self._idle_stuck_timer >= self.idle_stuck_time:
                self.idle_target = None
                self.idle_timer = self.idle_wait_time
                self._idle_stuck_timer = 0.0
        else:
            self._idle_stuck_timer = 0.0
        self._last_pos = cur_pos


    def draw_item(self):
        """ Отрисовывать предмет в руках """
        if not self.is_dead:
            self.weapon.draw()


    def update(self, delta_time):
        self.death_check()
        self.health_line.set_current_hp(self.hp)
        self.health_line.set_coords(self.left, self.bottom)
        self.update_state(delta_time)

        if self.player:
            # синхроним оружие с врагом
            self.weapon.center_x = self.center_x
            self.weapon.center_y = self.center_y
            self.weapon.player = self

        if self.state != self.prev_state:
            if self.state in ("attack", "chase"):
                self.reaction_timer = self.reaction_time
            self.prev_state = self.state

        # таймеры реакции/кулдауна
        if self.reaction_timer > 0:
            self.reaction_timer = max(0.0, self.reaction_timer - delta_time)
        if self.cooldown_timer > 0:
            self.cooldown_timer = max(0.0, self.cooldown_timer - delta_time)

        if self.state == 'chase':
            self.move_to(self.player.center_x, self.player.center_y)
        elif self.state == 'alert' and self.last_seen:
            self.move_to(self.last_seen[0], self.last_seen[1])
        elif self.state == 'attack':
            self.try_attack()
            # в атаке двигаем чела стрейфами, чтобы он не просто стоял
            dx = self.player.center_x - self.center_x
            dy = self.player.center_y - self.center_y
            angle = atan2(dy, dx) + 1.57
            self.center_x += (self.max_speed * 0.4) * cos(angle)
            self.center_y += (self.max_speed * 0.4) * sin(angle)
        else:
            self.idle_move(delta_time)

        # Плавный поворот только в idle
        if self.player and self.state == 'attack':
            dx = self.player.center_x - self.center_x
            dy = self.player.center_y - self.center_y
            target_angle = atan2(dy, dx)
            self.weapon_angle = target_angle
        else:
            target_angle = self.view_angle
            if self.state == 'idle':
                self.weapon_angle = self.smooth_angle(self.weapon_angle, target_angle, self.turn_speed, delta_time)
            else:
                self.weapon_angle = target_angle

        self.weapon.direct_angle = -degrees(self.weapon_angle)
        self.weapon.angle = -degrees(self.weapon_angle) + 90

    def try_attack(self):
        if self.player is None:
            return
        if self.reaction_timer > 0 or self.cooldown_timer > 0:
            return

        # угол на игрока
        dx = self.player.center_x - self.center_x
        dy = self.player.center_y - self.center_y
        # Согласуем систему углов с пулями (инверсия Y как у игрока)
        self.weapon.direct_angle = -degrees(atan2(dy, dx))

        bullets = self.weapon.shoot()
        if bullets:
            for b in bullets:
                self.spawned_bullets.append(b)
            self.burst_left -= 1

        if self.burst_left <= 0:
            self.cooldown_timer = self.attack_cooldown + self.burst_pause
            self.burst_left = self.burst_size
        else:
            self.cooldown_timer = self.attack_cooldown

    def take_damage(self, damage):
        """
        Получение урона
        """
        self.hp -= damage

    def draw_hp(self):
        self.health_line.draw()

    def death_check(self):
        """
        Проверка на смерть врага
        """
        if self.hp <= 0:
            self.is_dead = True
            self.remove_from_sprite_lists()
            self.kill()

    def take_damage(self, damage):
        """
        Получение урона
        """
        self.hp -= damage

    def draw(self):
        ...

    def draw_hp(self):
        self.health_line.draw()

    def death_check(self):
        """
        Проверка на смерть врага
        """
        if self.hp <= 0:
            self.is_dead = True
            self.remove_from_sprite_lists()
            self.kill()
