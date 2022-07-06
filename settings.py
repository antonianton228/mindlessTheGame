import math
import numpy as np
import pygame
import storyteller

# game settings
width = 1200
height = 800
half_width = width // 2
half_height = height // 2
double_height = height * 2

FPS = 65
tile = 100


# ray casting settings
fov = math.pi / 3
half_fov = fov / 2
num_rays = 600
max_depth = 800
penta_height = 5 * height
delta_angle = fov / num_rays
dist = num_rays / (2 * math.tan(half_fov))
dist = num_rays / (2 * math.tan(half_fov))
proj_coof = dist * tile * 1.5
scale = width // num_rays

# sprites
double_pi = 2 * math.pi
center_ray = num_rays // 2 - 1
fake_rays = 100
fake_rays_range = num_rays - 1 + 2 * fake_rays


# textures
texture_width = 1200
texture_height = 1200
half_texture_height = texture_height // 2
texture_scale = texture_width // tile


# player settings
player_pos = (half_width // 4, half_height - 50)
player_angle = 0
player_speed = 5


# colors
black = (0, 0, 0)
green = (0, 255, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
darkgrey = (100, 100, 100)
yellow = (255, 255, 0)
skyblue = (9, 3, 29)
red = (255, 0, 0)
grassgreen = (10, 1, 28)


# SAVE
level = storyteller.get_level()

# weapon
weapon_in_hand = 1
weapon_in_hand_trigger = False
dialog_draw = False

# story
num_kvest = 1
name_quest = ""
num_last_kvest = 0
needed_speaker = ''
is_quests = True
quest_trigger1 = False
quest_trigger2 = False
quest_trigger3 = False