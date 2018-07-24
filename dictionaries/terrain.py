import yaml

def load_terrain():
    with open('data/terrain_tags.yaml') as f:
        terrain_tags = yaml.load(f.read())
    return terrain_tags