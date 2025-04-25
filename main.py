import pygame
from playerv2 import player
from setting import WIDTH, HEIGHT
from gameObjectv2 import enemy, hazard, entrance
from tile_map import TileMap
from level import LevelManager
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

p1=player(0,0,2,4)
map=TileMap("assets/tilemap/lv1_test.csv")
level_list_data= [
    ("assets/tilemap/lv1_test.csv",
     {"start": (800,900),
      "end1": (1900,400)}),
    ("testmap.csv",
     {"start": (800,800),
      "end1": (1900,400)})
    ]
levelmanager=LevelManager(level_list_data, p1)


enemies=pygame.sprite.Group()
enemies.add(enemy(200, 500),
            enemy(850, 800))
hazards=pygame.sprite.Group()
hazards.add(hazard(700,500))

entrances=pygame.sprite.Group()
entrances.add(
    entrance(-30, 0, 1,30,HEIGHT//2),
    entrance(-30, HEIGHT//2, 2,30,HEIGHT//2),
    entrance(WIDTH+30, 0, 3,30,HEIGHT//2),
    entrance(WIDTH+30, HEIGHT//2, 4,30,HEIGHT//2)
    )
"""KHỞI TẠO ĐẦU TIÊN"""
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GÊm sỐ 1")

font = pygame.font.SysFont(None, 48)
paused=False
def draw_pause_menu():
    text = font.render("Paused - Press R to Resume", True, (255, 255, 255))
    screen.blit(text, (200, 250))
"""VÒNG LẶP GAME"""

running = True
while running:

    d_time=min(CLOCK.tick(FPS)/1000*FPS,2)
    #print(d_time) #SHOW DELTA TIME TO DEBUG
    screen.fill(BGCOLOR)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            # Nhấn ESC để pause
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
               paused = True
            if event.key == pygame.K_r:# Resume khi nhấn R
               paused = False
    #map.draw_map(screen)
    
    levelmanager.level.draw(screen)
    for e in enemies:
        e.draw(screen)
        e.in_moving(p1)
    for h in hazards:
        h.draw(screen)

    
    p1.draw(screen)
    if paused:
        draw_pause_menu()
    else:
        p1.update_moving(levelmanager.level.get_tiles(), d_time)
        p1.update_hit(enemies, hazards, entrances)

    #pygame.draw.rect(screen, WHITE, p1.rect) #SHOW HITBOX
    fps = CLOCK.get_fps()
    #print(f"FPS: {fps:.2f}") #SHOW FPS
    pygame.display.update() #update màn hình
    
pygame.quit()