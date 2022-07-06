import pygame
import settings
from playerclass import Player
from settings import *
import maps
from drawingclass import Drawing
from sprites import *
import numpy as np
from numba import njit
from ray_casting import ray_casting_walls, floor, floor_settings
from npc_ai import Interaction
import storyteller
import pygame as pg
from lor import Story




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
story = Story(sprites, player, drawing)
while True:
    world_map = maps.map_call()[1]
    flagloop = True
    floor_and_sky = [0, 0, 0]
    s = 0
    while flagloop:
        if player.is_alive:

            last_x, last_y, last_angle, move = player.x, player.y, player.angle, 1000000
            player.movement()
            move, s = floor_settings(player.x, player.y, player.angle, last_x, last_y, last_angle, s, move)

            walls, wall_hit = ray_casting_walls(player, drawing.textures)

            sprites.list_of_objects = sprites.dict_of_objects[storyteller.get_level()]

            # drawing.floor_drow(sc)
            #floor_and_sky = floor(player.x, player.y, player.angle, move, floor_and_sky[1], s)
            drawing.floor_drow(sc)
            drawing.world(walls + [obj.object_locate(player) for obj in sprites.list_of_objects] + [floor_and_sky])
            drawing.hp_bar()
            drawing.fps(clock)

            drawing.quest_bar()
            drawing.player_weapon([wall_hit, sprites.sprite_hit])


            interaction.intersection_object()
            interaction.npc_action()
            interaction.acting_object()
            interaction.clear_objects()
            if settings.dialog_draw:
                drawing.dialoge_draw('Привет', 'До свидания', 'До свидания')
                settings.dialog_draw = False
            story.make_kvest()
            settings.num_kvest = story.new_kvest(settings.num_kvest)
            if settings.num_last_kvest != settings.num_kvest:
                settings.num_last_kvest = settings.num_kvest
                story.start_kvest(settings.num_kvest)
        else:
            drawing.dialoge_draw("Вы погибли! Начать с последнего сохранения?", 'ДА', 'НЕТ')



        if not flagloop:
            break
        pygame.display.flip()
        clock.tick(120)