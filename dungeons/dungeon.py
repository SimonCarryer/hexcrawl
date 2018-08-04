import networkx as nx
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
import random
from dictionaries import dungeon_rooms
from .dungeon_populator import DungeonPopulator

dungeon_styles = {'caves': {'connectivity': 1.0, 'rooms': (3, 5), 'class': 'natural', 'secrets': 0},
                  'dungeon': {'connectivity': 1.2, 'rooms': (4, 8), 'class': 'built', 'secrets': 1},
                  'tunnels': {'connectivity': 1.8, 'rooms': (3, 6), 'class': 'built', 'secrets': 0},
                  'tomb': {'connectivity': 0.6, 'rooms': (3, 4), 'class': 'built', 'secrets': 2}
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
        self.used_rooms = []
        self.colour = 'black'

    def base_dungeon(self, initial_room=0):
        dungeon = nx.Graph()
        rooms_min, rooms_max = dungeon_styles[self.style]['rooms']
        threshold = dungeon_styles[self.style]['connectivity']
        colour = self.colour
        class_ = dungeon_styles[self.style]['class']
        n_rooms = random.randint(rooms_min, rooms_max)
        for i in range(initial_room, initial_room+n_rooms):
            dungeon.add_node(i,colour=colour, class_=class_, style=self.style, purpose=self.purpose, tags=[])
        while nx.average_node_connectivity(dungeon) < threshold:
            rooms = random.sample(dungeon.nodes(), 2)
            dungeon.add_edge(rooms[0], rooms[1], style='solid', weight=1)
        self.add_secrets(dungeon)
        self.label_secret_areas(dungeon)
        self.fix_unjoined_areas(dungeon)
        self.tag_nodes(dungeon)
        self.assign_rooms(dungeon)
        self.populate_dungeon(dungeon)
        self.graph = dungeon

    def add_secrets(self, dungeon):
        if random.randint(1, 6) <= dungeon_styles[self.style]['secrets']:
            max_nodes = len(dungeon.nodes())
            colour = self.colour
            class_ = dungeon_styles[self.style]['class']
            dungeon.add_node(max_nodes, colour=colour, class_=class_, style=self.style, purpose=self.purpose, tags=[])
            if random.randint(1, 6) in [1, 2, 3]:
                dungeon.add_node(max_nodes+1, colour=colour, class_=class_, style=self.style, purpose=self.purpose, tags=[])
                dungeon.add_edge(max_nodes, max_nodes+1, style='solid', weight=1)

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

    def label_edges(self, dungeon):
        biconnected_component_edges = nx.biconnected_component_edges(dungeon)
        for edge, edge_data in dungeon.edges(data=True):
            if edge in biconnected_component_edges:
                edge_data['important'] = True


    def tag_nodes(self, dungeon):
        nodes = [(node, data) for node, data in dungeon.nodes(data=True) if 'secret' not in data['tags']]
        central_nodes = [i for i in nx.articulation_points(dungeon)]
        paths = {a: len(nx.shortest_path(dungeon, 0, a)) for a, node in nodes}
        max_path = max(paths.values())
        for a, node in nodes:
            if a == 0:
                node['tags'].append('entrance')
            if a in central_nodes:
                node['tags'].append('central')
            if paths[a] == max_path:
                node['tags'].append('important')
            if len([i for i in dungeon.neighbors(a)]) == 1:
                node['tags'].append('dead-end')

    def choose_room(self, node):
        rooms = dungeon_rooms[node['purpose']]
        if len(node.get('tags', [])) > 0:
            suitable_rooms = [room for room in rooms if any([tag in room.get('tags', []) for tag in node['tags']])]
        else:
            suitable_rooms = [room for room in rooms if room.get('tags', []) == [] or not any([i not in room.get('tags', []) for i in ['secret', 'important']])]
        final = [room for room in suitable_rooms if room['room_id'] not in self.used_rooms]
        if len(final) > 0:
            room = random.choice(final)
        elif len(suitable_rooms) > 0:
            room = random.choice(suitable_rooms)
        else:
            room = random.choice(rooms)
        self.used_rooms.append(room['room_id'])
        return room

    def assign_rooms(self, dungeon):
        nodes = dungeon.nodes(data=True)
        for a, node in nodes:
            room = self.choose_room(node)
            node['room'] = room['description']

    def populate_dungeon(self, dungeon):
        populator = DungeonPopulator(dungeon)
        populator.populate()

    def write_module(self):
        nodes = self.graph.nodes(data=True)
        for number, node in nodes:
            print(number, node['room'], node.get('encounter', ''))

    def save_dungeon_image(self):
        self.write_module()
        colours = [i[1]['colour'] for i in self.graph.nodes(data=True)]
        styles = [c['style'] for a, b, c in self.graph.edges(data=True)]
        edges = {(a, b): 'a' for a, b, c in self.graph.edges(data=True) if c['style'] == 'dashed'}
        pos = nx.spring_layout(self.graph) 
        nx.draw_networkx_edges(self.graph, 
                            pos,
                            style='dashed',
                            edgelist=[(a, b) for a, b, c in self.graph.edges(data=True) if c['style'] == 'dashed'])
        nx.draw_networkx_edges(self.graph, 
                            pos,
                            style='solid',
                            edgelist = [(a, b) for a, b, c in self.graph.edges(data=True) if c['style'] == 'solid'])
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