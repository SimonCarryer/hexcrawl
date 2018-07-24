from encounters import Encounter
from dictionaries import environment_tags, terrain_tags
from random import choice


class Hex:
    def __init__(self, *initial_data, **kwargs):
        for dictionary in initial_data:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def get_encounter(self):
        terrain = choice(self.terrain)
        location = choice(terrain_tags[terrain]['terrain features'])
        monster_list = environment_tags[choice(self.environment)]
        encounter = Encounter(self.challenge)
        encounter.pick_monsters(monster_list)
        return {'encounter': encounter.display(), 'location': location}

    def get_weather(self):
        terrain = choice(self.terrain)
        return choice(terrain_tags[terrain]['weather'])



