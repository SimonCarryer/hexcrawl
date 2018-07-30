from encounters import Encounter
from places import Place
from dictionaries import environment_tags, terrain_tags
from random import choice
from numpy.random import choice as np_choice


class Hex:
    def __init__(self, *initial_data, **kwargs):
        for dictionary in initial_data:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        for key in kwargs:
            setattr(self, key, kwargs[key])
        if hasattr(self, 'place_names'):
            places = {}
            for place_name in self.place_names:
                places[place_name] = Place(place_name)
            self.places = places
        else:
            self.places = {}

    def get_encounter(self):
        terrain = choice(self.terrain)
        location = choice(terrain_tags[terrain]['terrain features'])
        monster_list = environment_tags[choice(self.environment)]
        encounter = Encounter(self.challenge)
        encounter.pick_monsters(monster_list)
        return {'encounter': encounter.display(), 'location': location}

    def get_weather(self):
        occurrence = np_choice(['rare', 'uncommon', 'common'], 1, p=[0.1, 0.3, 0.6])[0]
        terrain = choice(self.terrain)
        weather_options = [weather for weather in terrain_tags[terrain]['weather'] if weather['occurrence'] == occurrence]
        return choice(weather_options)

    def get_places(self):
        return [i for i in self.places.keys()]



