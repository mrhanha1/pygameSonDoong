import pygame
class Spritesheet:
    def __init__(self,filename):
        self.filename=filename
        self.spritesheet=pygame.image.load(filename).convert()
    def get_sprite(self,x,y,w,h):
        sprite=pygame.Surface((w,h))