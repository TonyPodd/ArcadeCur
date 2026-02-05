import arcade
import arcade.gui as gui


class PauseMenu(arcade.View):
    def __init__(self, prev_view = None, background_color = None):
        super().__init__()
        
        self.prev_view = prev_view

        # Менеджер интерфейса
        self.manager = gui.UIManager()
        self.manager.enable()

        self.anchor_layout = gui.UIAnchorLayout()
        self.box_layout = gui.UIBoxLayout(vertical=True, space_between=10)
        
        self.button_width = 200
        
        self.setup_widgets()
        
        self.anchor_layout.add(self.box_layout)
        self.manager.add(self.anchor_layout)

    def setup_widgets(self):
        # Текст
        menu_text = gui.UITextArea(
            text="Pause", 
            width=200,
            height=100,
            font_size=25,
            bold=True,
        )
        self.box_layout.add(menu_text)
        
        # Продолжить
        continue_button = gui.UIFlatButton(
            text="Продолжить", width=self.button_width
        )
        continue_button.on_click = self.go_game
        self.box_layout.add(continue_button)
        
        # settings
        settings_button = gui.UIFlatButton(
            text="Настройки", width=self.button_width
        )
        settings_button.on_click = self.go_settigns
        self.box_layout.add(settings_button)
        
        # в меню
        main_menu_button = gui.UIFlatButton(
            text="Назад", width=self.button_width
        )
        main_menu_button.on_click = self.go_main_menu
        self.box_layout.add(main_menu_button)

    def on_draw(self):
        self.clear()
        self.prev_view.on_draw()
        self.manager.draw()

    def go_main_menu(self, event):
        self.manager.disable()
        from .main_menu import MainMenu
        self.window.show_view(MainMenu())

    def go_settigns(self, event):
        self.manager.disable()
        from .settings_menu import SettingsMenu
        self.window.show_view(SettingsMenu(self))
        
    def go_game(self, event):
        self.manager.disable()
        self.prev_view.update_settings()
        self.window.show_view(self.prev_view)