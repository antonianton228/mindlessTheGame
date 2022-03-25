import pygame
import sys
import os.path


def get_level():
    if os.path.exists('saves/save.txt'):
        save = open('saves/save.txt')
        level = int(save.readline()[-2:])
    else:
        save = open('saves/save.txt', '+w')
        save.write('level = 00')
        level = 0
        save.close()
    return level

def change_level(level_n):
    pass