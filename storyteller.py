import os.path
import settings

dialog_person = ''
weapon_damage = 0


def get_level():
    if os.path.exists('saves/save.txt'):
        save = open('saves/save.txt')
        level1 = int(save.readline()[-2:])
    else:
        save = open('saves/save.txt', '+w')
        save.write('level = 00')
        level1 = 0
    save.close()
    return level1


def change_level(level_n, player):
    save = open('saves/save.txt', '+w')
    save.write(f'level = {level_n}')
    save.close()
    settings.level = level_n
