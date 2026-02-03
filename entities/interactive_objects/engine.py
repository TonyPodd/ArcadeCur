import arcade

from .object import InetactiveObject
from scripts.gui import EnginUi


class Engine(InetactiveObject):
    def __init__(self, path_or_texture=None, scale=1, center_x=0, center_y=0):
        super().__init__(path_or_texture, scale, center_x, center_y)
        
        self.engine_ui = EnginUi(self.center_x, self.center_y)
        self.all_ui.append(self.engine_ui)

    def update(self, delta_time = 1 / 60):
        super().update(delta_time)

        self.engine_ui.update()