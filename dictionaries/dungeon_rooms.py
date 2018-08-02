import yaml

def load_dungeon_rooms():
    with open('data/dungeon_rooms.yaml', 'r') as f:
        dungeon_rooms = yaml.load(f)
        i = 0
        for purpose in dungeon_rooms.keys():
            for room in dungeon_rooms[purpose]:
                room['room_id'] = i
                i += 1
        return dungeon_rooms