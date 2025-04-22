import pygame, csv, os

class Tile(pygame.sprite.Sprite):
    def __init__(self, path,x,y):
        super().__init__()
        self.image=pygame.image.load(path)
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        

    def draw(self,screen):
        screen.blit(self.image,(self.rect.x,self.rect.y))
    

class TileMap:
    def __init__(self, filepath):
        """create a tilemap with map in .csv file in filepath"""
        #tile grid=16 -> tile size =60
        #tile grid = 64 -> tile size = 15
        self.tile_size = 60
        self.start_x, self.start_y = 0, 0
        self.tiles = self.load_tiles(filepath)
        
        self.map_surface = pygame.Surface((self.map_w, self.map_h)) #cai nay phai chay sau load tiles
        self.map_surface.set_colorkey((0, 0, 0)) #key mau den của nền
        
        #self.load_map()

    def draw_map(self, surface):
        for tile in self.tiles:
            tile.draw(surface)

    def load_map(self):
        """this just need to load 1 time before game running"""
        for tile in self.tiles:
            tile.draw(self.map_surface)

    def read_csv(self, filepath):
        map = []
        with open(os.path.join(filepath)) as data:
            data = csv.reader(data, delimiter=',')
            for row in data:
                map.append(list(row))
        return map #2d list

    def load_tiles(self, filepath):
        tiles = []
        map_data = self.read_csv(filepath)
        x, y = 0, 0
        for row in map_data:
            x = 0
            for tile in row:
                if tile == '-1':
                    #nếu tile này không có gì để vẽ thì chỉ tăng x và y chọn đến tile tiếp theo
                    self.start_x, self.start_y = x * self.tile_size, y * self.tile_size 
                elif tile == '0':
                    tiles.append(Tile("assets/mossyblock.png", x * self.tile_size, y * self.tile_size))
                x += 1
            y += 1
        self.map_w = x * self.tile_size
        self.map_h = y * self.tile_size
        return tiles
