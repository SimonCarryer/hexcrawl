from .hex import Hex
from collections import defaultdict
from .no_hex_error import HexNotFoundError
from random import choice, randint
import yaml

class Map:
    def __init__(self):
        self.hexes = []
        with open('data/map.yaml') as f:
            hexes = yaml.load(f.read())
        for hex_data in hexes:
            self.hexes.append(Hex(hex_data))
        self.current_hex = self.get_hex_by_coords([0, 0])
        self.directions = {'North': [1, 1], 
                           'South': [-1, -1], 
                           'North-East': [1, 0], 
                           'South-East': [0, -1], 
                           'North-West': [0, 1], 
                           'South-West': [-1, 0], 
                           'East': [1, -1], 
                           'West': [-1, 1]}
        self.reversed_directions = {tuple(value): key for key, value in self.directions.items()}

    def get_hex_by_coords(self, coords):
        for hex_ in self.hexes:
            if hex_.coords == coords:
                return hex_
        raise HexNotFoundError

    def neighbours(self):
        for direction, value in self.directions.items():
            coords = [sum([a, b]) for a, b in zip(self.current_hex.coords, value)]
            try:
                yield (self.get_hex_by_coords(coords), direction)
            except HexNotFoundError:
                pass

    def valid_directions(self):
        all_directions = ['North', 'South', 'North-East', 'South-East', 'North-West', 'South-West']
        possible = []
        current = self.current_hex.coords
        for direction in all_directions:
            change = self.directions[direction]
            desired = [sum(x) for x in zip(current, change)]   
            try:
                self.get_hex_by_coords(desired)
                possible.append(direction)
            except HexNotFoundError:
                pass
        return possible

    def change_current_hex(self, direction):
        current = self.current_hex.coords
        change = self.directions[direction]
        desired = [sum(x) for x in zip(current, change)]
        try:
            self.current_hex = self.get_hex_by_coords(desired)
        except HexNotFoundError:
            print("You can't go that way - there's nothing there.")

    def neighbouring_encounter(self):
        encounter = {}
        neighbour, direction = choice([neighbour for neighbour in self.neighbours()])
        encounter['monsters'] = neighbour.get_encounter()
        encounter['notes'] = 'Wandering from %s' % direction
        encounter['location'] = self.current_hex.get_scenery()
        return encounter
    
    def encounter(self):
        if randint(1, 6) == 1:
            encounter = self.neighbouring_encounter()
        else:
            encounter = {}
            encounter['monsters'] = self.current_hex.get_encounter()
            encounter['location'] = self.current_hex.get_scenery()
        return encounter

    def get_encounter_set(self, n=3):
        return [self.encounter() for i in range(n)]

    def visible_terrain(self, visibility):
        for hex_ in self.hexes:
            if hex_.coords != self.current_hex.coords:
                for terrain in hex_.visible_terrain(self.current_hex.coords, visibility):
                    yield terrain

    def visible_places(self, visibility):
        for hex_ in self.hexes:
            if hex_.coords != self.current_hex.coords:
                for place in hex_.visible_places(self.current_hex.coords, visibility):
                    yield place

    def signs(self):
        return self.current_hex.get_signs()

    def rumours(self):
        for hex_ in self.hexes:
            yield hex_.rumours(self.current_hex.coords)

    def parse_visible_terrain(self, visibility):
        parsed = defaultdict(set)
        visible_terrain = [terrain for terrain in self.visible_terrain(visibility)]
        visible_places = [place for place in self.visible_places(visibility)]
        visible = visible_places + visible_terrain
        for terrain, distance, direction in visible:
            parsed[self.reversed_directions[direction]].add((terrain, distance))
        return [{'direction': direction, 'visible': list(visible)} for direction, visible in parsed.items()]

    def parse_rumours(self):
        parsed = defaultdict(set)
        rumours = [rumour for rumour in self.rumours()]
        for rumour_set in rumours:
            for name, rumour, distance, direction in rumour_set:
                parsed[self.reversed_directions[direction]].add((name, rumour, distance))
        return [{'direction': direction, 'rumour': list(rumour)} for direction, rumour in parsed.items()]

    def look(self):
        weather = self.current_hex.get_weather()
        return {'terrain': self.current_hex.terrain,
                'visible': self.parse_visible_terrain(weather['visibility']), 
                'weather': weather,
                'places': self.current_hex.get_places(),
                'scenery': self.current_hex.get_scenery(),
                'rumours': self.parse_rumours(),
                'signs': self.signs()
                }