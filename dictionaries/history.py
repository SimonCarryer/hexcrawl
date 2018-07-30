import yaml

def load_history():
    with open('data/history.yaml') as f:
        history = yaml.load(f.read())
    return history