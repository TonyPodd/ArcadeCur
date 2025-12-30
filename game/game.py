import arcade
from views.menu_view import MenuView
import config


class Game(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        menu_view = MenuView()
        self.show_view(menu_view)
