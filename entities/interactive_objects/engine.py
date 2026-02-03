import arcade

from .object import InetactiveObject
from scripts.gui import EnginUi


class Engine(InetactiveObject):
    def __init__(self, path_or_texture=None, scale=1, center_x=0, center_y=0):
        super().__init__(path_or_texture, scale, center_x, center_y)
        
        self.cost = 0
        self.is_full = False
        
        self.engine_ui = EnginUi(self.center_x, self.center_y, self.cost)
        self.all_ui.append(self.engine_ui)
        
        self.value = 0

    def update(self, delta_time = 1 / 60):
        super().update(delta_time)

        self.engine_ui.update(self.value)
        if not self.is_full:
            if self.value == self.cost:
                self.is_full = True

    def set_value(self, value: int):
        """ Заправляем двигатель \n Возвращаем, то на сколько заполнили """
        delta_value = min(value, self.cost - self.value)
        self.value += delta_value

        return delta_value