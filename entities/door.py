import arcade


class Door(arcade.Sprite):
    def __init__(self, scale=1, center_x=0, center_y=0, size: list[int, int]=None):
        super().__init__(None, scale, center_x, center_y)
        
        self.width = size[0]
        self.height = size[1]
        
        self.is_close = False  # Закртыта ли дверь