from base_state import GameState
import pygame as pg
from level import Level


class GamePlay(GameState):
    def __init__(self):
        super(GamePlay, self).__init__()

        self.level = Level()

    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True

        self.level.get_event(event)

    def update(self, dt):
        self.level.update(dt)

    def draw(self, screen):
        self.level.draw(screen)