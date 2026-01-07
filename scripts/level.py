import arcade
import csv
import random

from entities import Wall, Floor
from config import *


def load_level(level_type: str='start', num_room: int=2) -> dict:
    """
    Загрузка локации \n

    level_type - название локации \n
    num_room - количество комнат на уравле, не считая лифт и комнату босса
    """
    # Спрайты всех объектов комнаты
    object_data = {
        'floor': arcade.SpriteList(),
        'wall': arcade.SpriteList(),
    }
    
    # загрузка спрайтов с лифта
    
    return object_data


def load_room(name: str, room_type: str='fight', dx: float=0.0, dy: float=0.0) -> dict:
    """
    Загрузка комнат локации \n

    name - название комнаты \n
    room_type - тип комнаты (boss/fight/loot) \n
    dx - расположение комнаты на карте по X \n
    dy - расположение комнаты на карте по X \n
    """
    text_map = list()
    
    # Загружаем информацию с файла
    with open(file=f'levels/{room_type}/{name}.csv', mode='r', encoding='UTF-8') as file:
        reader = csv.reader(file, delimiter=',')
        
        for line in reader:
            text_map.append(line)
    
    # Спрайты всех объектов комнаты
    object_data = {
        'floor': arcade.SpriteList(),
        'wall': arcade.SpriteList(),
    }
    
    # загружаем объекты с локации
    for row in range(len(text_map)):
        for col in range(len(text_map[row])):
            tile_x = col * TILE_SIZE + dx
            tile_y = row * TILE_SIZE + dy
            
            # Пол
            if text_map[row][col] == '1':
                object_data['floor'].append(
                    Floor(
                        None,
                        1,
                        tile_x,
                        tile_y
                    )
                )
            
            # стены
            if text_map[row][col] == '2':
                object_data['wall'].append(
                    Wall(
                        None,
                        1,
                        tile_x,
                        tile_y
                    )
                )
    
    return object_data