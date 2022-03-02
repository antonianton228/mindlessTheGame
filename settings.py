import math


# game settings
width = 1200
height = 800
half_width = width // 2
half_height = height // 2
FPS = 65
tile = 100


# ray casting settings
fov = math.pi / 3
half_fov = fov / 2
num_rays = 300
max_depth = 800
delta_angle = fov / num_rays
dist = num_rays / (2 * math.tan(half_fov))
proj_coof = dist * tile * 3
scale = width // num_rays


# textures
texture_width = 1200
texture_height = 1200
texture_scale = texture_width // tile


# player settings
player_pos = (half_width // 4, half_height - 50)
player_angle = 0
player_speed = 2


# colors
black = (0, 0, 0)
green = (0, 255, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
darkgrey = (100, 100, 100)
yellow = (255, 255, 0)
skyblue = (0, 186, 255)
red = (255, 0, 0)