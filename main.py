import pygame as pg
import sys
from states.gameplay_state import GamePlay


class Game(object):
    def __init__(self, screen, states, start_state):
        self.done = False
        self.screen = screen
        self.clock = pg.time.Clock()
        self.fps = 60.0
        self.target_fps = 60.0
        self.ms_per_sec = 1000.0
        self.desired_frame_time = self.ms_per_sec / self.target_fps
        self.max_step = 1.0

        self.states = states
        self.state_name = start_state
        self.state = self.states[self.state_name]
        self.state.startup({})

    def event_loop(self):
        for event in pg.event.get():

            if event.type == pg.QUIT:
                self.done = True

            if event.type == pg.VIDEORESIZE:
                self.set_screen(event.w, event.h)

            self.state.get_event(event)

    def set_screen(self, width, height):
        self.screen = pg.display.set_mode((width, height), pg.RESIZABLE)

    def flip_state(self):
        current_state = self.state_name
        next_state = self.state.next_state
        self.state.done = False
        self.state_name = next_state
        persistent = self.state.persist
        print persistent
        self.state = self.states[self.state_name]
        self.state.startup(persistent)

    def update(self, dt):
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()

        self.state.update(dt)

    def draw(self):
        self.state.draw(self.screen)

    def run(self):
        while not self.done:
            self.event_loop()
            frame_time = self.clock.tick(self.fps)
            total_delta_time = frame_time / self.desired_frame_time
            while total_delta_time > 0.0:
                delta_time = min(total_delta_time, self.max_step)
                self.update(delta_time)
                total_delta_time -= delta_time

            #print self.clock.get_fps()

            self.draw()
            pg.display.flip()


if __name__ == "__main__":
    pg.mixer.init()
    pg.init()

    pg.display.set_caption("TacticRPG")
    screen = pg.display.set_mode((800, 512)) # , pg.RESIZABLE
    states = {"GAME": GamePlay()}

    game = Game(screen, states, "GAME")
    game.run()
    pg.quit()
    sys.exit()

