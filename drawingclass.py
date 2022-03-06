import pygame
from settings import *
from  ray_casting import ray_casting, floor_cast
#from floor_casting import floor_cast





class Drawing():
    def __init__(self, sc):
        self.sc = sc
        self.font = pygame.font.SysFont('Arial', 36, bold=True)
        self.textures = {1: pygame.image.load('data/textures/forest1.png').convert(),
                         2: pygame.image.load('data/textures/forest1.png').convert(),
                         3: pygame.image.load('data/textures/forest1.png').convert(),
                         4: pygame.image.load('data/textures/forest1.png').convert(),
                         5: pygame.image.load('data/textures/sky.png').convert(),
                         6: pygame.image.load('data/textures/grass.jpg').convert()}



    def backgraund(self, angle):
        # sky_offset = -5 * math.degrees(angle) % width
        # self.sc.blit(self.textures[5], (sky_offset, 0))
        # self.sc.blit(self.textures[5], (sky_offset - width, 0))
        # self.sc.blit(self.textures[5], (sky_offset + width, 0))
        # #floor_cast(sc)
        #
        #
        #
        # #self.sc.blit(self.textures[6], (sky_offset1 + width, 400))
        # pygame.draw.rect(self.sc, yellow, (0, half_height, width, half_width))
        pass


    def world(self, world_objects):
         for obj in sorted(world_objects, key=lambda x: x[0], reverse=True):
             if obj[0]:
                 _, object, object_pos = obj
                 self.sc.blit(object, object_pos)

    def fps(self, clock):
        display_fps = str(int(clock.get_fps()))
        render = self.font.render(display_fps, 0, red)
        self.sc.blit(render,(width - 65, 5))
