import pygame

import constants


class SpriteSheet(object):
    def __init__(self, file_name):
        self.sprite_sheet = pygame.image.load(file_name).convert()

    def get_image(self, x, y, width, height, *scale):
        image = pygame.Surface([width, height]).convert()
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey(constants.BLACK)
        if scale:
            scale_width, scale_height = scale
            image = pygame.transform.scale(image, (scale_width, scale_height))

        return image


