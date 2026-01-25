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

        # Карта комнаты
        self.text_map = list()

        # карту (пока только для 2x2 и 1x1)
        if len(rooms_coords) == 1:
            self.text_map.append(self.room_coords)
        if len(rooms_coords) == 4:
            for i in range(4):
                if i % 2 == 0:
                    self.text_map.append(list())
                self.text_map[i // 2].append(rooms_coords[i])

        # Загрузка угловых стен в чанка
        self.create_corner_walls()

    def get_sprites(self):
        return self.all_sprites

    def create_door(self, x: int, y: int, dir: str) -> None:
        # координаты первого тайла в чанке
        tile_x, tile_y = x * CHUNCK_SIZE[0] * TILE_SIZE, y * CHUNCK_SIZE[1] * TILE_SIZE

        print(f'Создана дверь комнаты №{self.room_number} направление: {dir}, координаты чанка: x={x} y={y}\n')

    def create_corner_walls(self):
        for y in range(len(self.text_map)):
            for x in range(len(self.text_map[y])):
                if y == 0:
                    wall_x, wall_y = x * CHUNCK_SIZE[0] * TILE_SIZE, y * CHUNCK_SIZE[1] * TILE_SIZE + TILE_SIZE * (CHUNCK_SIZE[1] - 1)
                    self.all_sprites['wall'].append(Wall(
                        None, 1, wall_x, wall_y
                    ))
                    self.all_sprites['wall'].append(Wall(
                        None, 1, wall_x + TILE_SIZE * (CHUNCK_SIZE[0] - 1), wall_y
                    ))
                    
                if y == len(self.text_map) - 1:
                    wall_x, wall_y = x * CHUNCK_SIZE[0] * TILE_SIZE, y * CHUNCK_SIZE[1] * TILE_SIZE
                    self.all_sprites['wall'].append(Wall(
                        None, 1, wall_x, wall_y
                    ))
                    self.all_sprites['wall'].append(Wall(
                        None, 1, wall_x + TILE_SIZE * (CHUNCK_SIZE[0] - 1), wall_y
                    ))
                
                if x == 0:
                    wall_x, wall_y = x * CHUNCK_SIZE[0] * TILE_SIZE, y * CHUNCK_SIZE[1] * TILE_SIZE
                    self.all_sprites['wall'].append(Wall(
                        None, 1, wall_x, wall_y
                    ))
                    self.all_sprites['wall'].append(Wall(
                        None, 1, wall_x, wall_y + TILE_SIZE * (CHUNCK_SIZE[1] - 1)
                    ))

                if x == len(self.text_map[y]) - 1:
                    wall_x, wall_y = x * CHUNCK_SIZE[0] * TILE_SIZE + (CHUNCK_SIZE[0] - 1) * TILE_SIZE, y * CHUNCK_SIZE[1] * TILE_SIZE
                    self.all_sprites['wall'].append(Wall(
                        None, 1, wall_x, wall_y
                    ))
                    self.all_sprites['wall'].append(Wall(
                        None, 1, wall_x, wall_y + TILE_SIZE * (CHUNCK_SIZE[1] - 1)
                    ))

        print(f'Угловые стены комнаты №{self.room_number} созданы\n')

    def create_wall(self, x: int, y: int, dir: str) -> None:
        # координаты первого тайла в чанке
        tile_x, tile_y = x * CHUNCK_SIZE[0] * TILE_SIZE, y * CHUNCK_SIZE[1] * TILE_SIZE

        print(f'Создана стена комнаты №{self.room_number} направление: {dir}, координаты чанка: x={x} y={y}\n')
