import pygame
from playerclass import Player
from settings import *
from maps import world_map
from drawingclass import Drawing
from sprites import *
from ray_casting import ray_casting


pygame.init()
sc = pygame.display.set_mode((width, height))
pygame.mouse.set_visible(False)
clock = pygame.time.Clock()
drawing = Drawing(sc)
sprites = Sprites()
player = Player(sprites)
from drawingclass import Drawing

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    player.movement()
    sc.fill(black)


    drawing.backgraund(player.angle)
    walls = ray_casting(player, drawing.textures)
    drawing.world(walls + [obj.object_locate(player) for obj in sprites.list_of_objects])
    drawing.fps(clock)


    pygame.display.flip()
    clock.tick(65)