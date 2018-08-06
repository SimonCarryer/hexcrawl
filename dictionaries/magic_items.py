import csv

def load_magic_items():
    magic_items = []
    with open('data/monsters.csv', 'r') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            magic_items.append(row)
    return magic_items