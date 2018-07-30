from .monster_list import load_environment_tags
from .terrain import load_terrain
from .places import load_places

environment_tags = load_environment_tags()
terrain_tags = load_terrain()
places = load_places()