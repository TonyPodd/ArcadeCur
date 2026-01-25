import arcade

from config import *
from entities import Door, Wall

class Room:
    def __init__(self, room_type: str, room_number: int, x: int, y: int, rooms_coords: tuple[tuple]):
        # settigns
        self.x = x
        self.y = y
        self.room_type = room_type
        self.room_number = room_number
        self.room_coords = rooms_coords
        
        # Sprites
        self.all_sprites = {
            'floor': arcade.SpriteList(),
            'wall': arcade.SpriteList(),
            'door': arcade.SpriteList()
        }

    def get_sprites(self):
        return self.all_sprites

    def create_door(self, x: int, y: int, dir: str) -> None:
        # координаты первого тайла в чанке
        tile_x, tile_y = x * CHUNCK_SIZE[0] * TILE_SIZE, y * CHUNCK_SIZE[1] * TILE_SIZE

        # Создание двери
        if dir == 'left':
            pass

        if dir == 'right':
            pass

        if dir == 'up':
            pass

        if dir == 'down':
            pass



    def create_wall(self, x: int, y: int, dir: str) -> None:
        # координаты первого тайла в чанке
        tile_x, tile_y = x * CHUNCK_SIZE[0] * TILE_SIZE, y * CHUNCK_SIZE[1] * TILE_SIZE

        # Создание стен
        if dir == 'left':
            for i in range(CHUNCK_SIZE[1]):
                delta_tile_y = tile_y + i * TILE_SIZE
                wall = Wall(
                    None, 1, tile_x, delta_tile_y
                )
                self.all_sprites['wall'].append(wall)

        if dir == 'right':
            tile_x += (CHUNCK_SIZE[0] - 1) * TILE_SIZE
            for i in range(CHUNCK_SIZE[0]):
                delta_tile_y = tile_y + i * TILE_SIZE
                wall = Wall(
                    None, 1, tile_x, delta_tile_y
                )
                self.all_sprites['wall'].append(wall)

        if dir == 'up':
            tile_y += (CHUNCK_SIZE[1] - 1) * TILE_SIZE
            for i in range(CHUNCK_SIZE[0]):
                delta_tile_x = tile_x + i * TILE_SIZE
                wall = Wall(
                    None, 1, delta_tile_x, tile_y
                )
                self.all_sprites['wall'].append(wall)

        if dir == 'down':
            for i in range(CHUNCK_SIZE[0]):
                delta_tile_x = tile_x + i * TILE_SIZE
                wall = Wall(
                    None, 1, delta_tile_x, tile_y
                )
                self.all_sprites['wall'].append(wall)