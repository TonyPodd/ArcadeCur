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

# orbs
ABSORPTION_RADIUS = 150
ABSORPTION_SPEED = 6


# level
TILE_SIZE = 64
TILE_SCALING = 1.0
LEVEL_SIZE = (10, 10)  # Размер карты чанков [x, y]
CHUNCK_SIZE = (16, 16)  # размер одного чанка
ROOM_FILE_NAMES = {
    'spawn': ['elevator.csv'],
    'loot': ['1.csv', '2.csv'],
    'shop': ['1.csv'],
    'boss': ['test.csv'],
    'fight': {
        '2x2': ['1.csv'],
        '1x1': ['1.csv', '2.csv']
    }
}

# chest
RARITIES = ['default', 'rare', 'legend']
CHEST_TYPES = ['weapon', 'ability']

#enemies
ENEMY_TYPES = {
    'recrut' : {
        'name' : 'рекрут',
        'hp' : 50,
        'weapon' : "default_gun",
        'agr_range' : 300,
        'attack_range' : 220,
        'speed' : 1.5,
        'reaction_time' : 0.35,
        'attack_cooldown' : 0.6,
        'burst_size' : 2,
        'burst_pause' : 0.7,
        'spread' : 3,
    },
    'grunt' : {
        'name' : 'штурмовик',
        'hp' : 80,
        'weapon' : "rifle",
        'agr_range' : 260,
        'attack_range' : 180,
        'speed' : 3.5,
        'reaction_time' : 0.25,
        'attack_cooldown' : 0.35,
        'burst_size' : 3,
        'burst_pause' : 0.6,
        'spread' : 2,
    },
    'shotgunner' : {
        'name' : 'дробовик',
        'hp' : 70,
        'weapon' : "shotgun",
        'agr_range' : 220,
        'attack_range' : 120,
        'speed' : 3.2,
        'reaction_time' : 0.3,
        'attack_cooldown' : 0.9,
        'burst_size' : 1,
        'burst_pause' : 0.9,
        'spread' : 7,
    },
    'sniper' : {
        'name' : 'снайпер',
        'hp' : 55,
        'weapon' : "sniper",
        'agr_range' : 360,
        'attack_range' : 320,
        'speed' : 2.4,
        'reaction_time' : 0.6,
        'attack_cooldown' : 1.4,
        'burst_size' : 1,
        'burst_pause' : 1.2,
        'spread' : 0.6,
    },
    'brute' : {
        'name' : 'громила',
        'hp' : 140,
        'weapon' : "axe",
        'agr_range' : 200,
        'attack_range' : 70,
        'speed' : 2.6,
        'reaction_time' : 0.4,
        'attack_cooldown' : 0.8,
        'burst_size' : 1,
        'burst_pause' : 0.6,
        'spread' : 10,
    },
    'slicer' : {
        'name' : 'саблист',
        'hp' : 90,
        'weapon' : "sword",
        'agr_range' : 210,
        'attack_range' : 90,
        'speed' : 3.8,
        'reaction_time' : 0.25,
        'attack_cooldown' : 0.5,
        'burst_size' : 1,
        'burst_pause' : 0.4,
        'spread' : 8,
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
        'damage' : 100,
        "weapon_type" : "gun",
        'damage_type' : "projectile",
        'bullet_radius' : 20,
        'shoot_timeout' : 1,
        'bullet_speed' : 10,
        'shots_per_tick' : 8,
        'spread' : 16,
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
        'bullet_radius' : 40,
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
