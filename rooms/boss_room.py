import arcade
import random

from .room import Room
from entities import Boss
from config import TILE_SIZE


class BossRoom(Room):
    def __init__(self, room_type, room_number, x, y, rooms_coords, difficulty=1.0):
        super().__init__(room_type, room_number, x, y, rooms_coords, difficulty)

        data = self.data_from_file(self.room_type)
        sprites_from_data = self.load_sprites_from_data(data)
        self.add_new_sprites(sprites_from_data)
        self.status = 0
        self.boss_spawned = False

    def begin_fight(self):
        self.close_doors()
        return self.valid_spawn_tiles()

    def end_fight(self):
        self.status = 1
        self.open_doors()

    def spawn_enemies(self, valid_tiles_sprites: arcade.SpriteList) -> arcade.SpriteList:
        if 'enemy' not in self.all_sprites:
            self.all_sprites['enemy'] = arcade.SpriteList()
        if self.boss_spawned:
            return self.all_sprites['enemy']

        spawn_tile = valid_tiles_sprites[0] if valid_tiles_sprites else None
        if spawn_tile is None and self.all_sprites.get('floor'):
            spawn_tile = random.choice(self.all_sprites['floor'])
        if spawn_tile is None:
            return self.all_sprites['enemy']

        boss = Boss(spawn_tile.center_x, spawn_tile.center_y, difficulty=self.difficulty)
        self.all_sprites['enemy'].append(boss)
        self.boss_spawned = True
        return self.all_sprites['enemy']

    def valid_spawn_tiles(self) -> arcade.SpriteList:
        spawn_sprites = arcade.SpriteList()
        if not self.all_sprites.get('floor'):
            return spawn_sprites

        # спавним босса ближе к центру комнаты
        floor_list = self.all_sprites['floor'].sprite_list
        avg_x = sum([s.center_x for s in floor_list]) / len(floor_list)
        avg_y = sum([s.center_y for s in floor_list]) / len(floor_list)
        tile = min(floor_list, key=lambda s: (s.center_x - avg_x) ** 2 + (s.center_y - avg_y) ** 2)
        sprite = arcade.Sprite(
            arcade.make_circle_texture(TILE_SIZE, (180, 50, 80)),
            1,
            tile.center_x,
            tile.center_y
        )
        spawn_sprites.append(sprite)
        return spawn_sprites

    def close_doors(self):
        for door in self.all_sprites['door']:
            door.close_door()

    def open_doors(self):
        for door in self.all_sprites['door']:
            door.open_door()
