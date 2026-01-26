import arcade

from .room import Room
from config import *
from entities import Floor

class SpawnRoom(Room):
    def __init__(self, room_type, room_number, x, y, rooms_coords):
        super().__init__(room_type, room_number, x, y, rooms_coords)
        self.create_spawn()
        
        sprites_from_data = self.data_from_file('spawn')
        self.add_new_sprites(sprites_from_data)

    def create_spawn(self) -> None:
        spawn_x = self.x * CHUNCK_SIZE[0] * TILE_SIZE + (CHUNCK_SIZE[0] * TILE_SIZE) // 2
        spawn_y = self.y * CHUNCK_SIZE[1] * TILE_SIZE + (CHUNCK_SIZE[1] * TILE_SIZE) // 2
        self.spawn = Floor(None, 1, spawn_x, spawn_y)
    
    def get_spawn(self) -> arcade.Sprite:
        return self.spawn