import random
import sys

import pygame
from settings import *
from ray_casting import ray_casting
from collections import deque





class Drawing():
    def __init__(self, sc, player, clock):
        self.sc = sc
        self.clock = clock
        self.player = player
        self.font = pygame.font.SysFont('Arial', 36, bold=True)
        self.textures = {1: pygame.image.load('data/textures/forest1.png').convert(),
                         2: pygame.image.load('data/textures/forest1.png').convert(),
                         3: pygame.image.load('data/textures/forest1.png').convert(),
                         4: pygame.image.load('data/textures/forest1.png').convert(),
                         5: pygame.image.load('data/textures/sky.png').convert(),
                         6: pygame.image.load('data/textures/grass.jpg').convert()}
        # menu
        self.menu_trigger = True
        self.menu_picture = pygame.image.load('data/menu/test.jpg').convert()


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
        self.shot_sound = pygame.mixer.Sound('data/sounds/weapon/shotgun/shot1.mp3')
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
            if not self.shot_lenght_count:
                self.shot_sound.set_volume(0.2)
                self.shot_sound.play()
            self.shot_proj = min(shots)[1] // 2
            self.bullet_sfx()
            shot_sprite = self.weapon_shot_animation[0]
            self.sc.blit(shot_sprite, self.weapon_pos)
            self.shot_animation_count += 1
            if self.shot_animation_count == self.shot_animation_speed:
                self.weapon_shot_animation.rotate(-1)
                self.shot_animation_count = 0
                self.shot_lenght_count += 1
                self.shot_animation_trigger = True
            if self.shot_lenght_count == self.shot_lenght:
                self.player.shot = False
                self.shot_lenght_count = 0
                self.sfx_lenght_count = 0
                self.shot_animation_trigger = False
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


    def menu(self):
        x = 0
        button_font = pygame.font.Font('data/font/font.ttf', 72)
        label_font = pygame.font.Font('data/font/font1.otf', 300)
        start = button_font.render('START', 1, pygame.Color('lightgray'))
        button_start = pygame.Rect(0, 0, 400, 150)
        button_start.center = half_width, half_height
        exit = button_font.render('EXIT', 1, pygame.Color('lightgray'))
        button_exit = pygame.Rect(0, 0, 400, 150)
        button_exit.center = half_width, half_height + 200

        while self.menu_trigger:
            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.sc.blit(self.menu_picture, (0, 0), (x % width, half_height, width, height))

            pygame.draw.rect(self.sc, black, button_start, border_radius=25, width=10)
            self.sc.blit(start, (button_start.centerx - 130, button_start. centery - 70))

            pygame.draw.rect(self.sc, black, button_exit, border_radius=25, width=10)
            self.sc.blit(exit, (button_exit.centerx - 130, button_exit.centery - 70))

            color = random.randrange(40)
            label = label_font.render('MindLess', 1, (color, color, color))
            self.sc.blit(label, (15, -30))

            pygame.display.flip()
            self.clock.tick(20)