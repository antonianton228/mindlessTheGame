from settings import *

class Weapon:
    def __init__(self, base, name, sprite, anim, sound, damage, bullets, sfx, anim_speed):
        self.name = name
        self.weapon_sprite = sprite
        self.weapon_animation = anim
        self.weapon_sound = sound
        self.weapon_damage = damage
        self.col_of_bullets = bullets
        self.weapon_base_sprite = base
        self.weapon_rect = self.weapon_base_sprite.get_rect()
        self.weapon_pos = (half_width - self.weapon_rect.width // 2, height
                           - self.weapon_rect.height)
        self.shot_lenght = len(self.weapon_animation)
        self.shot_animation_speed = anim_speed
        self.shot_animation_count = 0
        self.shot_animation_trigger = True
        self.sfx = sfx
        self.sfx_lenght_count = 0
        self.shot_lenght_count = 0
        self.sfx_lenght = len(self.sfx)