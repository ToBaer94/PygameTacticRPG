import pygame as pg
import util

Vector = pg.math.Vector2


class MovementSystem(object):

    def calculate_valid_move(self, character):
        pass

    def move_character(self, character, target, valid_tiles, path):
        target_tile = util.world_coord_to_tile_coord(target)
        if tuple([target_tile[0], target_tile[1]]) in valid_tiles:
            character.path = path[1:]
            character.origin = path[0]
            character.set_goal()

    def move_to_tile(self, character, goal):
        pass
