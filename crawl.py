from hex import Map


current_map = Map()

user_input = ''

while user_input != 'q':
    user_input = input('where to next? ')
    if user_input == 'e':
        print(current_map.encounter())
    if user_input in ['n', 's', 'ne', 'se', 'nw', 'sw']:
        dir_dict = {
            'n': 'North', 
            's': 'South', 
            'ne': 'North-East', 
            'se': 'South-East', 
            'nw': 'North-West', 
            'sw': 'South-West'
        }
        current_map.change_current_hex(dir_dict[user_input])
        print(current_map.look())
    if user_input == 'l':
        print(current_map.look())
    if user_input[:2] == 'e ':
        try:
            place = current_map.current_hex.places[user_input[2:]]
            print(place.explore())
        except KeyError:
            print("That's not a place")

