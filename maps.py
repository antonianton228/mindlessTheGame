from settings import *

text_map = [
    'WWWWWWWWWWWW',
    'W....WWWW..W',
    'W..........W',
    'W...WWWW...W',
    'W..WW......W',
    'W....WW...W',
    'W......WW..W',
    'WWWWWWWWWWWW'
]

world_map = set()
for i, row in enumerate(text_map):
    for j, char in enumerate(row):
        if char == 'W':
            world_map.add((j * tile, i * tile))