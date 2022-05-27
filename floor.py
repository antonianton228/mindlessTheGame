import pygame as pg
import numpy as np
from numba import njit


def floor(posx, posy, rot, move, surf):
    if move:
        hres = 120  # horizontal resolution
        halfvres = 50  # vertical resolution/2

        mod = hres / 60  # scaling factor (60° fov)
        frame = np.random.uniform(0, 1, (hres, halfvres * 2, 3))
        sky = pg.image.load('skybox.jpg')
        sky = pg.surfarray.array3d(pg.transform.scale(sky, (360, halfvres * 2))) / 255
        floor = pg.surfarray.array3d(pg.image.load('floor.jpg')) / 255

        frame = new_frame(posx, posy, rot, frame, sky, floor, hres, halfvres, mod)

        surf = pg.surfarray.make_surface(frame * 255)
        surf = pg.transform.scale(surf, (1200, 800))

    return 100000, surf, (0, 0)


@njit()
def new_frame(posx, posy, rot, frame, sky, floor, hres, halfvres, mod):
    posy, posx = posy * 0.01, posx * 0.01
    for i in range(hres):
        rot_i = rot + np.deg2rad(i / mod - 30)
        sin, cos, cos2 = np.sin(rot_i), np.cos(rot_i), np.cos(np.deg2rad(i / mod - 30))
        frame[i][:] = sky[int(np.rad2deg(rot_i) % 359)][:]
        for j in range(halfvres):
            n = (halfvres / (halfvres - j)) / cos2
            x, y = posx + cos * n, posy + sin * n
            xx, yy = int(x * 2 % 1 * 99), int(y * 2 % 1 * 99)
            frame[i][halfvres * 2 - j - 1] = floor[xx][yy]

    return frame
