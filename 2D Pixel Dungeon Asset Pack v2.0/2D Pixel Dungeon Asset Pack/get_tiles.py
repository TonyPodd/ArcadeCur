import arcade

TILE_SIZE = 16
COLUMNS = 10
ROWS = 10

def load_tiles(path="Dungeon_Tileset.png"):
    return arcade.load_spritesheet(
        path,
        sprite_width=TILE_SIZE,
        sprite_height=TILE_SIZE,
        columns=COLUMNS,
        count=COLUMNS * ROWS
    )

# sheet1 = arcade.SpriteSheet("Dungeon_Character_2.png")

# tile_width1 = sheet1.image.width // 7
# tile_height1 = sheet1.image.height // 2
# textures1 = sheet1.get_texture_grid(
#     size=(tile_width1, tile_height1), 
#     columns=10, 
#     count=100
# )