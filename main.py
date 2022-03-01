import pygame
from playerclass import Player
from settings import *
import math

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

    pygame.draw.circle(sc, green, player.pos, 12)
    pygame.draw.line(sc, green, player.pos, (player.x + width * math.cos(player.angle),
                                             player.y + width * math.sin(player.angle)))


    pygame.display.flip()
    clock.tick(60)