import yaml

def load_terrain():
    with open('data/terrain_tags.yaml') as f:
        terrain_tags = yaml.load(f.read())
    with open('data/weather.yaml') as f:
        weather = yaml.load(f.read())
    for terrain_type in terrain_tags.keys():
        weather_types = []
        for weather_type in terrain_tags[terrain_type]['weather']:
            weather_types.append({**weather_type, **weather[weather_type['name']]})
        terrain_tags[terrain_type]['weather'] = weather_types
    return terrain_tags