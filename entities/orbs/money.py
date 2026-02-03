import arcade

from .orb import Orb


class Money(Orb):
    def __init__(self, path_or_texture=None, scale=1, center_x=0, center_y=0):
        """
        Монета, который Выпадает с врагов \n
        Нужена для покупки орбов (если не хватиет), оружия и других итемов
        """
        super().__init__(path_or_texture, scale, center_x, center_y)

    def resize(self):
        """
        Размер относительно стоимости
        """
        self.width = 20 + 2 * (self.value - 1)
        self.height = 20 + 2 * (self.value - 1)
        self.texture = arcade.make_soft_circle_texture(self.width, (245, 200, 2))