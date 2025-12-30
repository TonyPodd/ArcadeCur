import arcade
from game.game import Game
import config


def main():
    game = Game(config.SCREEN_WIDTH, config.SCREEN_HEIGHT, config.SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
