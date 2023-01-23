from settings import *
import pygame
import maps
from storyteller import change_level
import settings

collision_walls = maps.map_call()[0]


class Player:
    def __init__(self, sprites):
        self.player_start_pos_dict = {
            0: (1120, 125),
            1: (200, 200),
            2: (200, 200),
        }
        self.x, self.y = self.player_start_pos_dict[settings.level]
        self.sprites = sprites
        self.angle = player_angle
        self.sensivity = 0.002
        # collision
        self.side = 50
        self.rect = pygame.Rect(*player_pos, self.side, self.side)
        # weapon
        self.shot = False
        # взаимодействие
        self.action = False
        self.hp = 100
        self.is_alive = True

        self.checkpoint_dict = {0: [range(2000, 2300), range(1400, 1500), 1],
                                1: [range(200, 300), range(1400, 1500), 2],
                                2: [range(1251, 1751), range(15, 90), 3],
                                }

    @property
    def pos(self):
        if int(self.x) in self.checkpoint_dict[settings.level][0] and int(self.y) in \
                self.checkpoint_dict[settings.level][1] and settings.move_next_lvl:
            change_level(self.checkpoint_dict[level][2], self)
            settings.change_map = True
            settings.move_next_lvl = False
        return self.x, self.y

    def collision_list(self):
        return maps.map_call()[0] + [pygame.Rect(*obj.pos, obj.side, obj.side) for obj in
                                     self.sprites.list_of_objects if obj.blocked]

    def movement(self):
        self.get_key()
        self.mouse_control()
        self.rect.center = self.x, self.y
        self.angle %= double_pi

    def take_damage(self, n):
        self.hp = self.hp - n
        if self.hp <= 0:
            self.is_alive = False

    def detect_collision(self, dx, dy):
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
            elif delta_x > delta_y:
                dy = 0
            elif delta_y > delta_x:
                dx = 0

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
        if keys[pygame.K_e] and not self.action:
            self.action = True

        return self.x, self.y, self.angle

    def mouse_control(self):
        if pygame.mouse.get_focused():
            diff = pygame.mouse.get_pos()[0] - half_width
            pygame.mouse.set_pos((half_width, half_height))
            self.angle += diff * self.sensivity
        return self.angle
