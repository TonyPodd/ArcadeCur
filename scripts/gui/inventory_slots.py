import arcade

from config import *


class InventorySlots:
    def __init__(self, player: arcade.Sprite):
        
        # settings
        self.player = player  # sprite игрока
        self.num_of_slots = 2  # Количество слотов
        self.slots = [None, None]  # Слоты для оружия, которые находятся в инвентаре
        self.current_slot = self.player.current_slot  # Номер текущего слота в инвентаре

        # size
        self.width = 50
        self.height = 50

    def update(self):
        self.current_slot = self.player.current_slot
        self.get_textures()

    def draw(self):
        # Отрисовка самих слотов словтов
        x = SCREEN_WIDTH // 2 - (self.width * self.num_of_slots + 10 * (self.num_of_slots - 1)) / 2
        for i in range(self.num_of_slots):
            dx = (10 + self.width) * i

            # остовная текстура
            arcade.draw_lbwh_rectangle_filled(
                x + dx,
                10,
                self.width,
                self.height,
                arcade.color.GRAY
            )

            # каёмка
            arcade.draw_lbwh_rectangle_outline(
                x + dx,
                10,
                self.width,
                self.height,
                arcade.color.BLACK,
                2
            )

        # Отрисовка выбранного слота
        arcade.draw_lbwh_rectangle_filled(
            5 + x + (10 + self.width) * self.current_slot,
            15,
            self.width - 10,
            self.height - 10,
            (90, 90, 90),
        )
        
        # Отрисовать текстукур item, которые есть в инвентаре 
        for ind in range(self.num_of_slots):
            if self.slots[ind] is not None:
                arcade.draw_sprite(self.slots[ind])

    def get_textures(self):
        """ 
        Функция для получения текстур item'ов
        """
        self.slots = self.player.get_items_texture()
        for i in range(len(self.slots)):
            slot = self.slots[i]
            if slot is not None:
                slot.center_x = SCREEN_WIDTH // 2 - ((self.width + 10) * self.num_of_slots  - 10) / 2 + (10 + self.width) * i + self.width / 2
                slot.center_y = 10 + self.height / 2
                slot.width = self.width - 20
                slot.height = self.height - 20