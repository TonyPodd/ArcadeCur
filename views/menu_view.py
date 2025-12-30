"""
Главное меню игры
"""
import arcade
from views import GameView


class MenuView(arcade.View):

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        self.clear()

        arcade.draw_text(
            "Рогалик)",
            self.window.width / 2,
            self.window.height / 2 + 50,
            arcade.color.WHITE,
            font_size=50,
            anchor_x="center"
        )

        arcade.draw_text(
            "Нажмите ENTER для начала",
            self.window.width / 2,
            self.window.height / 2 - 30,
            arcade.color.WHITE,
            font_size=20,
            anchor_x="center"
        )

        arcade.draw_text(
            "ESC - Выход",
            self.window.width / 2,
            self.window.height / 2 - 60,
            arcade.color.GRAY,
            font_size=16,
            anchor_x="center"
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            game_view = GameView()
            game_view.setup()
            self.window.show_view(game_view)
        elif key == arcade.key.ESCAPE:
            arcade.close_window()
