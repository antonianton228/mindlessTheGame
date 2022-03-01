from settings import *

text_map = [
    'WWWWWWWWWWWW',
    'W......W...W',
    'W..WWW...W.W',
    'W....W..WW.W',
    'W..W....W..W',
    'W..W...WWW.W',
    'W....W.....W',
    'WWWWWWWWWWWW'
]

world_map = set()
for i, row in enumerate(text_map):
    for j, char in enumerate(row):
        if char == 'W':
            world_map.add((j * tile, i * tile))