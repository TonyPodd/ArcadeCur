import arcade

from views import MenuView

class DeathView(arcade.View):
    def __init__(self):
        super().__init__()
        
        """ Экран после смерти """
    
    def on_draw(self) -> None:
        self.clear()
        
        arcade.draw_text(
            "СМЕРТЬ ТЕБЯ НАСТИГЛА",
            self.window.width / 2,
            self.window.height / 2 + 50,
            arcade.color.WHITE,
            font_size=50,
            anchor_x="center"
        )
        
        arcade.draw_text(
            "ESC - Выход в меню",
            self.window.width / 2,
            self.window.height / 2 - 60,
            arcade.color.WHITE,
            font_size=20,
            anchor_x="center"
        )
        
        arcade.draw_text(
            "ENTER - начать новую игру",
            self.window.width / 2,
            self.window.height / 2 - 30,
            arcade.color.WHITE,
            font_size=20,
            anchor_x="center"
        )
    
    def on_key_press(self, key, modifiers) -> None:
        # Вернутся в игру
        if key == arcade.key.ENTER:
            from game import GameView
            game_view = GameView()
            game_view.setup()
            self.window.show_view(game_view)

        # Перейти в меню
        elif key == arcade.key.ESCAPE:
            menu = MenuView()
            self.window.show_view(menu)
