import arcade

from views import MenuView
import config

# Game loop
class Game(arcade.Window):
    def __init__(self, width, height: int, title: int) -> None:
        super().__init__(width, height, title, center_window=True)
        arcade.enable_timings()

        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        menu_view = MenuView()
        self.show_view(menu_view)


def main():
    game = Game(config.SCREEN_WIDTH, config.SCREEN_HEIGHT, config.SCREEN_TITLE)
    game.setup()
    game.run()


if __name__ == "__main__":
    main()
