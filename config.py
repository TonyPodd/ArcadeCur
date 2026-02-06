"""
Основные константы
"""

# game settigns
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "rogalic)"
FPS = 60
VIEWPORT_MARGIN = 200

# minimap
MINIMAP_TILE_SIZE = 10
MINIMAP_MARGIN = 30
MINIMAP_BG_ALPHA = 180
MINIMAP_GAP = 2

SFX_VOLUME = 0.5
MELEE_REFLECT_TIME = 0.3

ENEMY_INDICATOR_COUNT = 5
ENEMY_INDICATOR_RADIUS = 140
ENEMY_INDICATOR_SIZE = 10
ENEMY_INDICATOR_MIN_DISTANCE = 120

# player
PLAYER_MOVEMENT_SPEED = 180
PLAYER_ROLL_SPEED = 500
PLAYER_ROLL_TIMER = 0.3
PLAYER_SCALING = 1.0
PLAYER_HEALTH_POINTS = 100

# enemy
ENEMY_SCALING = 1.0
ENEMY_SPEED = 120

DEFAULT_BULLET_VELOCITY = 10

# bullet styles
BULLET_TRAIL_ALPHA = 200
BULLET_TRAIL_WIDTH = 2

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
        'hp' : 45,
        'weapon' : "default_gun",
        'agr_range' : 300,
        'attack_range' : 220,
        'speed' : 1.7,
        'reaction_time' : 0.35,
        'attack_cooldown' : 0.7,
        'burst_size' : 2,
        'burst_pause' : 0.7,
        'spread' : 3,
    },
    'grunt' : {
        'name' : 'штурмовик',
        'hp' : 75,
        'weapon' : "rifle",
        'agr_range' : 260,
        'attack_range' : 180,
        'speed' : 3.2,
        'reaction_time' : 0.25,
        'attack_cooldown' : 0.4,
        'burst_size' : 3,
        'burst_pause' : 0.6,
        'spread' : 2,
    },
    'shotgunner' : {
        'name' : 'дробовик',
        'hp' : 80,
        'weapon' : "shotgun",
        'agr_range' : 220,
        'attack_range' : 110,
        'speed' : 3.0,
        'reaction_time' : 0.3,
        'attack_cooldown' : 1.0,
        'burst_size' : 1,
        'burst_pause' : 0.9,
        'spread' : 7,
    },
    'sniper' : {
        'name' : 'снайпер',
        'hp' : 50,
        'weapon' : "sniper",
        'agr_range' : 360,
        'attack_range' : 320,
        'speed' : 2.2,
        'reaction_time' : 0.6,
        'attack_cooldown' : 1.6,
        'burst_size' : 1,
        'burst_pause' : 1.2,
        'spread' : 0.6,
    },
    'brute' : {
        'name' : 'громила',
        'hp' : 160,
        'weapon' : "axe",
        'agr_range' : 200,
        'attack_range' : 70,
        'speed' : 2.4,
        'reaction_time' : 0.4,
        'attack_cooldown' : 0.85,
        'burst_size' : 1,
        'burst_pause' : 0.6,
        'spread' : 10,
    },
    'slicer' : {
        'name' : 'саблист',
        'hp' : 85,
        'weapon' : "sword",
        'agr_range' : 210,
        'attack_range' : 90,
        'speed' : 4.2,
        'reaction_time' : 0.25,
        'attack_cooldown' : 0.55,
        'burst_size' : 1,
        'burst_pause' : 0.4,
        'spread' : 8,
    },
    'imp' : {
        'name' : 'имп',
        'hp' : 40,
        'weapon' : "dagger",
        'agr_range' : 230,
        'attack_range' : 70,
        'speed' : 5.2,
        'reaction_time' : 0.2,
        'attack_cooldown' : 0.45,
        'burst_size' : 1,
        'burst_pause' : 0.3,
        'spread' : 6,
    },
    'tank' : {
        'name' : 'танк',
        'hp' : 220,
        'weapon' : "hammer",
        'agr_range' : 180,
        'attack_range' : 80,
        'speed' : 1.8,
        'reaction_time' : 0.5,
        'attack_cooldown' : 0.9,
        'burst_size' : 1,
        'burst_pause' : 0.7,
        'spread' : 12,
    },
    'shaman' : {
        'name' : 'шаман',
        'hp' : 70,
        'weapon' : "ice_wand",
        'agr_range' : 260,
        'attack_range' : 200,
        'speed' : 2.6,
        'reaction_time' : 0.35,
        'attack_cooldown' : 0.75,
        'burst_size' : 2,
        'burst_pause' : 0.8,
        'spread' : 4,
    }
}

# enemy visuals (procedural)
ENEMY_RECT_BASE = 32
ENEMY_VISUALS = {
    "recrut": {"color": (80, 120, 230), "size": (28, 28), "shape": "round"},
    "grunt": {"color": (160, 80, 220), "size": (34, 26), "shape": "rect"},
    "shotgunner": {"color": (220, 120, 60), "size": (36, 28), "shape": "hex"},
    "sniper": {"color": (100, 200, 120), "size": (24, 38), "shape": "rect"},
    "brute": {"color": (220, 80, 80), "size": (40, 40), "shape": "chunky"},
    "slicer": {"color": (80, 200, 200), "size": (30, 22), "shape": "diamond"},
    "imp": {"color": (240, 120, 160), "size": (22, 22), "shape": "diamond"},
    "tank": {"color": (120, 140, 160), "size": (46, 38), "shape": "chunky"},
    "shaman": {"color": (150, 120, 230), "size": (26, 36), "shape": "round"},
}

# procedural tiles/colors
FLOOR_COLOR = (50, 70, 60)
WALL_COLOR = (90, 90, 100)
DOOR_OPEN_COLOR = (160, 130, 70)
DOOR_CLOSED_COLOR = (80, 60, 40)
CHEST_COLOR = (30, 150, 60)
CHEST_OPEN_COLOR = (170, 200, 90)

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
    'smg' : {
        'name' : 'смг',
        'damage' : 7,
        "weapon_type" : "gun",
        'damage_type' : "projectile",
        'bullet_radius' : 3,
        'shoot_timeout' : 0.08,
        'bullet_speed' : 7,
        'shots_per_tick' : 1,
        'spread' : 3,
    },
    'burst_rifle' : {
        'name' : 'берст',
        'damage' : 9,
        "weapon_type" : "gun",
        'damage_type' : "projectile",
        'bullet_radius' : 4,
        'shoot_timeout' : 0.28,
        'bullet_speed' : 8,
        'shots_per_tick' : 3,
        'spread' : 2.5,
    },
    'shotgun' : {
        'name' : 'дробовик',
        'damage' : 10,
        "weapon_type" : "gun",
        'damage_type' : "projectile",
        'bullet_radius' : 14,
        'shoot_timeout' : 1.1,
        'bullet_speed' : 9,
        'shots_per_tick' : 7,
        'spread' : 18,
    },
    'sniper' : {
        'name' : 'снайперка',
        'damage' : 32,
        "weapon_type" : "gun",
        'damage_type' : "projectile",
        'bullet_radius' : 3,
        'shoot_timeout' : 1.2,
        'bullet_speed' : 10,
        'shots_per_tick' : 1,
        'spread' : 0.2,
    },
    'heavy_rifle' : {
        'name' : 'тяж.винтовка',
        'damage' : 18,
        "weapon_type" : "gun",
        'damage_type' : "projectile",
        'bullet_radius' : 5,
        'shoot_timeout' : 0.35,
        'bullet_speed' : 9,
        'shots_per_tick' : 1,
        'spread' : 1.5,
    },
    'railgun' : {
        'name' : 'рейлган',
        'damage' : 42,
        "weapon_type" : "gun",
        'damage_type' : "projectile",
        'bullet_radius' : 4,
        'shoot_timeout' : 1.5,
        'bullet_speed' : 14,
        'shots_per_tick' : 1,
        'spread' : 0.1,
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
    'ice_wand' : {
        'name' : 'ледяной жезл',
        'damage' : 16,
        "weapon_type" : "magic",
        'damage_type' : "projectile",
        'bullet_radius' : 7,
        'shoot_timeout' : 0.28,
        'bullet_speed' : 6,
        'shots_per_tick' : 1,
        'spread' : 3,
    },
    'sword' : {
        'name' : 'меч',
        'damage' : 18,
        "weapon_type" : "melee",
        'damage_type' : "hitscan",
        'bullet_radius' : 36,
        'shoot_timeout' : 0.55,
        'bullet_speed' : 0,
        'shots_per_tick' : 1,
        'spread' : 10,
    },
    'dagger' : {
        'name' : 'кинжал',
        'damage' : 12,
        "weapon_type" : "melee",
        'damage_type' : "hitscan",
        'bullet_radius' : 28,
        'shoot_timeout' : 0.35,
        'bullet_speed' : 0,
        'shots_per_tick' : 1,
        'spread' : 14,
    },
    'axe' : {
        'name' : 'топор',
        'damage' : 24,
        "weapon_type" : "melee",
        'damage_type' : "hitscan",
        'bullet_radius' : 32,
        'shoot_timeout' : 0.7,
        'bullet_speed' : 0,
        'shots_per_tick' : 1,
        'spread' : 14,
    },
    'hammer' : {
        'name' : 'молот',
        'damage' : 34,
        "weapon_type" : "melee",
        'damage_type' : "hitscan",
        'bullet_radius' : 38,
        'shoot_timeout' : 0.9,
        'bullet_speed' : 0,
        'shots_per_tick' : 1,
        'spread' : 10,
    }
}
