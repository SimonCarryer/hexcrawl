import yaml

def load_treasure_tables():
    treasure_tables = {}
    with open('data/treasure_tables.yaml') as f:
        tables = yaml.load(f.read())
    for key, value in tables.items():
        treasure_tables[key] = {}
        treasure_tables[key]['items'] = [[x for x in i.values()][0] for i in value]
        treasure_tables[key]['chance'] = [[x for x in i.keys()][0] for i in value]
    return treasure_tables

if __name__ == '__main__':
    tables = load_treasure_tables()
    print(tables['I'])

