import arcade


class Orb(arcade.Sprite):
    def __init__(self, path_or_texture = None, scale = 1, center_x = 0, center_y = 0):
        """
        Орб, который Выпадает с врагов \n
        Нужен для перехода между локациями
        """
        super().__init__(path_or_texture, scale, center_x, center_y)
