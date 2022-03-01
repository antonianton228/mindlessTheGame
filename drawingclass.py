import pygame
from settings import *
from  ray_casting import ray_casting


class Drawing():
    def __init__(self, sc):
        self.sc = sc
        self.font = pygame.font.SysFont('Arial', 36, bold=True)

    def backgraund(self):
        pygame.draw.rect(self.sc, skyblue, (0, 0, width, half_width))
        pygame.draw.rect(self.sc, yellow, (0, half_height, width, half_width))

    def world(self, player_pos, player_angle):
        ray_casting(self.sc, player_pos, player_angle)

    def fps(self, clock):
        display_fps = str(int(clock.get_fps()))
        render = self.font.render(display_fps, 0, red)
        self.sc.blit(render,(width - 65, 5))
