import arcade

from .orb import Orb


class Money(Orb):
    def __init__(self, path_or_texture=None, scale=1, center_x=0, center_y=0):
        """
        Монета, который Выпадает с врагов \n
        Нужена для покупки орбов (если не хватиет), оружия и других итемов
        """
        super().__init__(path_or_texture, scale, center_x, center_y)
