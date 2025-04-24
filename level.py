from tile_map import TileMap
import pygame

class Level:
    
    def __init__(self, tilemap_path, spawn_points: dict[str: tuple[int, int]],size):
        self.tilemap = TileMap(tilemap_path)
        self.spawn_points = spawn_points

    def update(self):
        pass  # sau này có thể thêm logic enemy, camera, events...

    def draw(self, surface):
        self.tilemap.draw_map(surface)

    def get_tiles(self):
        return self.tilemap.tiles

class LevelManager:
    def __init__(self, level_list, player):
        """level list is a list: tuple(level_path, {'spawnpoint_name': (x,y) })"""
        self.level_list = level_list
        self.level_index = 0
        self.player = player
        self.need_refresh=False
        self.load_level(0, spawnpoint_name='start')  # spawn mặc định

    def load_level(self, lvindex, spawnpoint_name):
        """load the level number 'lvindex' in level data and place player to spawnpoint [spawnpoint_name]"""
        #lấy cặp dữ liệu của tuple với path: str, spawnpoints: dict {name: (x,y)}
        path, spawn_points = self.level_list[lvindex]
        self.level = Level(path, spawn_points,2)
        self.level_index = lvindex
        self.set_player(spawnpoint_name)
        
    def set_player(self,spawnpoint_name):
        spawn_pos=self.level.spawn_points.get(spawnpoint_name) #là vector2
        if spawn_pos:
            self.player.rect.topleft=spawn_pos
            self.player.velocity=pygame.Vector2(0,0)
        else:
            pass
            #raise ValueError(f"Spawn point '{spawnpoint_name}' not found in level {lvindex}")
    def go_to_level(self, lvindex, spawnpoint_name):
        self.load_level(lvindex, spawnpoint_name)
    def change_level (self, lvindex, spawnpoint_name):
        
        if self.player.rect.colliderect(gate.rect):
            self.need_refresh=True
        if self.need_refresh:
            self.go_to_level(lvindex, spawnpoint_name)
            self.need_refresh=False

