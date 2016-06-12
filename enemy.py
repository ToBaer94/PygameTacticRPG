import pygame as pg
from os import pardir, path

Vector = pg.math.Vector2

img_dir = path.join(path.dirname(__file__), "assets", "creeps")


class Enemy(pg.sprite.Sprite):
    def __init__(self, x, y):
        super(Enemy, self).__init__()

        self.position = Vector(x, y)
        self.image = pg.image.load(path.join(img_dir, "creep.png")).convert_alpha()
        self.rect = self.image.get_rect(topleft=self.position)

        self.hp = 10
        self.attack = 2

        self.hit_ability = 40
        self.dodge_ability = 10

        self.attacking = False
        self.turned_around = False
        self.target = None

        self.vel = Vector(0, 0)

        self.original_animation_position = Vector(0, 0)
        self.can_animate = False

    def update(self, dt):
        self.position.x += self.vel.x
        self.position.y += self.vel.y

        self.rect.x = self.position.x
        self.rect.y = self.position.y

        if self.attacking:
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

    def get_tile_position(self):
        x_pos = self.position.x // 32
        y_pos = self.position.y // 32
        return [int(x_pos), int(y_pos)]

    def take_damage(self, damage):
        self.hp -= damage

        if self.hp <= 0:
            self.kill()




