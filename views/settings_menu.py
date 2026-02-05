import arcade
import arcade.gui as gui
import json


class SettingsMenu(arcade.View):
    def __init__(self, prev_view = None, background_color = None):
        super().__init__()
        
        self.prev_view = prev_view
        
        self.load_settings_from_file()

        # Менеджер интерфейса
        self.manager = gui.UIManager()
        self.manager.enable()

        self.anchor_layout = gui.UIAnchorLayout()
        self.anchor_settings = gui.UIAnchorLayout()
        
        self.box_layout = gui.UIBoxLayout(vertical=True, space_between=10)
        self.settigns_layout = gui.UIBoxLayout(vertical=True, space_between=10)
        
        self.button_width = 200
        
        self.setup_widgets()
        
        self.anchor_layout.add(self.box_layout)
        self.anchor_settings.add(self.settigns_layout)
        self.settigns_layout
        self.manager.add(self.anchor_layout)
        self.manager.add(self.anchor_settings)

    def load_settings_from_file(self):
        with open(file='settigns.json', mode='r', encoding='utf-8') as file:
            data = json.load(file)

        self.volume_sound = data['sound_volume']

    def setup_widgets(self):
        # buttons
        # Текст
        menu_text = gui.UITextArea(
            text="Настройки", 
            width=200,
            height=100,
            font_size=25,
            bold=True,
        )
        self.box_layout.add(menu_text)

        # остальные кнопки
        ...
        
        # Сохранить & нажать
        lower_layout = gui.UIBoxLayout(vertical=False, space_between=10)  # layout для кнопок сохранить и назал
        # Назад
        back_button = gui.UIFlatButton(
            text="Назад", width=self.button_width
        )
        back_button.on_click = self.go_back
        lower_layout.add(back_button)
        # save button
        save_button = gui.UIFlatButton(
            text="Сохранить", width=self.button_width
        )
        save_button.on_click = self.save_settigns
        lower_layout.add(save_button)
        self.box_layout.add(lower_layout)
    
        # settigns
        # Громкасть звуков
        volume_layout = gui.UIBoxLayout(vertical=False)
        volume_text = gui.UITextArea(
            text="Звуки:", 
            width=60,
            height=20,
            font_size=14,
        )
        volume_layout.add(volume_text)
        self.volume_slider = gui.UISlider(
            width=200, height=20, min_value=0, max_value=100, value=100 * self.volume_sound
        )
        volume_layout.add(self.volume_slider)
        self.settigns_layout.add(volume_layout)

    def on_draw(self):
        self.clear()
        self.manager.draw()

    def go_back(self, enent):
        self.manager.disable()
        self.prev_view.manager.enable()
        self.window.show_view(self.prev_view)

    def save_settigns(self, event):
        # Сохранение в файл
        ...