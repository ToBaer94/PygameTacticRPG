import pygame as pg
from os import pardir, path
from buttons.button import Button
from buttons.wait_button import WaitButton
from buttons.attack_button import AttackButton

ui_dir = path.join(path.dirname(__file__), "assets", "ui")
button_dir = path.join(ui_dir, "buttons")


class UISystem(object):
    def __init__(self, game_manager):
        super(UISystem, self).__init__()

        self.game_manager = game_manager
        self.buttons = []

        self.button_dict = {"wait": WaitButton(path.join(button_dir, "wait_button.png"), 60, 50, self),
                            "attack": AttackButton(path.join(button_dir, "attack_button.png"), 60, 50, self)
                            }

        self.ui_background = Button(path.join(ui_dir, "ui_background.png"), 50, 50, self)
        self.combat_ui_background = Button(path.join(ui_dir, "combat_ui_background.png"), 50, 50, self)

        self.add_button("wait")

        self.states = {"0": "Inactive",
                       "1": "action_ui",
                       "2": "attack_ui"}

        self.state = self.states["0"]

        self.battle_stats = []

    def get_event(self, event, pos):
        if self.state == self.states["1"]:
            for button in self.buttons:
                if button.rect.collidepoint(pos):
                    button.get_clicked()

    def add_button(self, button):
        if self.button_dict[button] not in self.buttons:
            self.buttons.append(self.button_dict[button])

    def remove_button(self, button):
        if self.button_dict[button] in self.buttons:
            self.buttons.remove(self.button_dict[button])

    def reset_buttons(self):
        self.buttons = []
        self.add_button("wait")
        self.battle_stats = []

    def set_ui_position(self, position):
        if position.x > 550:
            x_pos = position.x - 40 - 200
        else:
            x_pos = position.x + 40
        y_pos = position.y

        self.ui_background.set_position((x_pos, y_pos))
        for i, button in enumerate(self.buttons):
            button.set_position((x_pos + 25, y_pos + 300 - 85 * (i+1)))

    def create_battle_stats_ui(self, hero, enemy, hit_crit):
        font = pg.font.Font(None, 24)
        black = pg.Color("black")

        enemy_hit_stats = hit_crit[0]
        enemy_hit = enemy_hit_stats[0]
        enemy_crit = enemy_hit_stats[1]

        hero_hit_stats = hit_crit[1]
        hero_hit = hero_hit_stats[0]
        hero_crit = hero_hit_stats[1]

        e_hp = font.render(str(enemy.hp), 1, black)
        e_hp_pos = e_hp.get_rect(center=(self.ui_background.rect.x + 35, self.ui_background.rect.y + 75))

        e_atk = font.render(str(enemy.attack), 1, black)
        e_atk_pos = e_atk.get_rect(center=(self.ui_background.rect.x + 35, self.ui_background.rect.y + 107))

        e_hit = font.render(str(enemy_hit), 1, black)
        e_hit_pos = e_hit.get_rect(center=(self.ui_background.rect.x + 35, self.ui_background.rect.y + 145))

        e_crit = font.render(str(enemy_crit), 1, black)
        e_crit_pos = e_crit.get_rect(center=(self.ui_background.rect.x + 35, self.ui_background.rect.y + 185))



        h_hp = font.render(str(hero.hp), 1, black)
        h_hp_pos = h_hp.get_rect(center=(self.ui_background.rect.x + 170, self.ui_background.rect.y + 75))

        h_atk = font.render(str(hero.attack), 1, black)
        h_atk_pos = h_atk.get_rect(center=(self.ui_background.rect.x + 170, self.ui_background.rect.y + 107))

        h_hit = font.render(str(hero_hit), 1, black)
        h_hit_pos = h_hit.get_rect(center=(self.ui_background.rect.x + 170, self.ui_background.rect.y + 145))

        h_crit = font.render(str(hero_crit), 1, black)
        h_crit_pos = h_crit.get_rect(center=(self.ui_background.rect.x + 170, self.ui_background.rect.y + 185))

        self.battle_stats = [[e_hp, e_hp_pos], [e_atk, e_atk_pos], [e_hit, e_hit_pos], [e_crit, e_crit_pos],
                             [h_hp, h_hp_pos], [h_atk, h_atk_pos], [h_hit, h_hit_pos], [h_crit, h_crit_pos]
                             ]

    def draw(self, screen):
        if self.state == self.states["1"]:

            screen.blit(self.ui_background.image, self.ui_background.rect)

            for button in self.buttons:
                button.draw(screen)

        elif self.state == self.states["2"]:
            screen.blit(self.combat_ui_background.image, self.ui_background.rect)
            for stat in self.battle_stats:
                screen.blit(stat[0], stat[1])


