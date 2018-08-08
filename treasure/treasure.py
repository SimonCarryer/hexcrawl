from dictionaries import treasure_tables, item_tables
import random
import bisect

class Treasure:
    def __init__(self, level):
        self.level = level

    def find_appropriate_treasure_table(self):
        levels = sorted([i for i in treasure_tables.keys()])
        level = levels[bisect.bisect_left(levels, self.level)]
        return treasure_tables[level]

    def get_objects(self, die_n, die_sides, object_type, value):
        if die_n == '':
            return "No art objects or gems."
        roll = sum([random.randint(1, int(die_sides)) for _ in range(int(die_n))])
        total = int(roll)*int(value)
        return "%d %ss of value %dgp each (total %dgp)" % (int(roll), object_type, int(value), total)

    def get_items(self, die_sides, table_name):
        if die_sides == '':
            return "No magic items."
        roll = random.randint(1, int(die_sides))
        items = [self.roll_on_item_tables(table_name) for _ in range(roll)]
        return 'The following magic items: ' + ', '.join(items)

    def roll_on_treasure_table(self):
        table = self.find_appropriate_treasure_table()
        chances = [int(i['chance']) for i in table]
        roll = random.randint(1, 100)
        index = bisect.bisect_left(chances, roll)
        row = table[index]
        objects = self.get_objects(row['object_die_n'], row['object_die_sides'], row['object_type'], row['object_value'])
        items = self.get_items(row['item_die_sides'], row['item_table_name'])
        return objects, items

    def roll_on_item_tables(self, table_name):
        chances = sorted(item_tables[table_name]['chance'])
        items = item_tables[table_name]['items']
        roll = random.randint(1, 100)
        index = bisect.bisect_left(chances, roll)
        return items[index]


