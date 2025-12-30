import arcade

from entities import Player
from systems import PhysicsSystem, GameCamera
import config


class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.DARK_GREEN)

    def setup(self):
        self.camera = GameCamera(self.window.width, self.window.height)  # камера игрока
        self.gui_camera = arcade.camera.Camera2D()  # камера интерфейса

        # Player
        self.player = Player(100, 100)
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)

        # other sprites
        self.enemy_list = arcade.SpriteList()
        self.item_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()

        # пока что просто коллизи со стенами
        self.physics_system = PhysicsSystem(self.player, self.wall_list)

    def on_draw(self):
        self.clear()

        # Отрисовка игрового мира с камерой
        self.camera.use()

        self.wall_list.draw()
        self.item_list.draw()
        self.enemy_list.draw()
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
        self.player.update()
        self.physics_system.update()
        self.camera.center_on_sprite(self.player, 0.04)

    def on_key_press(self, key, modifiers) -> None:
        # Передвижение игрока
        if key == arcade.key.W:
            self.player.move_direction_y = 1
        elif key == arcade.key.S:
            self.player.move_direction_y = -1
        elif key == arcade.key.A:
            self.player.move_direction_x = -1
        elif key == arcade.key.D:
            self.player.move_direction_x = 1

        # Взаимодействия с интерфейсом
        # Пауза
        elif key == arcade.key.ESCAPE:
            from views import PauseView
            pause = PauseView(self)
            self.window.show_view(pause)

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.W, arcade.key.S):
            self.player.move_direction_y = 0
        elif key in (arcade.key.A, arcade.key.D):
            self.player.move_direction_x = 0
