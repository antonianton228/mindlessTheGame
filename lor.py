class Story:
    def __init__(self, sprites, player, drawing):
        self.drawing = drawing
        self.player = player
        self.sprites = sprites
        self.kvests = {}

    def start_kvest(self, num_kvest):
        self.drawing.dialoge_draw(self.kvests[num_kvest][0])

    def new_kvest(self, num_kvest):
        if self.kvests[num_kvest][1]:
            return num_kvest + 1
        return num_kvest

    def make_kvest(self):
        self.kvests = {
            1: [
                'Твое первое задание: выстрели с оружия.',
                self.player.shot
            ],
            2: [
                'Твое следующее задание: убей врага.',
                self.sprites.list_of_objects[0].is_dead
            ],
            3: [
                'Твое следующее задание: трахни антона.',
                False
            ]
        }