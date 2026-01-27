import arcade
import random
import csv

from .room import Room
from config import *


class FightRoom(Room):
    def __init__(self, room_type, room_number, x, y, rooms_coords):
        super().__init__(room_type, room_number, x, y, rooms_coords)
        
        # изменяем координаты чанка на левую нижнюю часть комнаты
        for i in range(len(self.text_map)):
            for j in range(len(self.text_map[i])):
                x, y = self.text_map[i][j]
                self.x = min(x, self.x)
                self.y = min(y, self.y)
        
        data = self.data_from_file(self.room_type)
        sprites_from_data = self.load_sprites_from_data(data)
        self.add_new_sprites(sprites_from_data)

    def data_from_file(self, room_type: str) -> dict:
        """
        Загрузка объектов с файла комнаты\n
        room_type - тип комнаты
        """
        n = len(self.text_map)
        # Загрузить случайную комнату
        file_name = f'levels/{room_type}/{n}x{n}/{random.choice(ROOM_FILE_NAMES[room_type][f'{n}x{n}'])}'
        with open(file=file_name, mode='r', encoding='UTF-8') as file:
            reader = csv.reader(file, delimiter=',')
            data = list(reader)
        
        all_objects = dict()  # объекты 1: (x, y)

        for i in range(len(data)):
            for j in range(len(data[i])):
                object_type = data[i][j]
                
                if object_type != '0':
                    if object_type not in all_objects:
                        all_objects[object_type] = list()
                    
                    all_objects[object_type].append((j, i))
        
        return all_objects