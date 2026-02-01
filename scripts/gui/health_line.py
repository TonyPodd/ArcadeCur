import arcade


class HealthLine:
    def __init__(self, width: int, hp: int, x: float, y: float):
        """
        Отрисовка линии, показывающую хп игрока/врага и других подобных энтити
        """
        self.max_hp = hp
        self.current_hp = hp

        self.width = width
        self.height = 4
        self.x = x
        self.y = y - 12

    def draw(self):
        arcade.draw_lbwh_rectangle_filled(
            self.x,
            self.y,
            self.width,
            self.height,
            arcade.color.RED
        )

        arcade.draw_lbwh_rectangle_filled(
            self.x,
            self.y,
            self.width * (self.current_hp * 100 / self.max_hp) / 100,
            self.height,
            arcade.color.GREEN
        )

    def set_current_hp(self, hp: float):
        self.current_hp = hp

    def set_coords(self, x: float, y: float):
        self.x = x
        self.y = y - 12