import pygame
from settings import *
from ray_casting import ray_casting
from collections import deque





class Drawing():
    def __init__(self, sc, player):
        self.sc = sc
        self.player = player
        self.font = pygame.font.SysFont('Arial', 36, bold=True)
        self.textures = {1: pygame.image.load('data/textures/forest1.png').convert(),
                         2: pygame.image.load('data/textures/forest1.png').convert(),
                         3: pygame.image.load('data/textures/forest1.png').convert(),
                         4: pygame.image.load('data/textures/forest1.png').convert(),
                         5: pygame.image.load('data/textures/sky.png').convert(),
                         6: pygame.image.load('data/textures/grass.jpg').convert()}

        # weapens
        self.weapon_base_sprite = pygame.image.load('data/sprites/weapons/shotgun/default.png')
        self.weapon_shot_animation = deque([pygame.image.load(f'data/sprites/weapons/shotgun/{i}.png').convert_alpha()
                                            for i in range(20)])
        self.weapon_rect = self.weapon_base_sprite.get_rect()
        self.weapon_pos = (half_width - self.weapon_rect.width // 2, height
                           - self.weapon_rect.height)
        self.shot_lenght = len(self.weapon_shot_animation)
        self.shot_lenght_count = 0
        self.shot_animation_speed = 1
        self.shot_animation_count = 0
        self.shot_animation_trigger = True

        self.sfx = deque([pygame.image.load(f'data/sprites/sfx/shotgun/{i}.png').convert_alpha() for i in range(9)])
        self.sfx_lenght_count = 0
        self.sfx_lenght = len(self.sfx)




    def world(self, world_objects):
         for obj in sorted(world_objects, key=lambda x: x[0], reverse=True):
             if obj[0]:
                 _, object, object_pos = obj
                 self.sc.blit(object, object_pos)

    def fps(self, clock):
        display_fps = str(int(clock.get_fps()))
        render = self.font.render(display_fps, 0, red)
        self.sc.blit(render,(width - 65, 5))


    def player_weapon(self, shots):
        if self.player.shot:
            self.shot_proj = min(shots)[1] // 2
            self.bullet_sfx()
            shot_sprite = self.weapon_shot_animation[0]
            self.sc.blit(shot_sprite, self.weapon_pos)
            self.shot_animation_count += 1
            if self.shot_animation_count == self.shot_animation_speed:
                self.weapon_shot_animation.rotate(-1)
                self.shot_animation_count = 0
                self.shot_lenght_count += 1
                self.shot_animation_trigger = False
            if self.shot_lenght_count == self.shot_lenght:
                self.player.shot = False
                self.shot_lenght_count = 0
                self.sfx_lenght_count = 0
                self.shot_animation_trigger = True
        else:
            self.sc.blit(self.weapon_base_sprite, self.weapon_pos)


    def bullet_sfx(self):
        if self.sfx_lenght_count < self.sfx_lenght:
            sfx = pygame.transform.scale(self.sfx[0],
                                         (self.shot_proj, self.shot_proj))
            sfx_rect = sfx.get_rect()
            self.sc.blit(sfx, (half_width - sfx_rect.w // 2,
                               half_height - sfx_rect.h // 2))
            self.sfx_lenght_count += 1
            self.sfx.rotate(-1)


    def floor_drow(self, sc):
        pygame.draw.rect(sc, skyblue, (0, 0, 1200, 400))
        pygame.draw.rect(sc, grassgreen, (0, 400, 1200, 800))
