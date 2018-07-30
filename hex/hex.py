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

    def get_location(self):
        terrain = choice(self.terrain)
        location = choice(terrain_tags[terrain]['terrain features'])
        return location

    def get_encounter(self):
        monster_list = environment_tags[choice(self.environment)]
        encounter = Encounter(self.challenge)
        encounter.pick_monsters(monster_list)
        return encounter.display()

    def get_weather(self):
        terrain = choice(self.terrain)
        return choice(terrain_tags[terrain]['weather'])

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





