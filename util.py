def world_coord_to_tile_coord(coord):
    target_x = coord[0] // 32
    target_y = coord[1] // 32
    return [int(target_x), int(target_y)]


def tile_coord_to_world_coord(coord):
    target_x = coord[0] * 32
    target_y = coord[1] * 32
    return [int(target_x), int(target_y)]