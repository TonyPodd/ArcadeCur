import arcade
import arcade.gui as gui
import json

from scripts import load_settings


class SettingsMenu(arcade.View):
    def __init__(self, prev_view = None, background_color = None):
        super().__init__()
        
        self.prev_view = prev_view
        
        self.settings = load_settings()

        # Менеджер интерфейса
        self.manager = gui.UIManager()
        self.manager.enable()

        self.anchor_settings = gui.UIAnchorLayout()
        self.settigns_layout = gui.UIBoxLayout(vertical=True, space_between=10, height= 600)
        
        self.button_width = 200
        
        self.setup_widgets()
        
        self.anchor_settings.add(self.settigns_layout)
        self.manager.add(self.anchor_settings)

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
        self.settigns_layout.add(menu_text)

        # settigns
        self.setup_sounds()
        self.setup_screen()

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

        self.settigns_layout.add(lower_layout)

    def setup_screen(self):
        """ Раздел экрана """
        screen_layout = gui.UIBoxLayout(vertical=True, space_between=10)
        
        # текст раздела
        text = gui.UITextArea(
            text="Экран", 
            width=100,
            height=40,
            font_size=20,
            bold=True
        )
        screen_layout.add(text)
        
        # Разрешение экрана
        screen_resolution_text = gui.UIBoxLayout(vertical=False)
        text = gui.UITextArea(
            text='Разрешение:',
            width=60,
            height=20,
            font_size=14,
        )
        screen_resolution_text.add(text)
        
        self.resolution_variants = gui.UIDropdown(
            options=[
                '1920x1080', '1280x720', '800x600', '640x480'
            ],
            width=self.button_width
        )
        self.resolution_variants.value = f'{self.settings["resolution"][0]}x{self.settings["resolution"][1]}'
        self.resolution_variants.on_change = self.set_resolution
        screen_layout.add(self.resolution_variants)

        self.settigns_layout.add(screen_layout)

    def setup_sounds(self):
        """ Раздел звука """
        # Звуки
        sound_layout = gui.UIBoxLayout(vertical=True, space_between=10)

        # текст раздела
        text = gui.UITextArea(
            text="Звуки", 
            width=100,
            height=40,
            font_size=20,
            bold=True
        )
        sound_layout.add(text)

        # Громкасть звуков игры
        volume_layout = gui.UIBoxLayout(vertical=False)
        volume_text = gui.UITextArea(
            text="SFX:", 
            width=60,
            height=20,
            font_size=14,
        )
        volume_layout.add(volume_text)
        
        #Ползунок звуков
        self.volume_slider = gui.UISlider(
            width=200, height=20, min_value=0, max_value=100, value=100 * self.settings['sound_volume']
        )
        volume_layout.add(self.volume_slider)
        sound_layout.add(volume_layout)
        self.settigns_layout.add(sound_layout)

    def on_draw(self):
        self.clear()
        self.manager.draw()

    def go_back(self, enent):
        self.manager.disable()
        self.prev_view.manager.enable()
        self.window.show_view(self.prev_view)

    def save_settigns(self, event):
        # Загрузка старых настроек
        with open(file='settings.json', mode='r', encoding='utf-8') as file:
            data = json.load(file)

        # обновление настроек
        data['sound_volume'] = self.volume_slider.value / 100
        data['resolution'] = self.settings['resolution']
        
        # Применяем новые
        if self.window.width != self.settings['resolution'][0]:
            self.window.set_size(*self.settings['resolution'])
            self.window.center_window()
            
            self.manager.on_resize(*self.settings['resolution'])
            self.prev_view.manager.on_resize(*self.settings['resolution'])
        
        self.window.set_fullscreen(self.settings['fullscreen'])

        # загрузить обновление
        with open(file='settings.json', mode='w', encoding='utf-8') as file:
            file.write(json.dumps(data))

    def set_resolution(self, event):
        """ Новое разрешение """

        self.settings['resolution'] = tuple(map(int, self.resolution_variants.value.split('x')))