from dictionaries import environment_tags
from encounters import DirectedEncounter, Encounter
from treasure import Treasure
import networkx as nx
import random

class DungeonPopulator:
    def __init__(self, dungeon, style, level, monsters):
        self.dungeon = dungeon
        self.style = style
        style_dict = {'hideout': {'method': self.hideout, 'colour': 'r'},
                      'immortal guardians': {'method': self.immortal_guardians, 'colour': 'black'}
        }
        self.populate = style_dict[style]['method']
        self.colour = style_dict[style]['colour']
        self.level = level
        self.monsters = environment_tags[monsters]['monsters']

    def decide_whether_to_explore_further(self):
        return len(self.explored_nodes) + random.randint(1, 3) < self.explore_depth   

    def explore(self, dungeon, node):
        self.explored_nodes.append(node)
        neighbours = dungeon.neighbors(node)
        possible_routes = [neighbour for neighbour in neighbours if neighbour not in self.explored_nodes]
        new_nodes = [new_node for new_node in possible_routes if dungeon.get_edge_data(node, new_node)['weight'] == 1]
        if len(new_nodes) > 0:
            if self.decide_whether_to_explore_further():
                new_direction = random.choice(new_nodes)
                self.explore(dungeon, new_direction)
        else:
           return

    def hideout(self):
        dungeon = self.dungeon
        self.explore_depth = 6
        self.explored_nodes = []
        # populates back of dungeon with a tough boss, and entrance with some guards. Odd stuff in between.
        # see what else they've explored:
        self.explore(dungeon, 0)
        for node, node_data in dungeon.nodes(data=True):
            if node in self.explored_nodes:
                node_data['colour'] = self.colour
        # put some encounters in there
        subgraph = dungeon.subgraph(self.explored_nodes)
        nodes = subgraph.nodes(data=True)
        paths = {a: len(nx.shortest_path(subgraph, 0, a)) for a, node in nodes}
        max_path = max(paths.values())
        final_room = random.choice([key for key, value in paths.items() if value == max_path])
        main_route = nx.shortest_path(subgraph, 0, final_room)
        for a, node in nodes:
            if a == final_room:
                encounter = DirectedEncounter(self.level, style='boss')
                encounter.pick_monsters(self.monsters)
                node['encounter'] = encounter.display()
                t = Treasure(self.level)
                node['treasure'] = t.roll_on_treasure_table()
            elif a == 0:
                encounter = DirectedEncounter(self.level, style='guards')
                encounter.pick_monsters(self.monsters)
                node['encounter'] = encounter.display()
            elif a not in main_route:
                roll = random.randint(1, 6)
                if roll > 3:
                    encounter = DirectedEncounter(self.level, style='elite')
                    encounter.pick_monsters(self.monsters)
                    node['encounter'] = encounter.display()
            else:
                roll = random.randint(1, 6)
                if roll > 3:
                    encounter = DirectedEncounter(self.level, style='basic')
                    encounter.pick_monsters(self.monsters)
                    node['encounter'] = encounter.display()

    def immortal_guardians(self):
        dungeon = self.dungeon
        # guardians left by the original inhabitants. They guard secret and important areas.
        for node, node_data in dungeon.nodes(data=True):
            node_data['colour'] = self.colour
            if 'important' in node_data['tags']:
                encounter = Encounter(self.level)
                encounter.pick_monsters(self.monsters)
                node_data['encounter'] = encounter.display()
            elif 'secret' in node_data['tags']:
                encounter = Encounter(self.level)
                encounter.pick_monsters(self.monsters)
                node_data['encounter'] = encounter.display()
