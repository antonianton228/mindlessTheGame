import math
from settings import *
import pygame
import maps
from storyteller import change_level
import settings

collision_walls = maps.map_call()[0]

class Player:
    def __init__(self, sprites):
        self.x, self.y = player_pos
        self.sprites = sprites
        self.angle = player_angle
        self.sensivity = 0.002
        # collision
        self.side = 50
        self.rect = pygame.Rect(*player_pos, self.side, self.side)
        self.flag1 = True  # это кринж но подругому не сделать
        self.flag2 = True  # это кринж но подругому не сделать
        self.flag = True  # это кринж но подругому не сделать
        # weapon
        self.shot = False

        self.checkpoint_dict = {0: [range(125, 175), range(15, 90), 1],
                                1: [range(1251, 1751), range(15, 90), 2],
                                2: [range(1251, 1751), range(15, 90), 3],
                                } # [2] - след. уровень




    @property
    def pos(self):
        if int(self.y) in self.checkpoint_dict[level][0] and int(self.x) in self.checkpoint_dict[level][1]:
            change_level(self.checkpoint_dict[level][2], self)
            self.x, self.y = 150, 350
        return self.x, self.y

    def collision_list(self):
        return maps.map_call()[0] + [pygame.Rect(*obj.pos, obj.side, obj.side) for obj in
                                  self.sprites.list_of_objects if obj.blocked]





    def movement(self):
        self.get_key()
        self.mouse_control()
        self.rect.center = self.x, self.y
        self.angle %= double_pi



    def detect_collision(self, dx, dy):
        self.flag = True
        self.flag1 = True
        self.flag2 = True
        next_rect = self.rect.copy()
        next_rect.move_ip(dx, dy)
        hit_indexes = next_rect.collidelistall(self.collision_list())
        if len(hit_indexes):
            delta_x, delta_y = 0, 0
            for hit_index in hit_indexes:
                hit_rect = self.collision_list()[hit_index]
                if dx > 0:
                    delta_x += next_rect.right - hit_rect.left
                else:
                    delta_x += hit_rect.right - next_rect.left
                if dy > 0:
                    delta_y += next_rect.bottom - hit_rect.top
                else:
                    delta_y += hit_rect.bottom - next_rect.top
            if abs(delta_x - delta_y) < 10:
                dx, dy = 0, 0
                self.flag = False
            elif delta_x > delta_y:
                dy = 0
                self.flag1 = False
            elif delta_y > delta_x:
                dx = 0
                self.flag2 = False

        self.x += dx
        self.y += dy



    def get_key(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            exit()

        if keys[pygame.K_w]:
            dx = player_speed * cos_a
            dy = player_speed * sin_a
            self.detect_collision(dx, dy)
        if keys[pygame.K_s]:
            dx = -player_speed * cos_a
            dy = -player_speed * sin_a
            self.detect_collision(dx, dy)
        if keys[pygame.K_a]:
            dx = player_speed * sin_a
            dy = -player_speed * cos_a
            self.detect_collision(dx, dy)
        if keys[pygame.K_d]:
            dx = -player_speed * sin_a
            dy = player_speed * cos_a
            self.detect_collision(dx, dy)
        if keys[pygame.K_1]:
            if settings.weapon_in_hand != 1:
                settings.weapon_in_hand = 1
                settings.weapon_in_hand_trigger = True
        if keys[pygame.K_2]:
            if settings.weapon_in_hand != 2:
                settings.weapon_in_hand = 2
                settings.weapon_in_hand_trigger = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not self.shot:
                    self.shot = True

        return self.x, self.y, self.angle

    def mouse_control(self):
        if pygame.mouse.get_focused():
            diff = pygame.mouse.get_pos()[0] - half_width
            pygame.mouse.set_pos((half_width, half_height))
            self.angle += diff * self.sensivity
        return self.angle

    def movement_floor(self, posx, posy, rot, keys, et):
        return 0, 0, 0
        # if self.flag:
        #     if keys[pygame.K_LEFT] or keys[ord('a')]:
        #         px, py = np.sin(rot) * 0.002 * et, np.cos(rot) * 0.002 * et
        #         posx, posy = posx + px, posy - py
        #
        #     if keys[pygame.K_RIGHT] or keys[ord('d')]:
        #         posx, posy = posx - np.sin(rot) * 0.002 * et, posy + np.cos(rot) * 0.002 * et
        #
        #     if keys[pygame.K_UP] or keys[ord('w')]:
        #         posx, posy = posx + np.cos(rot) * 0.002 * et, posy + np.sin(rot) * 0.002 * et
        #
        #     if keys[pygame.K_DOWN] or keys[ord('s')]:
        #         posx, posy = posx - np.cos(rot) * 0.002 * et, posy - np.sin(rot) * 0.002 * et
        #     rot = self.mouse_control()
        #     if not self.flag1:
        #         posy = 0
        #     if not self.flag2:
        #         posx = 0
        #     return posx, posy, rot
        # else:
        #     return 0, 0, rot