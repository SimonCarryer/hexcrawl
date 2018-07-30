from encounters import Encounter
from places import Place
from dictionaries import environment_tags, terrain_tags, history_tags
from random import choice
from numpy.random import choice as np_choice


class Hex:
    def __init__(self, *initial_data, **kwargs):
        for dictionary in initial_data:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        for key in kwargs:
            setattr(self, key, kwargs[key])
        if not hasattr(self, 'history'):
            self.history = []
        if hasattr(self, 'place_names'):
            places = {}
            for place_name in self.place_names:
                places[place_name] = Place(place_name)
            self.places = places
        else:
            self.places = {}

    def get_scenery(self):
        locations = []
        for terrain_type in self.terrain:
            locations += terrain_tags[terrain_type]['terrain features']
        for history_type in self.history:
            locations += history_tags[history_type]['landmarks']
        return choice(locations)

    def get_encounter(self):
        monster_list = environment_tags[choice(self.environment)]
        encounter = Encounter(self.challenge)
        encounter.pick_monsters(monster_list)
        return encounter.display()

    def get_weather(self):
        occurrence = np_choice(['rare', 'uncommon', 'common'], 1, p=[0.1, 0.3, 0.6])[0]
        terrain = choice(self.terrain)
        weather_options = [weather for weather in terrain_tags[terrain]['weather'] if weather['occurrence'] == occurrence]
        return choice(weather_options)

    def get_places(self):
        return [i for i in self.places.keys()]

    def distance(self, coords):
        a = self.coords[0] - coords[0]
        b = self.coords[1] - coords[1]
        return (a, b)

    def absolute_distance(self, coords):
        distance = self.distance(coords)
        return max([abs(i) for i in distance])

    def direction(self, distance):
        a = 0
        b = 0
        if distance[0] == 0:
            a = 0
            b = 1
        elif distance[1] == 0:
            a = 1
            b = 0
        else:
            if round(distance[0]/distance[1]) > 0:
                a = 1
            elif round(distance[0]/distance[1]) < 0:
                a = -1
            if round(distance[1]/distance[0]) > 0:
                b = 1
            elif round(distance[1]/distance[0]) < 0:
                b = -1
        return (a, b)

    def visible_terrain(self, coords, view_distance):
        distance = self.distance(coords)
        abs_distance = self.absolute_distance(coords)
        for terrain in self.terrain:
            if terrain_tags[terrain]['view distance'] + view_distance > abs_distance:
                yield (terrain, abs_distance, self.direction(distance))



