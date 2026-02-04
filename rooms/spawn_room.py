import arcade
import random

from .room import Room
from config import *
from entities import Floor, Wall, Chest, Engine, StoreCounter


class SpawnRoom(Room):
    def __init__(self, room_type, room_number, x, y, rooms_coords):
        super().__init__(room_type, room_number, x, y, rooms_coords)
        self.create_spawn()

        data = self.data_from_file('spawn')
        sprites_from_data = self.load_sprites_from_data(data)
        self.add_new_sprites(sprites_from_data)

    def create_spawn(self) -> None:
        spawn_x = self.x * CHUNCK_SIZE[0] * TILE_SIZE + (CHUNCK_SIZE[0] * TILE_SIZE) // 2
        spawn_y = self.y * CHUNCK_SIZE[1] * TILE_SIZE + (CHUNCK_SIZE[1] * TILE_SIZE) // 2
        self.spawn = Floor(None, 1, spawn_x, spawn_y)

    def get_spawn(self) -> arcade.Sprite:
        return self.spawn

    def load_sprites_from_data(self, data: dict) -> dict:
        # Все спрайты с комнат
        sprites = {
            'floor': arcade.SpriteList(),
            'wall': arcade.SpriteList(),
            'interactive': arcade.SpriteList(),
            'engine': arcade.SpriteList(),
            'chest': arcade.SpriteList(),
            'counter': arcade.SpriteList()
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
                
                if object_type == '3':
                    obj_sprite = Engine(
                        None, 1, tile_x, tile_y
                    )
                    sprites['engine'].append(obj_sprite)
                    sprites['interactive'].append(obj_sprite)

                if object_type == '4':
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
                
                # Тестовый объект
                if object_type == 'test':
                    counter = StoreCounter(
                        1, tile_x, tile_y
                    )
                    sprites['counter'].append(counter)
                    sprites['interactive'].append(counter)

        return sprites
