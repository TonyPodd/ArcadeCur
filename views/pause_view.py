
import arcade


class PauseView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view

    def on_draw(self):
        self.clear()

        self.game_view.on_draw()

        arcade.draw_text(
            "ПАУЗА",
            self.window.width / 2,
            self.window.height / 2 + 50,
            arcade.color.WHITE,
            font_size=50,
            anchor_x="center"
        )

        arcade.draw_text(
            "ENTER - Продолжить",
            self.window.width / 2,
            self.window.height / 2 - 30,
            arcade.color.WHITE,
            font_size=20,
            anchor_x="center"
        )

        arcade.draw_text(
            "ESC - Выход в меню",
            self.window.width / 2,
            self.window.height / 2 - 60,
            arcade.color.WHITE,
            font_size=20,
            anchor_x="center"
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            self.window.show_view(self.game_view)
        elif key == arcade.key.ESCAPE:
            from views.menu_view import MenuView
            menu = MenuView()
            self.window.show_view(menu)
