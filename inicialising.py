import pygame


def init():
    pygame.init()
    screen = pygame.display.set_mode((1000, 1000))
    clock = pygame.time.Clock()
    clock.tick(60)
    pygame.display.set_caption("My Game")
    screen.fill((0, 0, 255))
    pygame.display.flip()




