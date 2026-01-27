import arcade
import random

from .room import Room
from config import *
from entities import Floor, Wall
from entities.chest import Chest

class SpawnRoom(Room):
    def __init__(self, room_type, room_number, x, y, rooms_coords):
        super().__init__(room_type, room_number, x, y, rooms_coords)
        self.create_spawn()
        self.create_chest()

        data = self.data_from_file('spawn')
        sprites_from_data = self.load_sprites_from_data(data)
        self.add_new_sprites(sprites_from_data)

    def create_spawn(self) -> None:
        spawn_x = self.x * CHUNCK_SIZE[0] * TILE_SIZE + (CHUNCK_SIZE[0] * TILE_SIZE) // 2
        spawn_y = self.y * CHUNCK_SIZE[1] * TILE_SIZE + (CHUNCK_SIZE[1] * TILE_SIZE) // 2
        self.spawn = Floor(None, 1, spawn_x, spawn_y)

    def get_spawn(self) -> arcade.Sprite:
        return self.spawn

    def create_chest(self) -> None:
        # Сундук в случайной позиции внутри комнаты, не рядом со стенами
        margin_tiles = 2
        tile_x = random.randint(margin_tiles, CHUNCK_SIZE[0] - margin_tiles - 1)
        tile_y = random.randint(margin_tiles, CHUNCK_SIZE[1] - margin_tiles - 1)
        center_x = self.x * CHUNCK_SIZE[0] * TILE_SIZE + TILE_SIZE * tile_x
        center_y = self.y * CHUNCK_SIZE[1] * TILE_SIZE + TILE_SIZE * tile_y
        self.chest = Chest(center_x=center_x, center_y=center_y)

        if 'chest' not in self.all_sprites:
            self.all_sprites['chest'] = arcade.SpriteList()
        self.all_sprites['chest'].append(self.chest)

    def load_sprites_from_data(self, data: dict) -> dict:
        # Все спрайты с комнат
        sprites = {
            'floor': arcade.SpriteList(),
            'wall': arcade.SpriteList(),
        }

        for object_type in data:
            for j, i in data[object_type]:
                tile_x = self.x * CHUNCK_SIZE[0] * TILE_SIZE + TILE_SIZE * (j + 1)
                tile_y = self.y * CHUNCK_SIZE[1] * TILE_SIZE + TILE_SIZE * (i + 1)

                # Пол
                if object_type == '1':
                    sprites['floor'].append(Floor(
                        None, 1, tile_x, tile_y
                    ))

                #  Стена
                if object_type == '2':
                    sprites['wall'].append(Wall(
                        None, 1, tile_x, tile_y
                    ))

        return sprites
