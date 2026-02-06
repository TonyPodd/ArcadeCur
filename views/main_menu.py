import arcade
import arcade.gui as gui

# from game import GameView
from scripts import load_settings
from config import *


class MainMenu(arcade.View):
    def __init__(self):
        super().__init__()
        self.settings = load_settings()
        
        if self.window.width != self.settings['resolution'][0]:
            self.window.set_size(*self.settings['resolution'])
            self.window.center_window()

        # Менеджер интерфейса
        self.manager = gui.UIManager()
        self.manager.on_resize(*self.settings['resolution'])
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
            text="MENU", 
            width=200,
            height=100,
            font_size=25,
            bold=True,
        )
        self.box_layout.add(menu_text)
        # Новая игра
        new_game_button = gui.UIFlatButton(
            text="Новая игра", width=self.button_width
        )
        new_game_button.on_click = self.new_game
        self.box_layout.add(new_game_button)

        # # Продолжить игру
        # continue_game_button = gui.UIFlatButton(
        #     text="Продолжить игру", width=self.button_width
        # )
        # continue_game_button.on_click = self.continue_game
        # self.box_layout.add(continue_game_button)
        
        # Настройки
        settings_button = gui.UIFlatButton(
            text="Настройки", width=self.button_width
        )
        settings_button.on_click = self.settings_menu
        self.box_layout.add(settings_button)
        
        # выйти
        exit_button = gui.UIFlatButton(
            text="Выйти", width=self.button_width
        )
        exit_button.on_click = self.exit_game
        self.box_layout.add(exit_button)
    
    def on_show_view(self) -> None:
        arcade.set_background_color(arcade.color.AMAZON)

    def on_draw(self):
        self.clear()
        self.manager.draw()
    
    def new_game(self, event):
        self.manager.disable()
        from game import GameView
        game_view = GameView()
        game_view.setup()
        self.on_hide_view()
        self.window.show_view(game_view)
    
    def continue_game(self, event):
        print('continue game')
    
    def settings_menu(self, event):
        self.manager.disable()
        from .settings_menu import SettingsMenu
        self.window.show_view(SettingsMenu(self))

    def exit_game(self, event):
        self.manager.disable()
        arcade.exit()