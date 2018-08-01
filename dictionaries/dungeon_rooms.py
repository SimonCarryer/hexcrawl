import yaml

def load_dungeon_rooms():
    with open('dungeons.yaml', 'r') as f:
        dungeon_rooms = yaml.load(f)
        return dungeon_rooms