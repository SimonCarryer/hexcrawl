import yaml

def load_places():
    with open('data/places.yaml') as f:
        places = yaml.safe_load(f.read())
    return places
