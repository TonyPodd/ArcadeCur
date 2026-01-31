import arcade
import math

from entities import Player, Wall
from systems import PhysicsSystem, GameCamera
from scripts.gui import HealthBar, InventorySlots
from levels import Level
import config


class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.DARK_GREEN)

    def setup(self):
        # Алерты
        self.alerts = []

        # Координаты мышки на экране
        self.mouse_x = 0
        self.mouse_y = 0
        self.player_angel_view = 0  # Угол в под которым смотрит игрок

        # Player
        self.player = Player(0, 0)
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)

        # UI
        self.haelth_bar = HealthBar(self.player)
        self.inventory_ui = InventorySlots(self.player)

        # Камера
        self.camera = GameCamera()  # камера игрока
        self.gui_camera = arcade.camera.Camera2D()  # камера интерфейса
        self.camera.set_position(0, 0)

        # Уровни
        self.all_levels = list()  # все уровни
        self.current_level_number = 0  # Какой сейчс уровень
        self.current_room, self.current_room_type = 0, 'None'
        self.create_level('start')  # Стартовый уровень
        self.push_alert("Локация: Старт")

        # Пули
        self.bullets = arcade.SpriteList()

        # Движок коллизии
        self.physics_system = PhysicsSystem(self.player, self.wall_sprites)

    def on_draw(self):
        self.clear()

        # Отрисовка игрового мира с камерой
        self.camera.use()

        # Отрисовывается до игрока
        self.floor_sprites.draw()
        self.door_sprites.draw()

        # отрисовывается вместе с игроком
        self.drawing_sprites.sort(key=lambda x: x.position[1], reverse=True)
        self.drawing_sprites.draw()

        # отрисовываем пули
        self.bullets.draw()

        # Активный предмет у игрока
        self.player.draw_item()

        self.item_sprites_on_floor.draw()

        self.enemy_sprites.draw()

        # Подсказка подбора предмета
        for item in self.item_sprites_on_floor:
            if arcade.check_for_collision(self.player, item):
                arcade.draw_text(
                    f'E - подобрать "{item.name}"',
                    item.center_x,
                    item.center_y + 40,
                    arcade.color.WHITE,
                    font_size=14,
                    anchor_x="center",
                    anchor_y="center"
                )

        arcade.draw_line(
            self.player.center_x,
            self.player.center_y,
            self.player.center_x + math.cos(self.player_angel_view) * 100,
            self.player.center_y + math.sin(self.player_angel_view) * 100,
            arcade.color.RED,
            3
        )

        # Отрисовка UI - щас это координаты, потом что нибудь еще, тип иконка паузы
        self.gui_camera.use()
        self.haelth_bar.draw()
        self.inventory_ui.draw()

        # Координаты игрока
        arcade.draw_text(
            f"X: {int(self.player.center_x)}, Y: {int(self.player.center_y)}",
            10,
            self.window.height - 30,
            arcade.color.WHITE,
            14
        )
        # Комната в которой сейчас игрок
        arcade.draw_text(
            f"Номер комнаты: {self.current_room}, Тип комнаты: {self.current_room_type}",
            10,
            self.window.height - 70,
            arcade.color.WHITE,
            14
        )

        self.draw_alerts()

    def on_update(self, delta_time: float) -> None:
        self.player.update(delta_time)
        self.physics_system.update()
        self.camera.center_on_sprite(self.player, 0.04)
        self.update_alerts(delta_time)

        # смортим в какой комнате игрок
        self.current_room, self.current_room_type = self.all_levels[self.current_level_number].check_room(self.player)
        print(self.current_room, self.current_room_type)

        # Проверка умер ли игрок
        if self.is_dead():
            from views import DeathView
            deathview = DeathView()
            self.window.show_view(deathview)

        # Двигаем пули и удаляем при коллизии со стеной / истечении времени
        for bullet in list(self.bullets):
            bullet.update()
            if arcade.check_for_collision_with_list(bullet, self.wall_sprites):
                self.bullets.remove(bullet)
                continue
            if getattr(bullet, "expired", False):
                self.bullets.remove(bullet)

        # Обновляем сундуки и проверяем открытие
        for chest in self.chest_sprites:
            chest.update()
            if not chest.is_open and arcade.check_for_collision(self.player, chest.trigger):
                chest.open()
                print("СУНДУК ОТКРЫТ")
                item = chest.get_item()
                self.item_sprites_on_floor.append(item)

        # Проверяем возможность подобрать айтем
        for item in self.item_sprites_on_floor:
            if item.is_on_floor and arcade.check_for_collision(self.player, item):
                item.can_interact = True
            else:
                item.can_interact = False

            item.update()

        # Айтемы в инвентаре двигаются вместе с игроком
        for item in self.item_sprites_in_enventory:
            item.update()
        
        # Изменения GUI
        self.haelth_bar.update(delta_time)
        self.inventory_ui.update()

    def on_key_press(self, key, modifiers) -> None:
        # Передвижение игрока
        if key == arcade.key.W:
            self.player.direction['up'] = True
            self.player.last_direction_y = 'up'
        if key == arcade.key.S:
            self.player.direction['down'] = True
            self.player.last_direction_y = 'down'
        if key == arcade.key.A:
            self.player.direction['left'] = True
            self.player.last_direction_x = 'left'
        if key == arcade.key.D:
            self.player.direction['right'] = True
            self.player.last_direction_x = 'right'

        # дэш/перекат/рывок
        if (key == arcade.key.LCTRL or key == arcade.key.LSHIFT) and not self.player.is_roll:
            if self.player.direction['left'] or self.player.direction['right'] \
                or self.player.direction['up'] or self.player.direction['down']:
                self.player.do_roll()

        # Для теста урона
        if key == arcade.key.R:
            self.player.take_damage(10)

        # взаимодействие с предметом
        if (key == arcade.key.E):
            # Проверяем какие предметы есть на полу под игроком
            items_for_grab = arcade.check_for_collision_with_list(
                self.player, self.item_sprites_on_floor
            )
            if items_for_grab:
                item = items_for_grab[0]  # Берём самый первый item

                if item.player is None:
                    sprite = self.player.grab_item(item)

                    print(f'поддобрали предмет {item.name}')
                    
                    # Если есть свободные слоты
                    if sprite is True:
                        self.add_item_to_inventory(item)
                    # Если игрок умер
                    elif sprite is False:
                        pass
                    # Если нет свободных слотов
                    else:
                        self.add_item_to_inventory(item)
                        self.drop_inventory_item(sprite)

        # Выбросить айтем
        if (key == arcade.key.Q):
            dropped_item = self.player.drop_item()
            # Если персонаж умер, то ничего не делать
            if dropped_item is False:
                pass
            
            # Проверяем есть ли item в руках
            elif dropped_item is not None:
                self.drop_inventory_item(dropped_item)

        # переключение слотов
        if key in (arcade.key.NUM_1, arcade.key.KEY_1):
            self.player.current_slot = 0

        if key in (arcade.key.NUM_2, arcade.key.KEY_2):
            self.player.current_slot = 1

        # Взаимодействия с интерфейсом
        # Пауза
        if key == arcade.key.ESCAPE:
            from views import PauseView
            pause = PauseView(self)
            self.window.show_view(pause)

    def on_key_release(self, key, modifiers) -> None:
        if key == arcade.key.W:
            self.player.direction['up'] = False
        if key == arcade.key.S:
            self.player.direction['down'] = False
        if key == arcade.key.A:
            self.player.direction['left'] = False
        if key == arcade.key.D:
            self.player.direction['right'] = False

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT and not self.player.is_dead:
            item = self.player.first_item if self.player.current_slot == 0 else self.player.second_item
            if item != None and hasattr(item, "shoot"):
                new_bullets = item.shoot()
                if new_bullets != None:
                    for cur_b in new_bullets:
                        self.bullets.append(cur_b)

    def add_item_to_inventory(self, item):
        self.item_sprites_on_floor.remove(item)
        if item not in self.item_sprites_in_enventory:
            self.item_sprites_in_enventory.append(item)
        item.grab(self.player)

    def drop_inventory_item(self, item):
        if item in self.item_sprites_in_enventory:
            self.item_sprites_in_enventory.remove(item)
        if item not in self.item_sprites_on_floor:
            self.item_sprites_on_floor.append(item)
        item.drop()

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_x = x
        self.mouse_y = y

        # Расчет под каким углом сейчас игрок смотрит
        self.player_angel_view = math.atan2(self.mouse_y - self.center_y, self.mouse_x - self.center_x)
        self.player.view_angle = self.player_angel_view

    def is_dead(self) -> bool:
        """ Проверка умер ли игрок """
        if self.player.player_hp <= 0:
            self.player.on_die()
            return True
        return False

    def load_level_sprites(self, level_num: int) -> None:
        """ Загрузка спрайтов с уровня"""

        try:
            self.all_sprites.clear()
        except Exception:
            print('Нет спрайтов')
        try:
            self.wall_sprites.clear()
        except Exception:
            print('Нет спрайтов стен')
        try:
            self.floor_sprites.clear()
        except Exception:
            print('Нет спрайтов пола')
        try:
            self.door_sprites.clear()
        except Exception:
            print('Не спрайтов дверей')

        # спрайты с уровня
        self.all_sprites = self.all_levels[level_num].get_sprites()

        self.drawing_sprites = arcade.SpriteList()  # Спрайты для y-sort отрисовки
        self.drawing_sprites.append(self.player)

        self.wall_sprites = self.all_sprites['wall']
        self.floor_sprites = self.all_sprites['floor']
        self.door_sprites = self.all_sprites['door']
        self.chest_sprites = self.all_sprites.get('chest', arcade.SpriteList())

        self.enemy_sprites = arcade.SpriteList()
        self.item_sprites_on_floor = arcade.SpriteList()
        self.item_sprites_in_enventory = arcade.SpriteList()


        # спрайты для отрисовки, кроме пола
        for sprite in self.wall_sprites:
            self.drawing_sprites.append(sprite)

        # сундуки (если есть)
        for sprite in self.chest_sprites:
            self.drawing_sprites.append(sprite)

    def create_level(self, level_type):
        level = Level(level_type)
        self.all_levels.append(level)
        self.current_level_number = len(self.all_levels) - 1

        self.load_level_sprites(self.current_level_number)

        player_x, player_y = level.get_spawn_coords()
        self.player.set_position(player_x, player_y)
        self.camera.set_position(player_x, player_y)

    def push_alert(self, text, duration = 2.8):
        self.alerts.append({
            "text": text,
            "time": 0.0,
            "duration": duration,
        })

    def update_alerts(self, delta_time):
        for alert in self.alerts:
            alert["time"] += delta_time
        self.alerts = [a for a in self.alerts if a["time"] < a["duration"]]

    def draw_alerts(self):
        if not self.alerts:
            return

        width = min(520, int(self.window.width * 0.6))
        height = 56
        padding = 12
        top_margin = 24

        for i, alert in enumerate(self.alerts):
            t = alert["time"]
            d = alert["duration"]
            fade_in = 0.18
            fade_out = 0.35

            if t < fade_in:
                alpha = t / fade_in
            elif t > d - fade_out:
                alpha = max(0.0, (d - t) / fade_out)
            else:
                alpha = 1.0

            x = self.window.width / 2
            y = self.window.height - top_margin - (height / 2) - i * (height + 10)

            bg_color = (18, 18, 24, int(210 * alpha))
            shadow_color = (0, 0, 0, int(120 * alpha))
            border_color = (255, 255, 255, int(40 * alpha))
            accent_color = (80, 220, 160, int(255 * alpha))

            def draw_rect_filled(cx, cy, w, h, color):
                left = cx - w / 2
                right = cx + w / 2
                bottom = cy - h / 2
                top = cy + h / 2
                arcade.draw_lrbt_rectangle_filled(left, right, bottom, top, color)

            def draw_rect_outline(cx, cy, w, h, color, border_width=1):
                left = cx - w / 2
                right = cx + w / 2
                bottom = cy - h / 2
                top = cy + h / 2
                arcade.draw_lrbt_rectangle_outline(left, right, bottom, top, color, border_width)

            # Тень
            draw_rect_filled(x, y - 3, width, height, shadow_color)
            # Фон
            draw_rect_filled(x, y, width, height, bg_color)
            # Левая полоска
            draw_rect_filled(
                x - width / 2 + 6,
                y,
                4,
                height - 12,
                accent_color
            )
            # рамка
            draw_rect_outline(x, y, width, height, border_color, 2)

            arcade.draw_text(
                alert["text"],
                x,
                y,
                arcade.color.WHITE,
                font_size=16,
                anchor_x="center",
                anchor_y="center"
            )
