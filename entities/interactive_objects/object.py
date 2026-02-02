import arcade

from config import *

class InetactiveObject(arcade.Sprite):
    def __init__(self, path_or_texture=None, scale=1, center_x=0, center_y=0):
        super().__init__(path_or_texture, scale, center_x, center_y)
        
        self.texture = arcade.make_soft_square_texture(TILE_SIZE, arcade.color.YELLOW_ROSE, outer_alpha=255)
        self.tips = False  # Подсказки взаимодействия с объектом
        self.tips_text = 'E - Взаимодействуй со мной'
        self.interaction = False  # Может  ли взаимодействовать игрок в занный момент

        ds = 10  # На сколько надо расширить хитбокс для коллизии
        self._hit_box._points = (
            (-self.width / 2 - ds, -self.height / 2 - ds),
            (-self.width / 2 - ds, self.height / 2 + ds),
            (self.width / 2 + ds, self.height / 2 + ds),
            (self.width / 2 + ds, -self.height / 2 - ds)
        )
        
    def update(self, delta_time: float=1 / 60):
        ...

    def draw_tips(self):
        if self.tips:
            arcade.draw_text(
                self.tips_text,
                self.center_x,
                self.center_y,
                arcade.color.WHITE,
                14
            )

    def use(self):
        if self.interaction:
            ...

    def set_new_hit_box(self, ds):
        self._hit_box._points = (
            (-self.width / 2 - ds, -self.height / 2 - ds),
            (-self.width / 2 - ds, self.height / 2 + ds),
            (self.width / 2 + ds, self.height / 2 + ds),
            (self.width / 2 + ds, self.height / 2 - ds)
        )
