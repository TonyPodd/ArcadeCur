import arcade

from config import *
from entities import Door, Wall, Floor

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
        # Загрузка пола
        self.create_floor()

    def get_sprites(self):
        """ Получить все спрайты с комнаты """
        return self.all_sprites

    def create_door(self, x: int, y: int, dir: str) -> None:
        """
        Создание двери в определённом чанке и с определённой стороны\n
        x, y - координаты чанка\n
        dir - с какой стороны будет дверь\n
        """
        # координаты первого тайла в чанке
        tile_x = x * CHUNCK_SIZE[0] * TILE_SIZE
        tile_y = y * CHUNCK_SIZE[1] * TILE_SIZE
        door_lenth = 4  # Кол-во тайлов с дверью

        # Сдвиги координат начального тайла
        if dir == 'right':
            tile_x += (CHUNCK_SIZE[0] - 1) * TILE_SIZE
        if dir == 'up':
            tile_y += (CHUNCK_SIZE[1] - 1) * TILE_SIZE

        # создание двери справа/слева
        if dir in ['right', 'left']:
            wall_lenth = (CHUNCK_SIZE[1] - 2 - door_lenth) // 2  # кол-во тайлов со стеной / 2
            
            # нижняя стена
            for i in range(wall_lenth):
                tile_y += TILE_SIZE
                self.all_sprites['wall'].append(Wall(
                    None, 1, tile_x, tile_y
                ))

            # дверь
            for i in range(door_lenth):
                tile_y += TILE_SIZE
                self.all_sprites['door'].append(Door(
                    1, tile_x, tile_y
                ))
            
            # верхняя стена
            for i in range(wall_lenth + door_lenth, CHUNCK_SIZE[1] - 2):
                tile_y += TILE_SIZE
                self.all_sprites['wall'].append(Wall(
                    None, 1, tile_x, tile_y
                ))

        # создание двери сверху/снизу
        if dir in ['up', 'down']:
            wall_lenth = (CHUNCK_SIZE[0] - 2 - door_lenth) // 2  # кол-во тайлов со стеной / 2
            
            # левая стена
            for i in range(wall_lenth):
                tile_x += TILE_SIZE
                self.all_sprites['wall'].append(Wall(
                    None, 1, tile_x, tile_y
                ))

            # дверь
            for i in range(door_lenth):
                tile_x += TILE_SIZE
                self.all_sprites['door'].append(Door(
                    1, tile_x, tile_y
                ))
            
            # правая стена
            for i in range(wall_lenth + door_lenth, CHUNCK_SIZE[1] - 2):
                tile_x += TILE_SIZE
                self.all_sprites['wall'].append(Wall(
                    None, 1, tile_x, tile_y
                ))

    def create_corner_walls(self):
        """ Создание стен по углам чанка """

        for y in range(len(self.text_map)):
            for x in range(len(self.text_map[y])):
                
                # down
                if y == 0:
                    wall_x = self.text_map[y][x][0] * CHUNCK_SIZE[0] * TILE_SIZE
                    wall_y = self.text_map[y][x][1] * CHUNCK_SIZE[1] * TILE_SIZE

                    self.all_sprites['wall'].append(Wall(
                        None, 1, wall_x, wall_y
                    ))
                    self.all_sprites['wall'].append(Wall(
                        None, 1, wall_x + TILE_SIZE * (CHUNCK_SIZE[0] - 1), wall_y
                    ))

                # up
                if y == len(self.text_map) - 1:
                    wall_x = self.text_map[y][x][0] * CHUNCK_SIZE[0] * TILE_SIZE
                    wall_y = self.text_map[y][x][1] * CHUNCK_SIZE[1] * TILE_SIZE + TILE_SIZE * (CHUNCK_SIZE[1] - 1)
                    
                    self.all_sprites['wall'].append(Wall(
                        None, 1, wall_x, wall_y
                    ))
                    self.all_sprites['wall'].append(Wall(
                        None, 1, wall_x + TILE_SIZE * (CHUNCK_SIZE[0] - 1), wall_y
                    ))

                # left
                if x == 0:
                    wall_x = self.text_map[y][x][0] * CHUNCK_SIZE[0] * TILE_SIZE
                    wall_y = self.text_map[y][x][1] * CHUNCK_SIZE[1] * TILE_SIZE
                    
                    self.all_sprites['wall'].append(Wall(
                        None, 1, wall_x, wall_y
                    ))
                    self.all_sprites['wall'].append(Wall(
                        None, 1, wall_x, wall_y + TILE_SIZE * (CHUNCK_SIZE[1] - 1)
                    ))

                # right
                if x == len(self.text_map[y]) - 1:
                    wall_x = self.text_map[y][x][0] * CHUNCK_SIZE[0] * TILE_SIZE + (CHUNCK_SIZE[0] - 1) * TILE_SIZE
                    wall_y = self.text_map[y][x][1] * CHUNCK_SIZE[1] * TILE_SIZE
                    
                    self.all_sprites['wall'].append(Wall(
                        None, 1, wall_x, wall_y
                    ))
                    self.all_sprites['wall'].append(Wall(
                        None, 1, wall_x, wall_y + TILE_SIZE * (CHUNCK_SIZE[1] - 1)
                    ))

        print(f'Угловые стены комнаты №{self.room_number} созданы\n')

    def create_wall(self, x: int, y: int, dir: str) -> None:
        """
        Функция создание стены в чанке с определнной стороны\n
        x, y - координаты чанка\n
        dir - сторона, с которой будет стоять стена
        """
        
        # координаты первого тайла в чанке
        tile_x = x * CHUNCK_SIZE[0] * TILE_SIZE
        tile_y = y * CHUNCK_SIZE[1] * TILE_SIZE

        # Сдвиги координат начального тайла
        if dir == 'right':
            tile_x += (CHUNCK_SIZE[0] - 1) * TILE_SIZE
        if dir == 'up':
            tile_y += (CHUNCK_SIZE[1] - 1) * TILE_SIZE

        if dir in ['right', 'left']:
            for i in range(CHUNCK_SIZE[1] - 2):
                tile_y += TILE_SIZE
                self.all_sprites['wall'].append(Wall(
                    None, 1, tile_x, tile_y
                ))
        
        if dir in ['up', 'down']:
            for j in range(CHUNCK_SIZE[0] - 2):
                tile_x += TILE_SIZE
                self.all_sprites['wall'].append(Wall(
                    None, 1, tile_x, tile_y
                ))

    def create_floor(self):
        """ Создание пола в комнате """

        for y in range(len(self.text_map)):
            for x in range(len(self.text_map[y])):
                chunck_x, chunck_y = self.text_map[y][x]
                
                for i in range(CHUNCK_SIZE[1]):
                    for j in range(CHUNCK_SIZE[0]):
                        tile_x = chunck_x * CHUNCK_SIZE[0] * TILE_SIZE + TILE_SIZE * j
                        tile_y = chunck_y * CHUNCK_SIZE[1] * TILE_SIZE + TILE_SIZE * i

                        self.all_sprites['floor'].append(Floor(None, 1, tile_x, tile_y))
