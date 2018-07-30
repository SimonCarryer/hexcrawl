from .hex import Hex
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

    def get_hex_by_coords(self, coords):
        for hex in self.hexes:
            if hex.coords == coords:
                return hex
        raise HexNotFoundError

    def change_current_hex(self, direction):
        current = self.current_hex.coords
        change = self.directions[direction]
        desired = [sum(x) for x in zip(current, change)]
        self.current_hex = self.get_hex_by_coords(desired)

    def encounter(self):
        return self.current_hex.get_encounter()

    def look(self):
        return {'terrain': self.current_hex.terrain, 
                'weather': self.current_hex.get_weather()['name'],
                'places': self.current_hex.get_places(),
                'scenery': self.current_hex.get_scenery()
                }

