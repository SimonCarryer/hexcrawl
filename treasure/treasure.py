from dictionaries import magic_items, treasure_tables
import random
import bisect

class Treasure:
    def __init__(self, level):
        self.level = level

    def roll_on_treasure_tables(self, table_name):
        chances = treasure_tables[table_name]['chance']
        items = treasure_tables[table_name]['items']
        roll = random.randint(1, 100)
        index = bisect.bisect_left(chances, roll)
        return items[index]


