import pygame as pg


class Button(pg.sprite.Sprite):
    def __init__(self, image, x, y, parent):
        super(Button, self).__init__()

        self.image = pg.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.parent = parent

    def get_clicked(self):
        pass

    def set_position(self, pos):
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def draw(self, screen):
        screen.blit(self.image, self.rect)


