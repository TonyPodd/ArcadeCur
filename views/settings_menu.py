import arcade
import arcade.gui as gui


class SettingsMenu(arcade.View):
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
            text="Настройки", 
            width=200,
            height=100,
            font_size=25,
            bold=True,
        )
        self.box_layout.add(menu_text)
        
        # остальные кнопки
        ...
        
        # Назад
        back_button = gui.UIFlatButton(
            text="Назад", width=self.button_width
        )
        back_button.on_click = self.go_back
        self.box_layout.add(back_button)

    def on_draw(self):
        self.clear()
        self.manager.draw()

    def go_back(self, enent):
        self.manager.disable()
        self.prev_view.manager.enable()
        self.window.show_view(self.prev_view)