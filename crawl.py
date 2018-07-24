from hex import Map


current_map = Map()
#hex = current_map.get_hex_by_coords([0, 0])

#encounter = current_map.current_hex.get_encounter()

# for monster in environment_tags['haunted']:
#     print(monster['Name'])
#     print(encounter.acceptable_challenge(monster))
#     print(encounter.right_role(monster))
#     print(encounter.right_occurrence(monster))

#print([monster['name'] for monster in encounter.possible_monsters(monsters['spooky forest'])])

user_input = ''

while user_input != 'q':
    user_input = input('where to next? ')
    if user_input == 'e':
        print(current_map.encounter())
    if user_input in ['n', 's', 'ne', 'se', 'nw', 'sw']:
        current_map.change_current_hex(user_input)
    if user_input == 'l':
        print(current_map.look())

#print(encounter.display())
