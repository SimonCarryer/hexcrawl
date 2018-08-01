from encounters import Encounter
from places import Place
from dictionaries import environment_tags, terrain_tags, history_tags, xp_values
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
            self.places = {}
            for place_name in self.place_names:
                self.places[place_name] = Place(place_name)
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
        encounter.pick_monsters(monster_list['monsters'])
        return encounter.display()

    def get_weather(self):
        occurrence = np_choice(['rare', 'uncommon', 'common'], 1, p=[0.1, 0.3, 0.6])[0]
        terrain = choice(self.terrain)
        weather_options = [weather for weather in terrain_tags[terrain]['weather'] if weather['occurrence'] == occurrence]
        return choice(weather_options)

    def worst_monster(self):
        max_challenge = xp_values[self.challenge]
        monsters = []
        for tag in self.environment:
            monsters += environment_tags[tag]['monsters']
        return sorted([monster for monster in monsters if monster['XP'] <= max_challenge], key=lambda k: k['XP'])[-1]['Name']
        

    def get_signs(self):
        tag = choice(self.environment)
        signs = environment_tags[tag]['signs']
        sign = choice(signs)
        worst_monster = self.worst_monster()
        return '%s (%s), tracks indicate a %s' % (sign, tag, worst_monster)

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
        sign = lambda x: (1, -1)[x < 0]
        a = 0
        b = 0
        if distance[0] == 0:
            a = 0
            b = 1
        elif distance[1] == 0:
            a = 1
            b = 0
        else:
            if round(abs(distance[0])/(abs(distance[1]))) > 0:
                a = 1
            if round(abs(distance[1])/abs(distance[0])) > 0:
                b = 1
        return (a*sign(distance[0]), b*sign(distance[1]))

    def visible_terrain(self, coords, view_distance):
        distance = self.distance(coords)
        abs_distance = self.absolute_distance(coords)
        for terrain in self.terrain:
            if terrain_tags[terrain]['view distance'] + view_distance > abs_distance:
                yield (terrain, abs_distance, self.direction(distance))


    def rumours(self, coords, rumour_distance=0):
        distance = self.distance(coords)
        abs_distance = self.absolute_distance(coords)
        for name, place in self.places.items():
            if place.infamy + rumour_distance > abs_distance:
                yield (name, place.get_rumours(), abs_distance, self.direction(distance))


