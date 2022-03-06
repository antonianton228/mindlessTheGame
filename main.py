import pygame
from playerclass import Player
from settings import *
from maps import world_map
from drawingclass import Drawing
from sprites import *
from ray_casting import ray_casting_walls
from floor_casting import floor_casting


pygame.init()
sc = pygame.display.set_mode((width, height))
pygame.mouse.set_visible(False)
clock = pygame.time.Clock()
drawing = Drawing(sc)
sprites = Sprites()
player = Player(sprites)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    player.movement()


    drawing.backgraund(player.angle)
    walls = ray_casting_walls(player, drawing.textures)
    floor_casting(sc)
    drawing.world(walls + [obj.object_locate(player) for obj in sprites.list_of_objects])
    drawing.fps(clock)


    pygame.display.flip()
    clock.tick(65)