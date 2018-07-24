import csv
import yaml


def load_monster_manual():
    monster_dict = {}
    with open('data/monsters.csv', 'r') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            monster_dict[row['Name']] = row
    with open('data/npcs.csv', 'r') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            monster_dict[row['Name']] = row
    return monster_dict

def load_environment_tags():
    monster_dict = load_monster_manual()
    with open('data/environment_tags.yaml') as f:
        environment_tags = yaml.load(f.read())
    for tag in environment_tags.keys():
        amended_monsters = []
        for monster in environment_tags[tag]:
            monster_data = monster_dict.get(monster['Name'])
            if monster_data is not None:
                merged_data = {**monster, **monster_data}
                merged_data['XP'] = int(merged_data['XP'])
                if merged_data.get('role') is None:
                    merged_data['role'] = 'natural hazard'
                amended_monsters.append(merged_data)
            else:
                print('uh oh!')
        environment_tags[tag] = amended_monsters
    return environment_tags
            
            






