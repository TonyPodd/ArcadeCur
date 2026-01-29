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

DEFAULT_BULLET_VELOCITY = 5

VIEWPORT_MARGIN = 200

FPS = 60

LEVEL_SIZE = (10, 10)  # Размер карты чанков [x, y]
CHUNCK_SIZE = (16, 16)  # размер одного чанка
ROOM_FILE_NAMES = {
    'spawn': ['elevator.csv'],
    'loot': ['test.csv'],
    'shop': ['test.csv'],
    'boss': ['test.csv'],
    'fight': {
        '2x2': ['test.csv'],
        '1x1': ['test.csv']
    }
}

RARYTIES = ['default', 'rare', 'legend']
CHEST_TYPES = ['weapon', 'ability']

WEAPON_TYPES = {
    'default_gun' : {
        'name' : 'пукалка',
        'damage' : 15,
        "weapon_type" : "gun",     # melee или gun или magiс
        'damage_type' : "hitscan",    # я думаю прикольно сделать чтобы какие-то оружия хитсканили, а у каких-то с физикой были пульки
        'bullet_radius' : 5,
        'shoot_timeout' : 0.2,
        'bullet_speed' : 5,
    }
}
