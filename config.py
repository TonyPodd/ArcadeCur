"""
Основные константы
"""

# game settigns
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "rogalic)"
FPS = 60
VIEWPORT_MARGIN = 200

# player
PLAYER_MOVEMENT_SPEED = 120
PLAYER_ROLL_SPEED = 400
PLAYER_ROLL_TIMER = 0.3
PLAYER_SCALING = 1.0
PLAYER_HEALTH_POINTS = 100

# enemy
ENEMY_SCALING = 1.0
ENEMY_SPEED = 120

DEFAULT_BULLET_VELOCITY = 5

# level
TILE_SIZE = 64
TILE_SCALING = 1.0
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

# chest
RARYTIES = ['default', 'rare', 'legend']
CHEST_TYPES = ['weapon', 'ability']

# Позиции сундуков в стартовой комнате (в координатах CSV, 0..13)
SPAWN_CHEST_TILES = [(2, 2), (11, 2), (6, 10)]


#enemies
ENEMY_TYPES = {
    'recrut' : {
        'name' : 'мудак',
        'hp' : 50,
        'weapon' : "default_gun",
        'agr_range' : 50,
        'attack_range' : 40,
        'speed' : 3,
    }
}

# enemy spawn от первого значения до последнего
FIGHT_ROOM_ENEMY_COUNT_1X1 = (6, 10)
FIGHT_ROOM_ENEMY_COUNT_2X2 = (14, 18)

# weapon
WEAPON_TYPES = {
    'default_gun' : {
        'name' : 'пукалка',
        'damage' : 15,
        "weapon_type" : "gun",     # melee или gun или magiс
        'damage_type' : "projectile",    # melee будет hitscan, всё остальное — projectile
        'bullet_radius' : 5,
        'shoot_timeout' : 0.2,
        'bullet_speed' : 5,
        'shots_per_tick' : 1,
        'spread' : 2, # разброс
    },
    'pistol' : {
        'name' : 'пистолет',
        'damage' : 10,
        "weapon_type" : "gun",
        'damage_type' : "projectile",
        'bullet_radius' : 4,
        'shoot_timeout' : 0.25,
        'bullet_speed' : 6,
        'shots_per_tick' : 1,
        'spread' : 1.5,
    },
    'rifle' : {
        'name' : 'винтовка',
        'damage' : 12,
        "weapon_type" : "gun",
        'damage_type' : "projectile",
        'bullet_radius' : 4,
        'shoot_timeout' : 0.12,
        'bullet_speed' : 8,
        'shots_per_tick' : 1,
        'spread' : 1,
    },
    'shotgun' : {
        'name' : 'дробовик',
        'damage' : 8,
        "weapon_type" : "gun",
        'damage_type' : "projectile",
        'bullet_radius' : 6,
        'shoot_timeout' : 1,
        'bullet_speed' : 6,
        'shots_per_tick' : 8,
        'spread' : 10,
    },
    'sniper' : {
        'name' : 'снайперка',
        'damage' : 35,
        "weapon_type" : "gun",
        'damage_type' : "projectile",
        'bullet_radius' : 3,
        'shoot_timeout' : 1.0,
        'bullet_speed' : 10,
        'shots_per_tick' : 1,
        'spread' : 0.2,
    },
    'orb' : {
        'name' : 'посох',
        'damage' : 30,
        "weapon_type" : "magic",
        'damage_type' : "projectile",
        'bullet_radius' : 10,
        'shoot_timeout' : 0.4,
        'bullet_speed' : 3,
        'shots_per_tick' : 1,
        'spread' : 2.5,
    },
    'fire_wand' : {
        'name' : 'палочка',
        'damage' : 14,
        "weapon_type" : "magic",
        'damage_type' : "projectile",
        'bullet_radius' : 6,
        'shoot_timeout' : 0.18,
        'bullet_speed' : 7,
        'shots_per_tick' : 1,
        'spread' : 4,
    },
    'sword' : {
        'name' : 'меч',
        'damage' : 20,
        "weapon_type" : "melee",
        'damage_type' : "hitscan",
        'bullet_radius' : 12,
        'shoot_timeout' : 0.5,
        'bullet_speed' : 0,
        'shots_per_tick' : 1,
        'spread' : 10,
    },
    'axe' : {
        'name' : 'топор',
        'damage' : 28,
        "weapon_type" : "melee",
        'damage_type' : "hitscan",
        'bullet_radius' : 30,
        'shoot_timeout' : 0.2,
        'bullet_speed' : 0,
        'shots_per_tick' : 1,
        'spread' : 14,
    }
}
