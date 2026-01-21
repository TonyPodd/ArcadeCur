import arcade

from config import *

class Room:
    def __init__(self, room_type: str, room_number: int, x: int, y: int):
        self.x = x
        self.y = y
        self.room_type = room_type
        self.room_number = room_number

    def get_sprites(self):
        pass

    def create_door(self):
        pass

    def create_wall(self):
        pass