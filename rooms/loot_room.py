import arcade
import random

from .room import Room
from entities import Floor, Wall
from entities import Chest
from config import *


class LootRoom(Room):
    def __init__(self, room_type, room_number, x, y, rooms_coords):
        super().__init__(room_type, room_number, x, y, rooms_coords)

        data = self.data_from_file(self.room_type)
        sprites_from_data = self.load_sprites_from_data(data)
        self.add_new_sprites(sprites_from_data)
    
    def load_sprites_from_data(self, data: dict) -> dict:
        sprites = {
            'floor': arcade.SpriteList(use_spatial_hash=True),
            'wall': arcade.SpriteList(use_spatial_hash=True),
            'interactive': arcade.SpriteList(use_spatial_hash=True),
            'chest': arcade.SpriteList(use_spatial_hash=True)
        }
        
        for object_type in data:
            for j, i in data[object_type]:
                tile_x = self.x * CHUNCK_SIZE[0] * TILE_SIZE + TILE_SIZE * (j + 1)
                tile_y = self.y * CHUNCK_SIZE[1] * TILE_SIZE + TILE_SIZE * (i + 1)
            
                if object_type == '1':
                    sprites['floor'].append(Floor(
                        None, 1, tile_x, tile_y
                    ))
                    
                if object_type == '2':
                    sprites['wall'].append(Wall(
                        None, 1, tile_x, tile_y
                    ))

                if object_type == '3':
                    # определяем редкость сундука
                    random_num = random.randint(1, 101)
                    if random_num <= 80:
                        rarity = RARITIES[0]
                    elif random_num < 95:
                        rarity = RARITIES[1]
                    else:
                        rarity = RARITIES[2]
                    
                    chest = Chest(
                        1,
                        tile_x,
                        tile_y,
                        rarity,
                        'weapon'
                    )

                    sprites['chest'].append(chest)
                    sprites['interactive'].append(chest)

        return sprites