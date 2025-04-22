import pygame
from playerv2 import player
from setting import WIDTH, HEIGHT
from gameObjectv2 import enemy, hazard
from tile_map import TileMap
#ĐỊNH NGHĨA CÁC MÀU CẦN DÙNG
GRAY=(200, 200, 200)
BROWN=(139,93,0)
RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,0,255)
WHITE=(255,255,255)
BGCOLOR=(25,40,30)

CLOCK=pygame.time.Clock()
FPS=100


"""KHỞI TẠO CÁC BIẾN ĐẦU TIÊN"""

p1=player(WIDTH//2, HEIGHT-400)


enemies=[
    enemy(200, 500),
    enemy(850, 800)
    ]
hazards=[
    hazard(700,500)
    ]

"""KHỞI TẠO ĐẦU TIÊN"""
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GÊm sỐ 1")

map=TileMap("assets/tilemap/testmap.csv")

"""VÒNG LẶP GAME"""

running = True
while running:
    d_time=min(CLOCK.tick(FPS)/1000*FPS,2)
    #print(d_time) #SHOW DELTA TIME TO DEBUG
    screen.fill(BGCOLOR)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    map.draw_map(screen)
    for e in enemies:
        e.draw(screen)
        e.in_moving(p1)
    for h in hazards:
        h.draw(screen)

    #p1.in_move(map.tiles,d_time)
    p1.update_moving(map.tiles, d_time)
    p1.update_hit(enemies, hazards)
    p1.draw(screen)
    
    
    #pygame.draw.rect(screen, BLUE, p1.rect) #SHOW HITBOX
    fps = CLOCK.get_fps()
    #print(f"FPS: {fps:.2f}") #SHOW FPS
    pygame.display.update() #update màn hình
    
pygame.quit()