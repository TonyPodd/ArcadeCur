import arcade

from game import Game
import config


""" Файл для запуска игры """
def main():
    game = Game(config.SCREEN_WIDTH, config.SCREEN_HEIGHT, config.SCREEN_TITLE)
    game.setup()
    game.run()


if __name__ == "__main__":
    main()
