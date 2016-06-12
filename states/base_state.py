import pygame as pg


class GameState(object):
    def __init__(self):
        self.done = False
        self.quit = False
        self.screen = pg.display.get_surface()
        self.screen_rect = pg.display.get_surface().get_rect()
        self.next_state = None
        self.persist = {}
        self.font = pg.font.Font(None, 24)

    def startup(self, persistent):
        self.persist = persistent

    def get_event(self, event):
        pass

    def update(self, dt):
        pass

    def draw(self, screen):
        pass
