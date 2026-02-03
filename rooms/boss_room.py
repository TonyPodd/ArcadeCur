import arcade

from .room import Room


class BossRoom(Room):
    def __init__(self, room_type, room_number, x, y, rooms_coords):
        super().__init__(room_type, room_number, x, y, rooms_coords)

        data = self.data_from_file(self.room_type)
        sprites_from_data = self.load_sprites_from_data(data)
        self.add_new_sprites(sprites_from_data)