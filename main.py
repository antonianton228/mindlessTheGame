import pygame
from playerclass import Player
from settings import *
import math
from maps import world_map
from ray_casting import ray_casting
from drawingclass import Drawing

pygame.init()
sc = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
player = Player()
drawing = Drawing(sc)
from drawingclass import Drawing

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    player.movement()
    sc.fill(black)
    drawing.backgraund()
    drawing.world(player.pos, player.angle)
    drawing.fps(clock)

    # pygame.draw.circle(sc, green, player.pos, 12)
    # pygame.draw.line(sc, green, player.pos, (player.x + width * math.cos(player.angle),
    #                                         player.y + width * math.sin(player.angle)))
    #for x, y in world_map:
        # pygame.draw.rect(sc, (255, 255, 255), (x, y, tile, tile), 2)

    pygame.display.flip()
    clock.tick(60)