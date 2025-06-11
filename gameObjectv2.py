import pygame
from pygame import Vector2
from ground_collision import in_collision_x
GRAY=(200, 200, 200)
BROWN=(139,93,0)
RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,0,255)
WHITE=(255,255,255)

class GameObject (pygame.sprite.Sprite):
    """create an root rectangular object that has a object type, the object type can be choose from this list: enemy, hazard, deadzone"""
    
    def __init__(self, x, y, width, height, obj_type, color):
        super().__init__()
        self.rect=pygame.Rect(x, y, width, height)
        self.type=obj_type
        self.color=color
        
    def draw (self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

class enemy (GameObject):
    
    def __init__(self,x,y,width=20,height=20):
        super().__init__(x, y, width, height, "enemy", RED)
        self.gravity=0
        self.velocity=Vector2(0,0)
        self.movespeed=150
        self.direction = 1
        
    

    def in_moving(self, player, d_time, tiles, view_range=500):

        if abs(self.rect.x - player.rect.x) < view_range: #neu nam trong pham vi nhin
            # di theo player
            if self.rect.x < player.rect.centerx:
                self.velocity.x = self.movespeed
                self.direction = 1
            elif self.rect.x > player.rect.centerx:
                self.velocity.x = -self.movespeed
                self.direction = -1
        else:
            # di tu nhien
            self.velocity.x = self.movespeed * self.direction

        # update vi tri
        prev_x = self.rect.x
        self.rect.x += int(self.velocity.x * d_time)

        # kt va cham va dao huong di chuyen
        in_collision_x(self,tiles)
        if self.rect.x == prev_x:  # neu cham tile
            self.direction *= -1  # di nguoc lai
            self.velocity.x = self.movespeed * self.direction



class hazard (GameObject):

    def __init__(self, x, y, width=100, height=40):
        super().__init__(x, y, width, height, "hazard", (0,0,255,100))

class entrance (GameObject):
    def __init__(self, x, y, index,width= 20, height=200):
        super().__init__(x,y,width,height,"entrance",WHITE)
        self.index=index