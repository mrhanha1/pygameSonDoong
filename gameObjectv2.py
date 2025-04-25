import pygame
from pygame import Vector2
GRAY=(200, 200, 200)
BROWN=(139,93,0)
RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,0,255)
WHITE=(255,255,255)

class game_object:
    """create an root rectangular object that has a object type, the object type can be choose from this list: enemy, hazard, deadzone"""
    
    def __init__(self, x, y, width, height, obj_type, color):
        self.rect=pygame.Rect(x, y, width, height)
        self.type=obj_type
        self.color=color
        
    def draw (self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

class enemy (game_object):
    
    def __init__(self,x,y,width=20,height=20):
        super().__init__(x, y, width, height, "enemy", RED)
        self.gravity=0
        self.velocity=Vector2(0,0)
        self.movespeed=2
        
    def in_moving(self,player,view_range=500):
        self.velocity.x=0
        if abs(self.rect.x-player.rect.x)<view_range:
            #print("quai vat nhin thay ban")
            if self.rect.x<player.rect.centerx:
                self.velocity.x=self.movespeed
            elif self.rect.x>player.rect.centerx:
                self.velocity.x=-self.movespeed
        self.velocity.y+=self.gravity
        self.rect.x+=self.velocity.x
        self.rect.y+=self.velocity.y

class hazard (game_object):

    def __init__(self, x, y, width=100, height=40):
        super().__init__(x, y, width, height, "hazard", BLUE)

class entrance (game_object):
    def __init__(self, x, y, index,width= 40, height=200):
        super().__init__(x,y,width,height,"entrance",WHITE)
        self.index=index