import pygame
from playerclass import Player
from settings import *
from maps import world_map
from drawingclass import Drawing
from sprites import *
import numpy as np
from numba import njit
from ray_casting import ray_casting_walls

pygame.init()
sc = pygame.display.set_mode((width, height))
pygame.mouse.set_visible(False)
clock = pygame.time.Clock()
sprites = Sprites()
player = Player(sprites)
drawing = Drawing(sc , player)



hres = 400  # horizontal resolution
halfvres = 200  # vertical resolution/2
mod = hres / 60  # scaling factor (60° fov)
posx, posy, rot = 0, 0, 0
frame = np.random.uniform(0, 1, (hres, halfvres * 2, 3))
sky = pygame.image.load('data/textures/skybox2.jpg')
sky = pygame.surfarray.array3d(pygame.transform.scale(sky, (100, halfvres * 2))) / 255
floor = pygame.surfarray.array3d(pygame.image.load('data/textures/grass1.jpg')) / 255

@njit(fastmath=True)
def new_frame(posx, posy, rot, frame, sky, floor, hres, halfvres, mod):
    for i in range(hres):
        rot_i = rot + np.deg2rad(i / mod - 30)
        sin, cos, cos2 = np.sin(rot_i), np.cos(rot_i), np.cos(np.deg2rad(i / mod - 30))
        frame[i][:] = sky[int(np.rad2deg(rot_i) % 44)][:]
        for j in range(halfvres):
            n = (halfvres / (halfvres - j)) / cos2
            x, y = posx + cos * n, posy + sin * n
            xx, yy = int(x * 2 % 1 * 99), int(y * 2 % 1 * 99)
            # shade = 0.2 + 0.8 * (1 - j / halfvres)
            # if shade > 1:
            #     shade = 1
            frame[i][halfvres * 2 - j - 1] = floor[xx][yy]# * shade

    return frame


while True:


    frame = new_frame(posx, posy, rot, frame, sky, floor, hres, halfvres, mod)
    surf = pygame.surfarray.make_surface(frame * 255)
    surf = pygame.transform.scale(surf, (1200, 800))
    sc.blit(surf, (0, 0))
    player.movement()
    posx, posy, rot = player.movement_floor(posx, posy, rot, pygame.key.get_pressed(), clock.tick())
    walls, wall_hit = ray_casting_walls(player, drawing.textures)
    drawing.world(walls + [obj.object_locate(player) for obj in sprites.list_of_objects])
    drawing.fps(clock)
    drawing.player_weapon([wall_hit, sprites.sprite_hit])
    pygame.display.flip()
    clock.tick(65)





