import arcade


class HealthLine:
    def __init__(self, sprite: arcade.Sprite):
        """
        Отрисовка линии, показывающую хп игрока/врага и других подобных энтити
        """
        self.sprite = sprite
        self.max_hp = self.sprite.hp
        self.current_hp = self.sprite.hp

        self.width = sprite.width
        self.height = 4
        self.x = self.sprite.left
        self.y = self.sprite.bottom - 5

    def draw(self):
        arcade.draw_lbwh_rectangle_filled(
            self.x,
            self.y,
            self.width,
            self.height
        )
        
        arcade.draw_lbwh_rectangle_filled(
            self.x,
            self.y,
            self.width * (self.current_hp * 100 / self.max_hp ),
            self.height
        )

    def set_current_hp(self, hp):
        self.current_hp = hp