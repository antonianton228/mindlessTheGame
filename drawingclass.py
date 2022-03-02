import pygame
from settings import *
from  ray_casting import ray_casting


class Drawing():
    def __init__(self, sc):
        self.sc = sc
        self.font = pygame.font.SysFont('Arial', 36, bold=True)
        self.textures = {1: pygame.image.load('data/textures/brick1.png').convert(),
                         2: pygame.image.load('data/textures/brick2.png').convert(),
                         5: pygame.image.load('data/textures/sky.png').convert()}

    def backgraund(self, angle):
        sky_offset = -5 * math.degrees(angle) % width
        self.sc.blit(self.textures[5], (sky_offset, 0))
        self.sc.blit(self.textures[5], (sky_offset - width, 0))
        self.sc.blit(self.textures[5], (sky_offset + width, 0))
        pygame.draw.rect(self.sc, yellow, (0, half_height, width, half_width))

    def world(self, player_pos, player_angle):
        ray_casting(self.sc, player_pos, player_angle, self.textures)

    def fps(self, clock):
        display_fps = str(int(clock.get_fps()))
        render = self.font.render(display_fps, 0, red)
        self.sc.blit(render,(width - 65, 5))
