from tilemap import TileMap
import pygame

class Level:
    def __init__(self, csv_path):
        self.tilemap = TileMap(csv_path)

    def update(self):
        pass  # sau này có thể thêm logic enemy, camera, events...

    def draw(self, surface):
        self.tilemap.draw_map(surface)

    def get_tiles(self):
        return self.tilemap.tiles
