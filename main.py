import settings
from playerclass import Player
import maps
from drawingclass import Drawing
from sprites import *
from ray_casting import ray_casting_walls
from npc_ai import Interaction
import storyteller
from lor import Story

pygame.init()
sc = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
sprites = Sprites()
player = Player(sprites)
drawing = Drawing(sc, player, clock)
interaction = Interaction(player, sprites, drawing)

pygame.mouse.set_visible(True)
drawing.menu()
pygame.mouse.set_visible(False)
interaction.play_music()
story = Story(sprites, player, drawing)
world_map = maps.map_call()[1]
flagloop = True
while flagloop:
    if player.is_alive:
        world_map = maps.change_map(world_map)
        player.movement()

        walls, wall_hit = ray_casting_walls(player, drawing.textures, world_map)

        sprites.list_of_objects = sprites.dict_of_objects[storyteller.get_level()]

        drawing.floor_drow(sc)
        drawing.world(walls + [obj.object_locate(player) for obj in sprites.list_of_objects])
        drawing.hp_bar()
        drawing.fps(clock)

        drawing.quest_bar()
        drawing.player_weapon([wall_hit, sprites.sprite_hit])

        interaction.intersection_object()
        interaction.npc_action()
        interaction.acting_object()
        interaction.clear_objects()
        if settings.dialog_draw:
            a = drawing.dialoge_draw(*sprites.sprite_parameters[settings.dialog_draw]['phrases'])
            if settings.dialog_draw == 'fire':
                flagloop = a
                if settings.num_kvest == 3:
                    world_map[2 * tile, 15 * tile] = 4
                    settings.move_next_lvl = True
            settings.dialog_draw = ''
        story.make_kvest()
        settings.num_kvest = story.new_kvest(settings.num_kvest)
        if settings.num_last_kvest != settings.num_kvest:
            settings.num_last_kvest = settings.num_kvest
            story.start_kvest(settings.num_kvest)
    else:
        if not drawing.dialoge_draw("Вы погибли! Начать с последнего сохранения?", 'ДА', 'НЕТ'):
            flagloop = False
        else:
            sprites = Sprites()
            player = Player(sprites)
            drawing = Drawing(sc, player, clock)
            interaction = Interaction(player, sprites, drawing)

    if not flagloop:
        break
    pygame.display.flip()
    clock.tick(120)