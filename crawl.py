from hex import Map


current_map = Map()

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
