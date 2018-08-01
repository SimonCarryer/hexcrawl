import networkx as nx
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
import random
from dictionaries import dungeon_rooms

dungeon_styles = {'caves': {'connectivity': 1.0, 'rooms': (2, 5), 'class': 'natural', 'colour': 'r'},
                  'dungeon': {'connectivity': 1.2, 'rooms': (4, 8), 'class': 'built', 'colour': 'b'},
                  'tunnels': {'connectivity': 1.8, 'rooms': (3, 6), 'class': 'built', 'colour': 'g'},
                  'tomb': {'connectivity': 0.5, 'rooms': (2, 3), 'class': 'built', 'colour': 'black'}
                 }

class Dungeon:
    def __init__(self, *initial_data, **kwargs):
        for dictionary in initial_data:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        for key in kwargs:
            setattr(self, key, kwargs[key])
        if not hasattr(self, 'style'):
            self.style = 'dungeon'
        if not hasattr(self, 'purpose'):
            self.purpose = random.choice(['tomb', 'stronghold'])

    def base_dungeon(self, initial_room=0):
        dungeon = nx.Graph()
        rooms_min, rooms_max = dungeon_styles[self.style]['rooms']
        threshold = dungeon_styles[self.style]['connectivity']
        colour = dungeon_styles[self.style]['colour']
        class_ = dungeon_styles[self.style]['class']
        n_rooms = random.randint(rooms_min, rooms_max)
        for i in range(initial_room, initial_room+n_rooms):
            dungeon.add_node(i,colour=colour, class_=class_, style=self.style, purpose=self.purpose, tags=[])
        while nx.average_node_connectivity(dungeon) < threshold:
            rooms = random.sample(dungeon.nodes(), 2)
            dungeon.add_edge(rooms[0], rooms[1], style='solid', weight=1)
        self.label_secret_areas(dungeon)
        self.fix_unjoined_areas(dungeon)
        self.assign_rooms(dungeon)
        self.graph = dungeon

    def fix_unjoined_areas(self, dungeon):
        connected_components = [i for i in nx.connected_components(dungeon)]
        if len(connected_components) > 1:
            for idx in range(len(connected_components)-1):
                room = random.sample(connected_components[idx], 1)[0]
                connecting_room = random.sample(connected_components[idx+1], 1)[0]
                dungeon.add_edge(room, connecting_room, style='dashed', weight=2)

    def label_secret_areas(self, dungeon):
        connected_components = [i for i in nx.connected_components(dungeon)]
        if len(connected_components) > 1:
            for component in connected_components:
                if len(component) != max([len(i) for i in connected_components]):
                    for node in component:
                        dungeon.node[node]['tags'].append('secret')

    def choose_room(self, node):
        rooms = dungeon_rooms[node['purpose']]
        suitable_rooms = [room for room in rooms if node['tags'] == [] or any([tag in room.get('tags', []) for tag in node['tags']])]
        return random.choice(suitable_rooms)

    def assign_rooms(self, dungeon):
        nodes = dungeon.nodes(data=True)
        rooms = dungeon_rooms[purpose]
        used_rooms = []
        for a, node in nodes:
            room = choose_room(node)
            node['room'] = room['description']
            used_rooms.append(room['room_id'])

    def save_dungeon_image(self):
        colours = [i[1]['colour'] for i in self.graph.nodes(data=True)]
        styles = [i[2]['style'] for i in self.graph.edges(data=True)]
        edges = {(a, b): 'a' for a, b, c in self.graph.edges(data=True) if c['style'] == 'dashed'}
        pos = nx.spring_layout(self.graph) 
        nx.draw_networkx_edges(self.graph, 
                            pos,
                            styles=styles,
                            edge_labels=edges)
        nx.draw_networkx_nodes(self.graph, 
                            pos,
                            node_color=colours)
        nx.draw_networkx_edge_labels(self.graph, 
                            pos,
                            edge_labels=edges)
        nx.draw_networkx_labels(self.graph,
                            pos,
                            font_color='white',
                            font_weight='bold')
        plt.savefig('dungeon.png')