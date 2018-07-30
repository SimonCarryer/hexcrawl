from dictionaries import places


class Place:
    def __init__(self, name):
        for key in places[name]:
            setattr(self, key, places[name][key])