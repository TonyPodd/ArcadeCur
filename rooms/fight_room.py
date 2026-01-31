import arcade
import random
import csv
from pathlib import Path

from .room import Room
from config import *


class FightRoom(Room):
    def __init__(self, room_type, room_number, x, y, rooms_coords):
        super().__init__(room_type, room_number, x, y, rooms_coords)
        
        data = self.data_from_file(self.room_type)
        sprites_from_data = self.load_sprites_from_data(data)
        self.add_new_sprites(sprites_from_data)
        
        self.status = 0  # статус комнаты: 0 - не зачищена, 1 - зачищена

    def data_from_file(self, room_type: str) -> dict:
        """
        Загрузка объектов с файла комнаты\n
        room_type - тип комнаты
        """
        n = len(self.text_map)
        # Загрузить случайную комнату
        size_key = f"{n}x{n}"
        file_name = f"levels/{room_type}/{size_key}/{random.choice(ROOM_FILE_NAMES[room_type][size_key])}"
        file_path = Path(__file__).resolve().parent.parent / file_name
        with open(file=file_path, mode='r', encoding='UTF-8') as file:
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

    def begin_fight(self):
        self.close_doors()
        self.spawn_enemies()
    
    def end_fight(self):
        self.open_doors()
        self.spawn_chest()

    def spawn_enemies(self):
        """
        Спавн противников
        """
    
    def close_doors(self):
        for door in self.all_sprites['door']:
            # закрыть дверь
            door.close_door()
    
    def open_doors(self):
        """
        Открытие всех дверей
        """

    def spawn_chest(self):
        """
        Спавн сундука в конце зачистки
        """
