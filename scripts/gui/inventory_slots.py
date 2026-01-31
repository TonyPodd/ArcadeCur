import arcade


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
        ...

    def draw(self):
        # Отрисовка самих слотов словтов
        ...
        
        # Отрисовка выбранного слота
        ...
        
        # Отрисовать текстукур item, которые есть в инвентаре 
        for ind in range(self.num_of_slots):
            if self.slots[ind] is not None:
                ...
    
    def get_textures(self):
        """ 
        Функция для получения текстур item'ов
        """