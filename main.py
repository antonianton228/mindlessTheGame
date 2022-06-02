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
import pygame as pg




pygame.init()
sc = pygame.display.set_mode((width, height))

clock = pygame.time.Clock()
sprites = Sprites()
player = Player(sprites)
drawing = Drawing(sc, player, clock)
interaction = Interaction(player, sprites, drawing)


pygame.mouse.set_visible(True)
drawing.menu()
pygame.mouse.set_visible(False)
interaction.play_music()
while True:
    world_map = maps.map_call()[1]
    flagloop = True
    floor_and_sky = [0, 0, 0]
    s = 0
    while flagloop:
        last_x, last_y, last_angle, move = player.x, player.y, player.angle, 1000000
        player.movement()
        move, s = drawing.floor_settings(player.x, player.y, player.angle, last_x, last_y, last_angle, s, move)

        walls, wall_hit = ray_casting_walls(player, drawing.textures)

        sprites.list_of_objects = sprites.dict_of_objects[storyteller.get_level()]

        # drawing.floor_drow(sc)
        floor_and_sky = drawing.floor(player.x, player.y, player.angle, move, floor_and_sky[1], s)
        drawing.world(walls + [obj.object_locate(player) for obj in sprites.list_of_objects] + [floor_and_sky])
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