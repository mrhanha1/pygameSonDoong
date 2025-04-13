import pygame
from playerv2 import player
from setting import WIDTH, HEIGHT
from gameObjectv2 import groundOBJ, enemy, hazard
from tile_map import *
from spritesheet import Spritesheet
#ĐỊNH NGHĨA CÁC MÀU CẦN DÙNG
GRAY=(200, 200, 200)
BROWN=(139,93,0)
RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,0,255)
WHITE=(255,255,255)


CLOCK=pygame.time.Clock()
FPS=100


"""KHỞI TẠO CÁC BIẾN ĐẦU TIÊN"""
p1=player(WIDTH//2, HEIGHT-300)
gameGrounds=[
    groundOBJ(200, 800, 100, 200),
    groundOBJ(500, 600, 100, 200),
    groundOBJ(1100, 600, 100, 200),
    groundOBJ(0, 900, 1920, 500)
]
enemies=[
    enemy(200, 500),
    enemy(850, 800)
    ]
hazards=[
    hazard(700,500)
    ]
spritesheet=Spritesheet("spritesheet.png")
map=TileMap("assets/tilemap/testmap.csv", spritesheet)

"""KHỞI TẠO ĐẦU TIÊN"""
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GÊm sỐ 1")


"""VÒNG LẶP GAME"""

running = True
while running:
    d_time=min(CLOCK.tick(100)/1000*FPS,2)
    #print(d_time) #SHOW DELTA TIME TO DEBUG
    screen.fill(GRAY)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for ground in gameGrounds:
        ground.draw(screen)
    for e in enemies:
        e.draw(screen)
        e.in_moving(p1)
    for h in hazards:
        h.draw(screen)
    
    p1.in_move(gameGrounds,enemies, hazards,d_time)
    p1.in_update_hit(enemies, hazards, d_time)
    p1.draw(screen)
    #pygame.draw.rect(screen, BLUE, p1.rect) #SHOW HITBOX
    fps = CLOCK.get_fps()
    #print(f"FPS: {fps:.2f}") #SHOW FPS
    pygame.display.update() #update màn hình
    
pygame.quit()