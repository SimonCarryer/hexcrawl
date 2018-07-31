from random import choice
from dictionaries import places, environment_tags
from encounters import Encounter


class Place:
    def __init__(self, name):
        super(Place, self)
        for key in places[name]:
            setattr(self, key, places[name][key])

    def get_encounter(self):
        monster_list = environment_tags[choice(self.inhabitants)]['monsters']
        encounter = Encounter(self.challenge)
        encounter.pick_monsters(monster_list)
        return encounter.display()

    def explore(self):
        return {'description': self.description,
                'dungeons': self.dungeons,
                'encounter': self.get_encounter()}
            
    def get_rumours(self):
        return choice(self.rumours)