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
        self.directions = {'n': [1, 1], 's': [-1, -1], 'ne': [1, 0], 'se': [-1, 0], 'nw': [0, 1], 'sw': [-1, 0]}
        self.reversed_directions = {tuple(value): key for key, value in self.directions.items()}

    def get_hex_by_coords(self, coords):
        for hex in self.hexes:
            if hex.coords == coords:
                return hex
        raise HexNotFoundError

    def neighbours(self):
        for direction, value in self.directions.items():
            coords = [sum([a, b]) for a, b in zip(self.current_hex.coords, value)]
            try:
                yield (self.get_hex_by_coords(coords), direction)
            except HexNotFoundError:
                pass

    def change_current_hex(self, direction):
        current = self.current_hex.coords
        change = self.directions[direction]
        desired = [sum(x) for x in zip(current, change)]
        self.current_hex = self.get_hex_by_coords(desired)

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

    def visible_terrain(self, visibility):
        for hex_ in self.hexes:
            if hex_ != self.current_hex:
                for terrain in hex_.visible_terrain(self.current_hex.coords, visibility):
                    yield terrain

    def parse_visible_terrain(self, visibility):
        parsed = defaultdict(set)
        visible = [terrain for terrain in self.visible_terrain(visibility)]
        for terrain, distance, direction in visible:
            parsed[self.reversed_directions[direction]].add((terrain, distance))
        return dict(parsed)

    def look(self):
        weather = self.current_hex.get_weather()
        return {'terrain': self.current_hex.terrain,
                'visible': self.parse_visible_terrain(weather['visibility']), 
                'weather': weather['name'],
                'places': self.current_hex.get_places(),
                'scenery': self.current_hex.get_scenery()
                }