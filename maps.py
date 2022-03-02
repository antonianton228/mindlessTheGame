from settings import *

text_map = [
    '111111111111',
    '1.....2....1',
    '1.22.....2.1',
    '1..........1',
    '1.22.......1',
    '1.2......2.1',
    '1.....2....1',
    '111111111111'
]

world_map = {}
for i, row in enumerate(text_map):
    for j, char in enumerate(row):
        if char == '1':
            world_map[(j * tile, i * tile)] = 1
        elif char == '2':
            world_map[(j * tile, i * tile)] = 2