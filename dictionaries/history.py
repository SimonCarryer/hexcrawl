import yaml

def load_history():
    with open('data/history.yaml') as f:
        history = yaml.safe_load(f.read())
    return history
