import arcade

import config
from .weapon import Weapon
from scripts.gui import HealthLine

class Enemy(arcade.Sprite):
    def __init__(self, x: float, y: float, type = "recrut"):
        super().__init__()

        # settings
        self.type = type
        self.is_dead = False  # Умер ли енеми
        self.hp = config.ENEMY_TYPES[self.type]['hp']
        self.max_speed = config.ENEMY_TYPES[self.type]['speed']
        self.agr_radius = config.ENEMY_TYPES[self.type]['agr_range']
        self.attack_radius = config.ENEMY_TYPES[self.type]['attack_range']
        self.weapon_name = config.ENEMY_TYPES[self.type]['weapon']
        self.weapon_type = config.WEAPON_TYPES[self.weapon_name]['weapon_type']
        self.weapon = Weapon(center_x=int(self.center_x), center_y= int(self.center_y), type=self.weapon_name, clas= self.weapon_type)

        self.last_seen = None
        enemy_cfg = config.ENEMY_TYPES[self.type]
        self.reaction_time = enemy_cfg.get('reaction_time', 0.3)
        self.attack_cooldown = enemy_cfg.get('attack_cooldown', 0.6)
        self.burst_size = enemy_cfg.get('burst_size', 1)
        self.burst_pause = enemy_cfg.get('burst_pause', 0.6)
        self.spread = enemy_cfg.get('spread', 0)

        self.reaction_timer = 0.0
        self.cooldown_timer = 0.0
        self.burst_left = self.burst_size

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




    def update(self, delta_time):
        self.death_check()
        self.health_line.set_current_hp(self.hp)
        self.health_line.set_coords(self.left, self.bottom)



    def move_to_player(self):
        ...
        # self

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
