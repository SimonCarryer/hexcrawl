import yaml

def load_item_tables():
    item_tables = {}
    with open('data/item_tables.yaml') as f:
        tables = yaml.load(f.read())
    for key, value in tables.items():
        item_tables[key] = {}
        item_tables[key]['items'] = [[x for x in i.values()][0] for i in value]
        item_tables[key]['chance'] = [[x for x in i.keys()][0] for i in value]
    return item_tables

def load_treasure_tables():
    treasure_tables = {}
    column_names = ['chance', 'object_die_n', 'object_die_sides', 'object_value', 'object_type', 'item_die_sides', 'item_table_name']
    with open('data/treasure_tables.yaml') as f:
        tables = yaml.load(f.read())
    for key, values in tables.items():
        treasure_tables[key] = []
        for row in values:
            row = row.split(',')
            treasure_tables[key].append({name: value for name, value in zip(column_names, row)})
    return treasure_tables


if __name__ == '__main__':
    tables = load_treasure_tables()
    print(yaml.dump(tables, default_flow_style=False))
    

