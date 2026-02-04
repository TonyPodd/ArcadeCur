import arcade
import math

from entities import Player, Chest
from systems import PhysicsSystem, GameCamera
from scripts.gui import HealthBar, InventorySlots, OrbUi, EnemyUi
from levels import Level
import config


class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.DARK_GREEN)
        self.perf_graph_list = arcade.SpriteList()
        self.fps_graph = arcade.PerfGraph(150, 50, "FPS")
        self.fps_graph.center_x = 75
        self.fps_graph.center_y = 25
        self.perf_graph_list.append(self.fps_graph)

    def setup(self):
        self.collision_sprites = arcade.SpriteList()
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
        self.item_sprites_in_enventory = arcade.SpriteList()
        self.in_fight = False  # Идёт ли сейчас сражение
        self.money = 0  # кол-во денег
        self.orbs = 0  # кол-во орбов

        # UI
        self.haelth_bar = HealthBar(self.player)
        self.inventory_ui = InventorySlots(self.player)
        self.orb_ui = OrbUi()
        self.enemy_counter_ui = EnemyUi()

        # Камера
        self.camera = GameCamera()  # камера игрока
        self.gui_camera = arcade.camera.Camera2D()  # камера интерфейса
        self.camera.set_position(0, 0)

        # Движок коллизии
        self.physics_system = PhysicsSystem(self.player, self.collision_sprites)
        self.enemy_physics = []

        # Уровни
        self.all_levels = list()  # все уровни
        self.current_level_number = 0  # Какой сейчс уровень
        self.current_room, self.current_room_type = 0, 'None'
        self.create_level('start')  # Стартовый уровень
        self.push_alert("Локация: Старт")


        self.enemy_bullets = arcade.SpriteList()

    def on_draw(self):
        self.clear()

        # Отрисовка игрового мира с камерой
        self.camera.use()

        # Отрисовывается до игрока
        self.floor_sprites.draw()
        self.door_sprites.draw()
        self.interactive_sprites.draw()
        for sprite in self.counter_sprites:
            sprite.draw_item()

        # отрисовывается вместе с игроком
        self.drawing_sprites.sort(key=lambda x: x.bottom, reverse=True)
        self.drawing_sprites.draw()

        # отрисовываем пули
        self.bullets.draw()
        self.enemy_bullets.draw()

        # Активный предмет у игрока
        self.player.draw_item()
        self.item_sprites_on_floor.draw()
        self.enemy_sprites.draw()

        # Линия с хп врагов
        for enemy in self.enemy_sprites.sprite_list:
            enemy.draw_hp()
            enemy.draw_item()

        self.orb_sprites.draw()
        self.money_sprites.draw()

        arcade.draw_line(
            self.player.center_x,
            self.player.center_y,
            self.player.center_x + math.cos(self.player_angel_view) * 100,
            self.player.center_y + math.sin(self.player_angel_view) * 100,
            arcade.color.RED,
            3
        )

        # ui
        for sprite in self.interactive_sprites:
            sprite.draw_tips()

        # Интерфейс объектов взаимодействия
        for object in self.interactive_sprites:
            object.draw_ui()

        # Отрисовка UI игрока
        self.gui_camera.use()

        # Подсказка подбора предмета
        items_nearby = arcade.check_for_collision_with_list(self.player, self.item_sprites_on_floor)
        if items_nearby:
            for item in items_nearby:
                arcade.draw_text(
                    f'E - подобрать "{item.name}"',
                    item.center_x,
                    item.center_y + 40,
                    arcade.color.WHITE,
                    font_size=14,
                    anchor_x="center",
                    anchor_y="center"
                )

        self.haelth_bar.draw()
        self.inventory_ui.draw()
        self.orb_ui.draw()

        if self.in_fight:
            self.enemy_counter_ui.draw()

        # Координаты игрока
        # arcade.draw_text(
        #     f"X: {int(self.player.center_x)}, Y: {int(self.player.center_y)}",
        #     10,
        #     self.window.height - 30,
        #     arcade.color.WHITE,
        #     14
        # )
        # Комната в которой сейчас игрок
        # arcade.draw_text(
        #     f"Номер комнаты: {self.current_room_num}, Тип комнаты: {self.current_room_type}",
        #     10,
        #     self.window.height - 70,
        #     arcade.color.WHITE,
        #     14
        # )
        self.perf_graph_list.draw()

        self.draw_alerts()
        

    def on_update(self, delta_time: float) -> None:
        self.player.update(delta_time)
        self.physics_system.update()
        self.camera.update(delta_time)
        self.camera.center_on_sprite(self.player, 0.1)
        self.update_alerts(delta_time)

        # смортим в какой комнате игрок
        collide_floor = self.check_current_room()

        # Начинаем бой если тип комнаты - fight, и она не зачищена
        if self.current_room not in self.all_levels[self.current_level_number].completed_rooms:
            if self.current_room_type == 'fight':
                self.start_fight(collide_floor)

        # Заканчиваем бой, если враги - всё
        if self.in_fight and not self.enemy_sprites.sprite_list:
            self.end_fight()

        # Проверка умер ли игрок
        if self.is_dead():
            from views import DeathView
            deathview = DeathView()
            self.window.show_view(deathview)

        self.enemy_sprites.update(delta_time)

        # коллизия со стенами для енеми
        for engine in self.enemy_physics:
            engine.update()

        # Двигаем пули
        self.bullets.update(delta_time)
        self.enemy_bullets.update(delta_time)

        # Обновляем врагов и переносим их пули в общий список
        # обновляем углы оружий енеми
        for enemy in self.enemy_sprites.sprite_list:
            dead, orbs, money = enemy.death_check()

            if not dead:
                enemy.weapon.update()
                if enemy.spawned_bullets:
                    self.enemy_bullets.extend(enemy.spawned_bullets)
                    enemy.spawned_bullets.clear()

            else:
                # получение денег и орбов
                if orbs is not None:
                    self.orb_sprites.extend(orbs)

                if money is not None:
                    self.money_sprites.extend(money)

        self.interactive_sprites.update(delta_time)

        # Проверяем коллизию врагов с пулями
        self.enemy_collision_with_bullet()

        # Проверяем коллизию игрока с пулями
        self.player_collision_with_bullet()

        # удаляем при коллизии со стеной / истечении времени
        self.bullet_collision_with_wall()

        self.interactive_sprites.update()
        self.engine_sprites.sprite_list[0]
        self.trigger_collision()

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

        # Всасывание орбов
        self.orb_sprites.update(delta_time, self.player.position)
        self.money_sprites.update(delta_time, self.player.position)

        # Подбор орбов
        for sprite in arcade.check_for_collision_with_list(self.player, self.money_sprites):
            self.money += sprite.picked_up()
        for sprite in arcade.check_for_collision_with_list(self.player, self.orb_sprites):
            self.orbs += sprite.picked_up()

        # Изменения GUI
        self.haelth_bar.update(delta_time)
        self.inventory_ui.update()
        self.orb_ui.update(self.orbs, self.money)
        if self.in_fight:
            self.enemy_counter_ui.update(len(list(self.enemy_sprites)))

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
            if any(self.player.direction.values()):
                self.player.do_roll()

        if (key == arcade.key.E):
            # Проверяем какие предметы есть на полу под игроком
            items_for_grab = arcade.check_for_collision_with_list(
                self.player, self.item_sprites_on_floor
            )
            interactive_objects = arcade.check_for_collision_with_list(self.player, self.interactive_sprites)
            counter_sprites = arcade.check_for_collision_with_list(self.player, self.counter_sprites)

            # взаимодействие с предметом
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
            
            elif counter_sprites:
                for counter in counter_sprites:
                    if counter.interaction:
                        delta_money, item = counter.use(self.money)
                        if item is not None:

                            self.money -= delta_money
                            self.item_sprites_on_floor.append(item)
                            self.interaction = False
                        continue

            elif interactive_objects:
                object_sprite = interactive_objects[0]  # Первый объект
                item = object_sprite.use()
                if item is not None:
                    self.item_sprites_on_floor.append(item)
                    self.interactive_sprites.remove(object_sprite)

        # Выбросить айтем
        if (key == arcade.key.Q):
            dropped_item = self.player.drop_item()
            # Если персонаж умер, то ничего не делать
            if dropped_item is False:
                pass

            # Проверяем есть ли item в руках
            elif dropped_item is not None:
                self.drop_inventory_item(dropped_item)
        
        # Заправить движок
        if key == arcade.key.R:
            engin = self.engine_sprites.sprite_list[0]
            if engin.is_used:
                self.orbs -= engin.set_value(self.orbs)
        
        if key == arcade.key.SPACE:
            # Переход некст локу
            engin = self.engine_sprites.sprite_list[0]
            if engin.is_used:
                if engin.is_full:
                    self.create_level()

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
                    self.bullets.extend(new_bullets)

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
        if self.player.hp <= 0:
            self.player.on_die()
            return True
        return False

    def clear_all_spriteLists(self):
        
        try:
            self.all_sprites.clear()
        except Exception:
            ...
        try:
            self.wall_sprites.clear()
        except Exception:
            ...
        try:
            self.floor_sprites.clear()
        except Exception:
            ...
        try:
            self.door_sprites.clear()
        except Exception:
            ...
        try:
            self.enemy_sprites.clear()
        except Exception:
            ...
        try:
            self.bullets.clear()
        except Exception:
            ...
        try:
            self.orb_sprites.clear()
        except Exception:
            ...
        try:
            self.money_sprites.clear()
        except Exception:
            ...
        try:
            self.interactive_sprites.clear()
        except Exception:
            ...
        try:
            self.chest_sprites.clear()
        except Exception:
            ...
        try:
            self.engine_sprites.clear()
        except Exception:
            ...
        try:
            self.collision_sprites.clear()
        except Exception:
            ...
        try:
            self.drawing_sprites.clear()
        except Exception:
            ...
        try:
            self.counter_sprites.clear()
        except Exception:
            ...
        try:
            self.item_sprites_on_floor.clear()
        except Exception:
            ...

    def load_level_sprites(self, level_num: int) -> None:
        """ Загрузка спрайтов с уровня"""
        self.clear_all_spriteLists()

        # спрайты с уровня
        self.all_sprites = self.all_levels[level_num].get_sprites()

        self.wall_sprites = self.all_sprites['wall']
        self.floor_sprites = self.all_sprites['floor']
        self.door_sprites = self.all_sprites['door']
        self.interactive_sprites = self.all_sprites['interactive']
        self.engine_sprites = self.all_sprites['engine']
        self.counter_sprites = self.all_sprites['counter']
        self.chest_sprites = self.all_sprites.get('chest', arcade.SpriteList())
        self.enemy_sprites = self.all_sprites.get('enemy', arcade.SpriteList())

        self.drawing_sprites = arcade.SpriteList()  # Спрайты для y-sort отрисовки
        self.collision_sprites = arcade.SpriteList(use_spatial_hash=True)
        self.bullets = arcade.SpriteList()
        self.orb_sprites = arcade.SpriteList()
        self.money_sprites = arcade.SpriteList()
        self.item_sprites_on_floor = arcade.SpriteList()

        # Добавление спрайтов для отрисовки
        self.drawing_sprites.append(self.player)
        self.drawing_sprites.extend(self.wall_sprites)
        self.drawing_sprites.extend(self.chest_sprites)
        
        # Тестовые трюки с оптимизацией
        self.money_sprites.use_spatial_hash = True
        self.orb_sprites.use_spatial_hash = True
        self.chest_sprites.is_static = True
        self.wall_sprites.use_spatial_hash = True
        self.wall_sprites.is_static = True
        self.door_sprites.is_static = True
        self.floor_sprites.is_static = True

        # Спрайты с коллизией с игроком
        self.collision_sprites.extend(self.wall_sprites)

    def create_level(self, level_type='default'):
        level = Level(level_type)
        self.all_levels.append(level)
        self.current_level_number = len(self.all_levels) - 1

        self.load_level_sprites(self.current_level_number)

        player_x, player_y = level.get_spawn_coords()
        self.player.set_position(player_x, player_y)
        self.camera.set_position(player_x, player_y)
        self.physics_system.set_new_collision_sprites(self.collision_sprites)

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

    def check_doors(self):
        """
        Првоерка находятся ли закрытые и открытые двери в своих спрайт листах
        """

        for sprite in self.all_sprites['door']:
            # Если закрыта и не в спрайтах коллизии
            if sprite.is_close and sprite not in self.collision_sprites:
                self.collision_sprites.append(sprite)

            # Если дверь открыта и в спрайтах коллизии, то убрать
            elif sprite in self.collision_sprites:
                self.collision_sprites.remove(sprite)

    def check_current_room(self) -> arcade.SpriteList:
        """
        Определяет комнату, в которой игрок
        """
        floor_sprites = arcade.SpriteList()

        self.current_room_num, self.current_room_type, list_floor_sprites = self.all_levels[self.current_level_number].check_room(self.player)
        if self.current_room_num != 0:
            self.current_room = self.all_levels[self.current_level_number].rooms[self.current_room_num]

        # Добавляет спрайты пола из массива в спрайт лист
        for sprite in list_floor_sprites:
            floor_sprites.append(sprite)

        return floor_sprites

    def bullet_collision_with_wall(self) -> None:
        """
        Проверка сталкивается ли пуля со стеной \n
        """
        for bullet_list in [self.bullets, self.enemy_bullets]:
            for bullet in bullet_list:
                if bullet.damage_type != 'hit':
                    if arcade.check_for_collision_with_list(bullet, self.collision_sprites):
                        bullet.kill()

    def enemy_collision_with_bullet(self) -> None:
        """
        Провеяем задела ли врага пуля \n
        Если да, то враг получает урон
        """

        for enemy in self.enemy_sprites.sprite_list:
            collide_bullets = arcade.check_for_collision_with_list(enemy, self.bullets)

            for bullet in collide_bullets:
                # Наносим урон врагу, если он с ней не сталкивался
                if bullet not in enemy.bullets_hitted:
                    enemy.take_damage(bullet.damage)
                    if bullet.damage_type == 'bullet':
                        self.bullets.remove(bullet)
                        bullet.kill()
                        continue
                    # добавляем пули к уже столкнувшимся
                    enemy.bullets_hitted.add(bullet)

    def player_collision_with_bullet(self) -> None:
        """
        Провеяем задела ли игроока пуля \n
        Если да, то получаем урон
        """

        collide_bullets = arcade.check_for_collision_with_list(self.player, self.enemy_bullets)

        for bullet in collide_bullets:
            # Впитываем урон, если не сталкивались с пуей
            if bullet not in self.player.bullets_hitted:
                self.player.take_damage(bullet.damage)
                self.camera.shake(12, 0.2)
                if bullet.damage_type == 'bullet':
                    self.enemy_bullets.remove(bullet)
                    bullet.kill()
                    continue
                # добавляем пули к уже столкнувшимся
                self.player.bullets_hitted.append(bullet)

    def start_fight(self, collide_floor: arcade.SpriteList):
        self.all_levels[self.current_level_number].completed_rooms.append(self.current_room)
        self.enemy_sprites = self.current_room.begin_fight()

        # Спрайты коллизии для врагов
        self.enemy_col_sprites = arcade.SpriteList(use_spatial_hash=True)
        self.enemy_col_sprites.extend(self.current_room.all_sprites['wall'])
        self.enemy_col_sprites.extend(self.current_room.all_sprites['door'])

        for enemy in self.enemy_sprites:
            engine = arcade.PhysicsEngineSimple(enemy, self.enemy_col_sprites)
            self.enemy_physics.append(engine)

        for enemy in self.enemy_sprites:
            enemy.player = self.player
            enemy.walls = self.current_room.all_sprites['wall']

        # Проверяем закрылись ли двери
        self.check_doors()

        # Перемещаям игрока на кординаты пола перед дверью
        floor = collide_floor.sprite_list[0]
        x, y = floor.center_x, floor.center_y
        self.player.set_position(x, y)
        self.in_fight = True
        
        self.enemy_counter_ui.set_num_of_enemy(len(list(self.enemy_sprites)))
        self.push_alert("Локация: 'Fight'")

    def end_fight(self):
        self.current_room.end_fight()
        # чистим коллизии/движки врагов, чтобы не копились между комнатами
        for enemy in list(self.enemy_sprites.sprite_list):
            if enemy in self.collision_sprites:
                self.collision_sprites.remove(enemy)
        self.enemy_sprites = arcade.SpriteList()
        self.enemy_physics.clear()
        self.enemy_col_sprites.clear()
        self.enemy_bullets = arcade.SpriteList()

        # Проверяем закрылись ли двери
        self.check_doors()
        self.in_fight = False

    def trigger_collision(self):
        """ Проверка сталкивается ли игрок с интерактивным объектом """
        collision_sprites = arcade.check_for_collision_with_list(self.player, self.interactive_sprites)
        for s in self.interactive_sprites:
            s.tips = False
            if s not in collision_sprites:
                s.is_used = False

        for sprite in collision_sprites:
            sprite.tips = True
