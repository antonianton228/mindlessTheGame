import pygame

import settings
from playerclass import Player
from settings import *
import maps
from drawingclass import Drawing
from sprites import *
import numpy as np
from numba import njit
from ray_casting import ray_casting_walls
from npc_ai import Interaction
import storyteller




pygame.init()
sc = pygame.display.set_mode((width, height))

clock = pygame.time.Clock()
sprites = Sprites()
player = Player(sprites)
drawing = Drawing(sc , player, clock)
interaction = Interaction(player, sprites, drawing)



hres = 400  # horizontal resolution
halfvres = 200  # vertical resolution/2
mod = hres / 60  # scaling factor (60° fov)
posx, posy, rot = 0, 0, 0
frame = np.random.uniform(0, 1, (hres, halfvres * 2, 3))
sky = pygame.image.load('data/textures/skybox2.jpg')
sky = pygame.surfarray.array3d(pygame.transform.scale(sky, (100, halfvres * 2))) / 255
#print(floor)


pygame.mouse.set_visible(True)
drawing.menu()
pygame.mouse.set_visible(False)
interaction.play_music()
while True:
    world_map = maps.map_call()[1]
    flagloop = True
    while flagloop:
        drawing.floor_drow(sc)
        player.movement()
        posx, posy, rot = player.movement_floor(posx, posy, rot, pygame.key.get_pressed(), clock.tick()) # хз почему, но без этого фпс меньше

        walls, wall_hit = ray_casting_walls(player, drawing.textures)

        sprites.list_of_objects = sprites.dict_of_objects[storyteller.get_level()]

        drawing.world(walls + [obj.object_locate(player) for obj in sprites.list_of_objects])
        drawing.fps(clock)
        drawing.player_weapon([wall_hit, sprites.sprite_hit])

        interaction.intersection_object()
        interaction.npc_action()
        interaction.acting_object()
        interaction.clear_objects()
        if settings.dialog_draw:
            drawing.dialoge_draw()
            settings.dialog_draw = False

        if not flagloop:
            break
        pygame.display.flip()
        clock.tick(120)





