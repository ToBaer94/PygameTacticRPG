import pygame as pg
from os import path, pardir
import copy
Vector = pg.math.Vector2


img_dir = path.join(path.dirname(__file__), "assets", "heroes")


class Hero(pg.sprite.Sprite):

    def __init__(self):
        super(Hero, self).__init__()

        self.position = Vector(64, 64)
        self.image = self.orig_image = pg.image.load(path.join(img_dir, "hero.png")).convert_alpha()
        self.moved_image = pg.image.load(path.join(img_dir, "hero_moved.png")).convert_alpha()
        self.rect = self.image.get_rect(topleft=self.position)

        self.movement_range = 5

        self.vel = Vector(0, 0)
        self.goal = None
        self.path = None
        self.origin = None

        self.hp = 10
        self.attack = 2

        self.hit_ability = 70
        self.dodge_ability = 20

        self.has_moved = False
        self.has_reached_goal = False

        self.moving = False

        self.turned_around = False
        self.attacking = False

        self.target = None

        self.original_animation_position = Vector(0, 0)

        self.can_animate = False

    def update(self, dt):

        self.position.x += self.vel.x
        self.position.y += self.vel.y

        self.rect.x = self.position.x
        self.rect.y = self.position.y

        if self.goal:
            self.move_to_tile()

        elif self.attacking:
            if self.original_animation_position:
                self.do_attack(self.target, self.direction_x, self.direction_y)
            else:
                self.original_animation_position = Vector(self.position.x, self.position.y)
                self.direction_x = self.target.position.x - self.position.x
                self.direction_y = self.target.position.y - self.position.y

                self.turned_around = False
                self.do_attack(self.target, self.direction_x, self.direction_y)

    def do_attack(self, target, direction_x, direction_y):
        if self.can_animate:
            if not target:
                raise NotImplementedError("U fucked sth up yo, no target")

            direction_vector = Vector(direction_x, direction_y)

            current_dir_x = self.target.position.x - self.position.x
            current_dir_y = self.target.position.y - self.position.y

            current_dir_vector = Vector(current_dir_x, current_dir_y)

            norm_dir_vector = direction_vector.normalize()


            if current_dir_vector.x < direction_vector.x / 2 and self.vel.x > 0:
                self.turned_around = True

            if abs(current_dir_vector.x) < abs(direction_vector.x / 2) and self.vel.x < 0:
                self.turned_around = True

            if self.turned_around:
                self.vel.x = norm_dir_vector.x * -0.5
                self.vel.y = norm_dir_vector.y * -0.5
            else:
                self.vel.x = norm_dir_vector.x * 0.5
                self.vel.y = norm_dir_vector.y * 0.5

            if self.position.x < self.original_animation_position.x and self.turned_around and self.vel.x < 0:
                print "this works"
                self.position = self.original_animation_position
                self.turned_around = False
                self.target = None
                self.attacking = False
                self.vel.x = 0
                self.original_animation_position = Vector(0, 0)

                return

            if self.position.x > self.original_animation_position.x and self.turned_around and self.vel.x > 0:
                print "that works"
                self.position = self.original_animation_position
                self.target = None
                self.turned_around = False
                self.attacking = False
                self.vel.x = 0
                self.original_animation_position = Vector(0, 0)

                return

    def move_to_tile(self):
        self.moving = True

        if (self.position.x - self.goal[0]*32) < self.vel.x and self.vel.x < 0:
            self.position.x = self.goal[0]*32
            self.vel.x = 0
            self.set_goal()

        elif (self.position.x - self.goal[0]*32) > self.vel.x and self.vel.x > 0:
            self.position.x = self.goal[0]*32
            self.vel.x = 0
            self.set_goal()

        elif (self.position.y - self.goal[1]*32) < self.vel.x and self.vel.y < 0:
            self.position.y = self.goal[1]*32
            self.vel.y = 0
            self.set_goal()

        elif (self.position.y - self.goal[1]*32) > self.vel.y and self.vel.y > 0:
            self.position.y = self.goal[1]*32
            self.vel.y = 0
            self.set_goal()

    def set_goal(self):
        if self.path != []:
            self.goal = self.path.pop(0)
            self.set_target_tile()

        else:
            self.moving = False
            self.has_reached_goal = True
            self.goal = None

    def get_tile_position(self):
        x_pos = self.position.x // 32
        y_pos = self.position.y // 32
        return [int(x_pos), int(y_pos)]

    def set_target_tile(self):
        self.vel.x = self.goal[0] * 32 - self.position.x
        self.vel.y = self.goal[1] * 32 - self.position.y
        length = self.vel.length()
        if length == 0:
            return
        self.vel = self.vel.normalize()
        self.vel.x *= 3
        self.vel.y *= 3

    def set_position(self, pos):
        self.position = Vector(self.origin[0] * 32,
                               self.origin[1] * 32)

        self.rect.x = self.position.x
        self.rect.y = self.position.y

    def take_damage(self, damage):
        self.hp -= damage

