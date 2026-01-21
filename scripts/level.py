import arcade
import csv
import random

from entities import Wall, Floor
from config import *


def load_level(level_type: str) -> dict:
    """
    Загрузка локации \n

    level_type - название локации \n
    """

    # Спрайты всех объектов комнаты
    object_data = {}

    # Карта чанков
    text_map = list()
    for i in range(CHUNCK_SIZE[1]):
        text_map.append(list())
        for j in range(CHUNCK_SIZE[0]):
            text_map[i].append(0)
            # 0 - Пустой чанк
    
    all_rooms = create_rooms(text_map)  # все комнаты


def create_rooms(text_map: list[list]) -> dict:
    all_rooms = dict()  # номер комнаты: класс комнаты