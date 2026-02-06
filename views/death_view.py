import arcade


class DeathView(arcade.View):
    def __init__(self, result: dict=None):
        super().__init__()
        """ Экран после смерти """
        
        if result is not None:
            self.result = result
        else:
            self.result = dict()
    
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
        
        x = self.window.width / 3 * 2
        y = self.window.height / 3 + 50
        arcade.draw_text(
            'Результаты:',
            x,
            y
        )
        for name in self.result:
            y -= 20
            # Название раздела
            arcade.draw_text(
                name,
                x,
                y
            )
            arcade.draw_text(
                self.result[name],
                x + 300,
                y
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
            from views import MainMenu
            menu = MainMenu()
            self.window.show_view(menu)
