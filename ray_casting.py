import pygame
from settings import *
from maps import world_map

# def ray_casting(sc, player_pos, player_angle):
#     cur_angle = player_angle - half_fov
#     x0, y0 = player_pos
#     for ray in range(num_rays):
#         sin_a = math.sin(cur_angle)
#         cos_a = math.cos(cur_angle)
#         for depth in range(max_depth):
#             x = x0 + depth * cos_a
#             y = y0 + depth * sin_a
#             # pygame.draw.line(sc, (10, 10, 10), player_pos, (x, y), 2)
#             if (x // tile * tile, y // tile * tile) in world_map:
#                 depth *= math.cos(player_angle - cur_angle)
#                 proj_height = proj_coof / depth
#                 c = 255 / (1 + depth * depth * 0.00002)
#                 color = (c, c // 4, c // 2)
#                 pygame.draw.rect(sc, color, (ray * scale, half_height - proj_height // 2, scale, proj_height))
#                 break
#         cur_angle += delta_angle
def mapping(a, b):
    return (a // tile) * tile, (b // tile) * tile


def ray_casting(sc, player_pos, player_angle):
    ox, oy = player_pos
    xm, ym = mapping(ox, oy)
    cur_angle = player_angle - half_fov
    for ray in range(num_rays):
        sin_a = math.sin(cur_angle)
        cos_a = math.cos(cur_angle)
        # vert
        if cos_a >= 0:
            x = xm + tile
            dx = 1
        else:
            x = xm
            dx = -1
        for i in range(0, width, tile):
            depth_v = (x - ox) / cos_a
            y = oy + depth_v * sin_a
            if mapping(x + dx, y) in world_map:
                break
            x += dx * tile
        # hor
        if sin_a >= 0:
            y = ym + tile
            dy = 1
        else:
            y = ym
            dy = -1
        for i in range(0, height, tile):
            depth_h = (y - oy) / sin_a
            x = ox + depth_h * cos_a
            if mapping(x, y + dy) in world_map:
                break
            y += dy * tile
        # proj
        depth = min(depth_h, depth_v)
        depth *= math.cos(player_angle - cur_angle)
        proj_height = proj_coof / depth
        c = 255 / (1 + depth * depth * 0.00002)
        color = (c, c // 4, c // 2)
        pygame.draw.rect(sc, color, (ray * scale, half_height - proj_height // 2, scale, proj_height))
        cur_angle += delta_angle
