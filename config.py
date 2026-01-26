"""
Основные константы
"""

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "rogalic)"

TILE_SIZE = 64
TILE_SCALING = 1.0

PLAYER_MOVEMENT_SPEED = 120
PLAYER_ROLL_SPEED = 400
PLAYER_ROLL_TIMER = 0.3
PLAYER_SCALING = 1.0

ENEMY_SCALING = 1.0
ENEMY_SPEED = 120

VIEWPORT_MARGIN = 200

FPS = 60

LEVEL_SIZE = (10, 10)  # Размер карты чанков [x, y]
CHUNCK_SIZE = (16, 16)  # размер одного чанка
ROOM_FILE_NAMES = {
    'spawn': ['elevator.csv'],
    'loot': ['test.cvs'],
    'shop': ['test.cvs'],
    'boss': ['test.cvs'],
    'fight11': ['test.cvs'],  # комната 1x1
    'fight22': ['test.csv'],  # комната 2x2
}