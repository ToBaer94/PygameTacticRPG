import pygame as pg
import tilerenderer
from os import path, pardir
import Queue

import random

from hero import Hero
from enemy import Enemy
from movement_system import MovementSystem
from ui_system import UISystem

import util

level_dir = path.join(path.dirname(__file__), "assets", "levels", "map.tmx")

Vector = pg.math.Vector2


class Level(object):
    def __init__(self):
        self.tmx_file = path.join(level_dir)
        self.tile_renderer = tilerenderer.Renderer(self.tmx_file)
        self.map_surface = self.tile_renderer.make_map()
        self.map_rect = self.map_surface.get_rect()

        self.tile_width = 32

        self.tile_number_x = int(self.map_rect.width // self.tile_width)
        self.tile_number_y = int(self.map_rect.height // self.tile_width)

        self.valid_movement_tiles = {}

        self.hero_group = pg.sprite.Group()
        hero = Hero()
        self.hero_group.add(hero)

        self.enemy_group = pg.sprite.Group()
        enemy = Enemy(6 * 32, 6 * 32)
        self.enemy_group.add(enemy)
        enemy = Enemy(96, 96)
        self.enemy_group.add(enemy)

        self.movement_system = MovementSystem()
        self.ui_system = UISystem(self)

        self.selected_hero = None

        self.states = {"0": "selection",
                       "1": "movement_selection",
                       "2": "action",
                       "3": "attack_selection",
                       "4": "attack"}

        self.state = self.states["0"]

        self.take_input = True

        self.attacker = None
        self.defender = None
        self.damage = []

    def get_event(self, event):
        if self.take_input:
            if self.state == self.states["0"]:
                if event.type == pg.MOUSEBUTTONDOWN:
                    pressed = pg.mouse.get_pressed()
                    if pressed[0]:
                        pos = pg.mouse.get_pos()
                        self.select_hero(pos)

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        if not self.selected_hero:
                            for character in self.hero_group:
                                character.has_moved = False
                                character.image = character.orig_image
                                character.has_reached_goal = False

            elif self.state == self.states["1"]:
                if event.type == pg.MOUSEBUTTONDOWN:
                    pressed = pg.mouse.get_pressed()
                    if pressed[0]:
                        pos = pg.mouse.get_pos()

                        if not self.selected_hero:
                            raise AttributeError("shit bru dis shit broke, no hero selected")

                        if not self.selected_hero.has_reached_goal and not self.selected_hero.moving:
                            path_to_go = self.create_path_finding(pos)
                            self.movement_system.move_character(self.selected_hero, pos, self.valid_movement_tiles, path_to_go)
                            if self.selected_hero.moving:
                                self.path_finding = None
                                self.valid_movement_tiles = None

                    if pressed[2]:
                        if self.selected_hero:
                            if not self.selected_hero.moving:
                                self.selected_hero = None
                                self.valid_movement_tiles = None
                                self.path_finding = None

                                self.state = self.states["0"]

            elif self.state == self.states["2"]:
                if event.type == pg.MOUSEBUTTONDOWN:
                    pressed = pg.mouse.get_pressed()
                    if pressed[0]:
                        pos = pg.mouse.get_pos()
                        self.ui_system.get_event(event, pos)

                    if pressed[2]:
                        if self.selected_hero:
                            pos = [self.selected_hero.origin[0] * 32,self.selected_hero.origin[1] * 32]
                            self.selected_hero.set_position(pos)

                            self.selected_hero.has_reached_goal = False
                            self.ui_system.state = self.ui_system.states["0"]
                            self.ui_system.reset_buttons()
                            self.create_valid_move()

                            self.state = self.states["1"]

            elif self.state == self.states["3"]:
                enemy_list = self.check_for_enemies()

                if event.type == pg.MOUSEMOTION:
                    pos = pg.mouse.get_pos()
                    self.ui_system.state = self.ui_system.states["0"]
                    for enemy in enemy_list:
                        if enemy.rect.collidepoint(pos):

                            hit_crit_chance = self.calculate_hit_crit(self.selected_hero, enemy)
                            self.ui_system.set_ui_position(self.selected_hero.position)
                            self.ui_system.create_battle_stats_ui(self.selected_hero, enemy, hit_crit_chance)

                            self.ui_system.state = self.ui_system.states["2"]

                if event.type == pg.MOUSEBUTTONDOWN:
                    pressed = pg.mouse.get_pressed()
                    if pressed[0]:
                        pos = pg.mouse.get_pos()
                        for enemy in enemy_list:
                            if enemy.rect.collidepoint(pos):
                                self.do_attack(self.selected_hero, enemy)

                                self.selected_hero.has_moved = True

                                self.selected_hero.image = self.selected_hero.moved_image

                                self.selected_hero.has_reached_goal = False
                                self.selected_hero.origin = None
                                self.selected_hero = None

                                self.state = self.states["0"]
                                self.ui_system.state = self.ui_system.states["0"]
                                self.ui_system.reset_buttons()

                    if pressed[2]:
                        if self.selected_hero:
                            self.state = self.states["2"]

    def do_attack(self, attacker, defender):
        self.take_input = False

        hit_stats = self.calculate_hit_crit(attacker, defender)
        hit_results = self.roll_hero_hit(hit_stats)
        damage = self.calculate_damage(attacker, defender, hit_results)

        self.attacker = attacker
        self.defender = defender
        self.damage = damage

        self.do_attack_animation()

    def do_attack_animation(self):
        self.attacker.target = self.defender
        self.attacker.attacking = True

        self.defender.target = self.attacker
        self.defender.attacking = True






    def roll_hero_hit(self, hit_stats):
        attacker_hit_stats = hit_stats[0]
        attacker_hit = attacker_hit_stats[0]
        attacker_crit = attacker_hit_stats[1]

        defender_hit_stats = hit_stats[1]
        defender_hit = defender_hit_stats[0]
        defender_crit = defender_hit_stats[1]

        attacker_hit_roll = random.randint(0, 100)

        if attacker_hit_roll > attacker_hit:
            print "attacker has hit the enemy"
            attacker_result = 1

            attacker_crit_roll = random.randint(0, 100)
            if attacker_crit_roll > attacker_crit:
                print "attacker has crit the enemy"
                attacker_result = 2

        else:
            print "attacker missed the enemy"
            attacker_result = 0

        defender_hit_roll = random.randint(0, 100)

        if defender_hit_roll > defender_hit:
            print "defender has hit the enemy"
            defender_result = 1

            defender_crit_roll = random.randint(0, 100)
            if defender_crit_roll > defender_crit:
                print "defender has crit the enemy"
                defender_result = 2

        else:
            print "defender missed the enemy"
            defender_result = 0

        return [attacker_result, defender_result]

    def calculate_hit_crit(self, attacker, defender):
        attacker_hit_chance = max(0, attacker.hit_ability - defender.dodge_ability)
        attacker_crit_chance = max(0, attacker.hit_ability - defender.dodge_ability * 3)

        defender_hit_chance = max(0, defender.hit_ability - attacker.dodge_ability)
        defender_crit_chance = max(0, defender.hit_ability - attacker.dodge_ability * 3)

        return [[attacker_hit_chance, attacker_crit_chance], [defender_hit_chance, defender_crit_chance]]

    def calculate_damage(self, attacker, defender, hit_result):
        attacker_hit_result = hit_result[0]
        defender_hit_result = hit_result[1]

        attacker_damage_done = 0
        defender_damage_done = 0

        if attacker_hit_result == 0:
            "attacker missed the defender"
        elif attacker_hit_result == 1:
            "attacker hit the enemy"
            attacker_damage_done = attacker.attack
        else:
            "attacker crit the enemy"
            attacker_damage_done = attacker.attack * 2

        if defender_hit_result == 0:
            "defender missed the defender"
        elif defender_hit_result == 1:
            "defender hit the enemy"
            defender_damage_done = defender.attack
        else:
            "defender crit the enemy"
            defender_damage_done = defender.attack * 2

        return [attacker_damage_done, defender_damage_done]

    def check_tile(self, coord):
        pos = util.tile_coord_to_world_coord(coord)
        for enemy in self.enemy_group:
            if enemy.rect.collidepoint(pos):
                #print "detected enemy at", coord
                return False
        for hero in self.hero_group:
            if hero.rect.collidepoint(pos):
                #print "detected hero at", coord
                return False

        return True

    def select_hero(self, pos):
        for hero in self.hero_group:
            if hero.rect.collidepoint(pos):
                if not hero.has_moved:
                    self.selected_hero = hero
                    self.create_valid_move()

                    self.state = self.states["1"]
                else:
                    print "hero has moved"

    def create_valid_move(self):
        tile_list = []
        cost_dict = {}

        movement_range = self.selected_hero.movement_range

        for x in range(self.tile_number_x):
            for y in range(self.tile_number_y):
                tile_property = self.tile_renderer.tmx_data.get_tile_properties(x, y, 0)
                if "movement_cost" in tile_property:
                    tile_list.append([x, y])
                    cost_dict[tuple([x, y])] = tile_property["movement_cost"]

        pathing = Queue.PriorityQueue()
        start = self.selected_hero.get_tile_position()
        pathing.put(start, 0)
        came_from = {}
        cost_so_far = {}
        came_from[tuple(start)] = None
        cost_so_far[tuple(start)] = 0

        while not pathing.empty():
            current = pathing.get()
            for next in self.get_neighbors(current, tile_list):
                if self.check_tile(next):
                    new_cost = cost_so_far[tuple(current)] + int(cost_dict[tuple(next)])
                    if new_cost > movement_range:
                        continue
                    if tuple(next) not in cost_so_far or new_cost < cost_so_far[tuple(next)]:
                        cost_so_far[tuple(next)] = new_cost
                        priority = new_cost
                        pathing.put(next, priority)
                        came_from[tuple(next)] = current

        valid_tile_list = []
        for x in came_from.iterkeys():
            valid_tile_list.append(x)
        self.valid_movement_tiles = valid_tile_list

    def create_path_finding(self, end):
        tile_list = []

        end = util.world_coord_to_tile_coord(end)

        for x in range(self.tile_number_x):
            for y in range(self.tile_number_y):
                tile_property = self.tile_renderer.tmx_data.get_tile_properties(x, y, 0)
                if "movement_cost" in tile_property:
                    tile_list.append([x, y])

        pathing = Queue.PriorityQueue()
        start = self.selected_hero.get_tile_position()

        pathing.put(start, 0)
        came_from = {}
        cost_so_far = {}
        came_from[tuple(start)] = None
        cost_so_far[tuple(start)] = 0

        while not pathing.empty():
            current = pathing.get()

            if current == end:
                break

            for next in self.get_neighbors(current, tile_list):
                new_cost = cost_so_far[tuple(current)] + 1
                if tuple(next) not in cost_so_far or new_cost < cost_so_far[tuple(next)]:
                    cost_so_far[tuple(next)] = new_cost
                    priority = new_cost
                    pathing.put(next, priority)
                    came_from[tuple(next)] = current

        current = end
        final_path = [current]
        while current != start:
            current = came_from[tuple(current)]
            final_path.append(current)
        final_path.reverse()
        return final_path

    def get_neighbors(self, node, tile_list):
        dirs = [[1, 0], [0, 1], [-1, 0], [0, -1]]
        result = []
        for direct in dirs:
            neighbor = [node[0] + direct[0], node[1] + direct[1]]
            if neighbor in tile_list:
                result.append(neighbor)
        return result

    def update(self, dt):
        #print self.state

        for hero in self.hero_group:
            hero.update(dt)


        for enemy in self.enemy_group:
            enemy.update(dt)

        if self.state == self.states["1"]:
            if self.selected_hero.has_reached_goal:
                self.state = self.states["2"]

        if self.state == self.states["2"]:
            enemy_list = self.check_for_enemies()

            if enemy_list:
                self.ui_system.add_button("attack")

            self.ui_system.state = self.ui_system.states["1"]
            self.ui_system.set_ui_position(self.selected_hero.position)
            self.valid_movement_tiles = None

        if self.state == self.states["3"]:
            if self.ui_system.state == self.ui_system.states["1"]:
                self.ui_system.state = self.ui_system.states["0"]

        if not self.take_input:
            if self.attacker.attacking:
                self.attacker.can_animate = True
                return

            self.attacker.can_animate = False
            if self.defender.attacking:
                    self.defender.can_animate = True
                    return
            self.defender.can_animate = False

            # All animations are done, enable user input
            self.take_input = True



    def check_for_enemies(self):
        tile_list = []

        for x in range(self.tile_number_x):
            for y in range(self.tile_number_y):
                tile_property = self.tile_renderer.tmx_data.get_tile_properties(x, y, 0)
                if "movement_cost" in tile_property:
                    tile_list.append([x, y])

        tile = self.selected_hero.get_tile_position()
        neighbors = self.get_neighbors(tile, tile_list)

        enemy_list = []

        for enemy in self.enemy_group:
            if enemy.get_tile_position() in neighbors:
                enemy_list.append(enemy)

        return enemy_list

    def draw(self, screen):
        screen.blit(self.map_surface, (0, 0))
        self.hero_group.draw(screen)
        self.enemy_group.draw(screen)
        self.draw_debug_pathing(screen)
        self.ui_system.draw(screen)
        #self.draw_debug(screen)

    def draw_debug(self, screen):
        for x in range(0, self.map_rect.width // self.tile_width):
            for y in range(0, self.map_rect.height // self.tile_width):
                pg.draw.rect(screen, pg.Color("black"), [x * self.tile_width, y * self.tile_width, 32, 32], 1)

    def draw_debug_pathing(self, screen):
        if self.valid_movement_tiles:
            for x in self.valid_movement_tiles:
                if x == None:
                    continue
                pg.draw.rect(screen, pg.Color("black"), [x[0] * 32, x[1] * 32, 32, 32], 1)



