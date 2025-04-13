import pygame, csv, os

class Tile(pygame.sprite.Sprite):
    def __init__(self, image,x,y,spritesheet):
        super().__init__(self)
        self.image=spritesheet.parse_sprite(image)
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        
    def draw(self,screen):
        screen.blit(self.image,(self.rect.x,self.rect.y))


class TileMap():
    def __init__(self,filename,spritesheet):
        self.tile_size=16
        self.start_x,self.start_y=0,0
        self.spritesheet=spritesheet
        self.tiles=self.load_tiles(filename)
        self.map_surface=pygame.Surface((self.map_w,self.map_h))
        self.map_surface.set_colorkey((0,0,0))
        self.load_map()
        
    def draw_map(self, surface):
        surface.blit(self.map_surface,(0,0))
        
    def load_map(self):
        for tile in self.tiles:
            tile.draw(self.map_surface)
        
    def read_csv(self,filename):
        map=[]
        with open(os.path.join(filename)) as data:
            data=csv.reader(data, delimiter=',')
            for row in data:
                map.append(list(row))
        return map

    def load_tiles(self,filename):
        tiles=[]
        map=self.read_csv(filename)
        x,y=0,0
        for row in map:
            x=0
            for tile in row:
                if tile=='1':
                    self.start_x, self.start_y = x*self.tile_size, y*self.tile_size
                elif tile=='0':
                    tiles.append(Tile("assets/mossyblock.png", x*self.tile_size, y*self.tile_size, self.spritesheet))
                x+=1#cot tiep theo
            y+=1 #hang tiep theo
        self.map_w=x*self.tile_size
        self.map_h=y*self.tile_size
        return tiles