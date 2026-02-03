import arcade

from .object import InetactiveObject


class Engine(InetactiveObject):
    def __init__(self, path_or_texture=None, scale=1, center_x=0, center_y=0):
        super().__init__(path_or_texture, scale, center_x, center_y)

    def update(self, delta_time = 1 / 60):
        ...