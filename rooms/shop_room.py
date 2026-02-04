import arcade

from .room import Room
from config import *
from entities import Wall, Floor, StoreCounter


class ShopRoom(Room):
    def __init__(self, room_type, room_number, x, y, rooms_coords):
        super().__init__(room_type, room_number, x, y, rooms_coords)
        
        data = self.data_from_file('shop')
        sprites_from_data = self.load_sprites_from_data(data)
        self.add_new_sprites(sprites_from_data)
    
    def load_sprites_from_data(self, data: dict) -> dict:
        sprites = {
            'floor': arcade.SpriteList(),
            'wall': arcade.SpriteList(),
            "counter": arcade.SpriteList(),
            'interactive': arcade.SpriteList()
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

                # Лавка с предетом
                if object_type == '3':
                    counter = StoreCounter(1, tile_x, tile_y)
                    
                    sprites['interactive'].append(counter)
                    sprites['counter'].append(counter)

        return sprites
