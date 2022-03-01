from settings import *

text_map = [
    'WWWWWWWWWWWWWWW',
    'W.............W',
    'WWWWWWW..WWWWWW',
    'W.............W',
    'W......WWWWWWWW',
    'WWWWWW........W',
    'W........WWWWWW',
    'WWWWWWWWWWWWWWW'
]

world_map = set()
for i, row in enumerate(text_map):
    for j, char in enumerate(row):
        if char == 'W':
            world_map.add((j * tile, i * tile))