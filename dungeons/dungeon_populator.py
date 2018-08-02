from dictionaries import environment_tags
from encounters import Encounter

class DungeonPopulator:
    def __init__(self, dungeon):
        self.dungeon = dungeon
        self.style = 'hideout'
        self.level = 2
        self.monsters = environment_tags['bandits']['monsters']

    def populate(self):
        style_dict = {'hideout': self.hideout}
        method = style_dict[self.style]
        method()

    def hideout(self):
        # populates back of dungeon with a tough boss, and entrance with some guards. Odd stuff in between.

    