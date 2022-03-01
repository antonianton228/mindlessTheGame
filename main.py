import pygame
from playerclass import Player
from settings import *
import math
from maps import world_map
from ray_casting import ray_casting

pygame.init()
sc = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
player = Player()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    player.movement()
    sc.fill(black)
    pygame.draw.rect(sc, blue, (0, 0, width, half_width))
    pygame.draw.rect(sc, yellow, (0, half_height, width, half_width))
    ray_casting(sc, player.pos, player.angle)

    # pygame.draw.circle(sc, green, player.pos, 12)
    # pygame.draw.line(sc, green, player.pos, (player.x + width * math.cos(player.angle),
    #                                         player.y + width * math.sin(player.angle)))
    #for x, y in world_map:
        # pygame.draw.rect(sc, (255, 255, 255), (x, y, tile, tile), 2)

    pygame.display.flip()
    clock.tick(60)