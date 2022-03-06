import pygame
from settings import *
from main import player

def floor_casting(sc):
    hres = 100
    halfvres = 200

    mod = hres / 60
    posx, posy, rot = *player.pos, player.angle
    frame = np.random.uniform(0, 1, (hres, halfvres * 2, 3))
    sky = pg.image.load('')

