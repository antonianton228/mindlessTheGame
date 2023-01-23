import settings


def f1():
    settings.is_quests = False


def f2():
    settings.is_quests = True


class Story:
    def __init__(self, sprites, player, drawing):
        self.drawing = drawing
        self.player = player
        self.sprites = sprites
        self.kvests = {}

    def start_kvest(self, num_kvest):
        self.drawing.dialoge_draw(f'Твое следующее задание: {self.kvests[num_kvest][0]}',
                                  f'{self.kvests[num_kvest][4]}', f'{self.kvests[num_kvest][5]}')

    def new_kvest(self, num_kvest):
        settings.needed_speaker = self.kvests[num_kvest][2]
        self.kvests[num_kvest][3]()
        if self.kvests[num_kvest][1]:
            return num_kvest + 1
        settings.name_quest = self.kvests[num_kvest][0]
        return num_kvest

    def make_kvest(self):
        self.kvests = {
            1: [
                'Идите на заправку',
                settings.level == 1,
                '',
                f2,
                'Да, я иду',
                'Надо немного подождать'
            ],
            2: [
                'Убейте всех врагов',
                not list(filter(lambda x: x.name == 'square' and not x.is_dead,
                                self.sprites.dict_of_objects[settings.level])),
                'None1',
                f2,
                'Да, я иду',
                'Надо немного подождать'
            ],
            3: [
                'Поговори с огнём',
                settings.quest_trigger1,
                'fire',
                f1,
                'Да, я иду',
                'Надо немного подождать'
            ],
            4: [
                'На выход',
                False,
                'None',
                f2,
                'Да, я иду',
                'Надо немного подождать'
            ]
        }
