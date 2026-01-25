import arcade

from entities import Player, Wall
from systems import PhysicsSystem, GameCamera
from scripts import Level
import config


class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.DARK_GREEN)

    def setup(self):
        self.camera = GameCamera()  # камера игрока
        self.gui_camera = arcade.camera.Camera2D()  # камера интерфейса

        # Player
        self.player = Player(100, 100)
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)

        # other sprites
        self.enemy_sprites = arcade.SpriteList()
        self.item_sprites = arcade.SpriteList()
        
        # Загрузка тестого уровня
        self.current_level = Level('start')
        self.all_sprites = self.current_level.get_sprites()
        self.wall_sprites = self.all_sprites['wall']
    
        # Движок коллизии
        self.physics_system = PhysicsSystem(self.player, self.wall_sprites)

    def on_draw(self):
        self.clear()

        # Отрисовка игрового мира с камерой
        self.camera.use()

        self.wall_sprites.draw()
        self.item_sprites.draw()
        self.enemy_sprites.draw()
        self.player_list.draw()

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
