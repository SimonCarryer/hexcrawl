from .monster_list import load_environment_tags
from .terrain import load_terrain
from .places import load_places
from .history import load_history
from .xp_values import load_xp_values
from .dungeon_rooms import load_dungeon_rooms
from .magic_items import load_magic_items

environment_tags = load_environment_tags()
terrain_tags = load_terrain()
places = load_places()
history_tags = load_history()
xp_values = load_xp_values()
dungeon_rooms = load_dungeon_rooms()
magic_items = load_magic_items()