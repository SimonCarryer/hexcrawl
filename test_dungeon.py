from dungeons import Dungeon

dungeon = Dungeon({'style': 'dungeon', 'purpose': 'stronghold'})

dungeon.base_dungeon()

dungeon.populate_dungeon('immortal guardians', 3, 'haunted')
dungeon.populate_dungeon('hideout', 2, 'bandits')

dungeon.write_module()

dungeon.save_dungeon_image()