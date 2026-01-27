import arcade

from entities import Player, Wall
from systems import PhysicsSystem, GameCamera
from levels import Level
import config


class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.DARK_GREEN)

    def setup(self):
        # Player
        self.player = Player(0, 0)
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)

        # Камера
        self.camera = GameCamera()  # камера игрока
        self.gui_camera = arcade.camera.Camera2D()  # камера интерфейса
        self.camera.set_position(0, 0)
        
        # Уровни
        self.all_levels = list()  # все уровни
        self.current_level_number = 0  # Какой сейчс уровень
        self.create_level('start')  # Стартовый уровень

        # Движок коллизии
        self.physics_system = PhysicsSystem(self.player, self.wall_sprites)

    def on_draw(self):
        self.clear()

        # Отрисовка игрового мира с камерой
        self.camera.use()

        # Отрисовывается до игрока
        self.floor_sprites.draw()
        self.door_sprites.draw()
        
        # отрисовывается вместе с игроком
        self.drawing_sprites.sort(key=lambda x: x.position[1], reverse=True)
        self.drawing_sprites.draw()

        self.item_sprites.draw()
        self.enemy_sprites.draw()

        # Отрисовка UI - щас это координаты, потом что нибудь еще, тип иконка паузы
        self.gui_camera.use()

        # Координаты игрока
        arcade.draw_text(
            f"X: {int(self.player.center_x)}, Y: {int(self.player.center_y)}",
            10,
            self.window.height - 30,
            arcade.color.WHITE,
            14
        )

    def on_update(self, delta_time: float) -> None:
        self.player.update(delta_time)
        self.physics_system.update()
        self.camera.center_on_sprite(self.player, 0.04)

    def on_key_press(self, key, modifiers) -> None:
        # Передвижение игрока
        if key == arcade.key.W:
            self.player.direction['up'] = True
            self.player.last_direction_y = 'up'
        if key == arcade.key.S:
            self.player.direction['down'] = True
            self.player.last_direction_y = 'down'
        if key == arcade.key.A:
            self.player.direction['left'] = True
            self.player.last_direction_x = 'left'
        if key == arcade.key.D:
            self.player.direction['right'] = True
            self.player.last_direction_x = 'right'
        
        # дэш/перекат/рывок
        if key == arcade.key.LCTRL and not self.player.is_roll:
            if self.player.direction['left'] or self.player.direction['right'] \
                or self.player.direction['up'] or self.player.direction['down']:
                self.player.do_roll()

        # Взаимодействия с интерфейсом
        # Пауза
        if key == arcade.key.ESCAPE:
            from views import PauseView
            pause = PauseView(self)
            self.window.show_view(pause)

    def on_key_release(self, key, modifiers):
        if key == arcade.key.W:
            self.player.direction['up'] = False
        if key == arcade.key.S:
            self.player.direction['down'] = False
        if key == arcade.key.A:
            self.player.direction['left'] = False
        if key == arcade.key.D:
            self.player.direction['right'] = False

    def load_level_sprites(self, level_num: int) -> None:
        """ Загрузка спрайтов с уровня"""
        
        try:
            self.all_sprites.clear()
        except Exception:
            print('Нет спрайтов')
        try:
            self.wall_sprites.clear()
        except Exception:
            print('Нет спрайтов стен')
        try:
            self.floor_sprites.clear()
        except Exception:
            print('Нет спрайтов пола')
        try:
            self.door_sprites.clear()
        except Exception:
            print('Не спрайтов дверей')
        
        # спрайты с уровня
        self.all_sprites = self.all_levels[level_num].get_sprites()

        self.drawing_sprites = arcade.SpriteList()  # Спрайты для y-sort отрисовки
        self.drawing_sprites.append(self.player)

        self.wall_sprites = self.all_sprites['wall']
        self.floor_sprites = self.all_sprites['floor']
        self.door_sprites = self.all_sprites['door']
        
        # other sprites
        self.enemy_sprites = arcade.SpriteList()
        self.item_sprites = arcade.SpriteList()
        
        # спрайты для отрисовки, кроме пола
        for sprite in self.wall_sprites:
            self.drawing_sprites.append(sprite)

    def create_level(self, level_type: str) -> None:
        level = Level(level_type)
        self.all_levels.append(level)
        self.current_level_number = len(self.all_levels) - 1
        
        self.load_level_sprites(self.current_level_number)
        
        player_x, player_y = level.get_spawn_coords()
        self.player.set_position(player_x, player_y)
        self.camera.set_position(player_x, player_y)