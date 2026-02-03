import arcade


class EnginUi:
    def __init__(self, x: int, y:int):
        super().__init__()
        """ Интерфейс для пользования двигателем лифта """
        self.cost = 1  # Кол-во орбов, для перехода на некст локу
        self.value = 0 # Кол-во орбов, влитых в движок
        self.text_color = arcade.color.RED  # изначальный цвет текста

        # размер окна
        self.width = 200
        self.height = 100
        
        # Коорды левого нижнего
        self.x = x - self.width / 2
        self.y = y

    def draw(self):
        #  Основа
        arcade.draw_lbwh_rectangle_filled(
            self.x,
            self.y,
            self.width,
            self.height,
            (61, 61, 61)
        )
        # Каёмка
        arcade.draw_lbwh_rectangle_outline(
            self.x,
            self.y,
            self.width,
            self.height,
            arcade.color.BLACK,
            4
        )
        # текст
        arcade.draw_text(
            f'Топливо: {self.value}/{self.cost}',
            self.x + 5, 
            self.y + self.height - 14,
            self.text_color
        )

    def update(self):
        if self.value == self.cost:
            self.text_color = arcade.color.GREEN
        else:
            self.text_color = arcade.color.RED