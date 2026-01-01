import arcade
import csv

from entities import Wall, Floor
from config import *


def load_level(name: str) -> dict:
    text_map = list()
    
    # Загружаем информацию с файла
    with open(file=f'levels/{name}.csv', mode='r', encoding='UTF-8') as file:
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
            tile_x = col * TILE_SIZE
            tile_y = row * TILE_SIZE
            
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