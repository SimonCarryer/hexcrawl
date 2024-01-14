import yaml

def load_xp_values():
    with open('data/xp_values.yaml') as f:
        xp_values = yaml.safe_load(f.read())
    return xp_values
