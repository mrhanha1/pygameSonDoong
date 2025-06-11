import pygame
from playerv2 import player
from setting import *
from gameObjectv2 import entrance
from tile_map import TileMap
from level import LevelManager
from vfx import VFXManager

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
CHANGE_LV_EVT=pygame.USEREVENT+1

p1=player(0,0)
level_list_data= [
    ("assets/tilemap/lv0.csv",
     {1: (40,HEIGHT-100),
      3: (40,HEIGHT-100),
      2: (WIDTH-80,HEIGHT//2+100),
      4: (WIDTH-80,HEIGHT//2+100)}),
    ("assets/tilemap/lv1.csv",
     {1: (40,HEIGHT//2),
      3: (40,HEIGHT//2),
      2: (WIDTH-40,HEIGHT//2),
      4: (WIDTH-40,HEIGHT//2)}),
    ("assets/tilemap/lv2.csv",
     {1: (40,HEIGHT//2),
      3: (40,HEIGHT//2),
      2: (WIDTH-80,100),
      4: (WIDTH-80,HEIGHT-250)}),
    ("assets/tilemap/lv3.csv",
     {1: (40,HEIGHT//2-100),
      3: (40,HEIGHT//2+150),
      2: (WIDTH-80,HEIGHT//2-100),
      4: (WIDTH-80,HEIGHT-100)}),
    ("assets/tilemap/lv4.csv",
     {1: (50,HEIGHT//2-120),
      3: (60,HEIGHT-160),
      2: (WIDTH-80,HEIGHT//2-100),
      4: (WIDTH-80,HEIGHT-100)}),
    ("assets/tilemap/lv5.csv",
     {1: (50,HEIGHT//2-200),
      3: (40,HEIGHT-200),
      2: (WIDTH-80,150),
      4: (WIDTH-80,HEIGHT-100)}),
    ("assets/tilemap/lv6.csv",
     {1: (50,HEIGHT//2-200),
      3: (40,HEIGHT-250),
      2: (WIDTH-80,HEIGHT//2-100),
      4: (WIDTH-80,HEIGHT//2+150)}),
    ("assets/tilemap/lv7.csv",
     {1: (40,HEIGHT//2-250),
      3: (40,HEIGHT//2+150),
      2: (WIDTH-80,60),
      4: (WIDTH-80,60)}),
    ("assets/tilemap/lv8.csv",
     {1: (40,HEIGHT-200),
      3: (40,HEIGHT-200),
      2: (WIDTH-80,100),
      4: (WIDTH-80,100)}),
    ("assets/tilemap/lv9.csv",
     {1: (40,HEIGHT-200),
      3: (40,HEIGHT-200),}),
    ]
levelmanager=LevelManager(level_list_data, p1)
levelmanager.load_level(1, 2)

entrances=pygame.sprite.Group()
entrances.add(
    entrance(-40, 0, 1, 50, HEIGHT//2),
    entrance(-40, HEIGHT//2, 3, 50, HEIGHT//2),
    entrance(WIDTH-10, 0, 2,60,HEIGHT//2),
    entrance(WIDTH-10, HEIGHT//2, 4,60,HEIGHT//2)
    )

vfxmanager=VFXManager()

"""KHỞI TẠO GAME"""
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GÊm sỐ 1")

font = pygame.font.SysFont(None, 48)
paused=False
def draw_pause_menu():
    text = font.render("Paused - Press R to Resume", True, (255, 255, 255))
    screen.blit(text, (200, 250))
def draw_level_text(screen: pygame.Surface, level_index: int, font: pygame.font.Font):
    """Vẽ tên level hiện tại lên góc trên trái màn hình."""
    text_surface = font.render(f"Debug print Level {level_index}", True, (255, 255, 255))  # chữ trắng
    screen.blit(text_surface, (10, 10))  # vẽ tại góc trái trên màn hình
"""VÒNG LẶP GAME"""

running = True
while running:

    d_time=d_time = CLOCK.tick(FPS)/1000
    #print(d_time) #SHOW DELTA TIME TO DEBUG
    screen.fill(BGCOLOR)
    for event in pygame.event.get():
            # Nhấn ESC để pause
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
               paused = True
            if event.key == pygame.K_r:# Resume khi nhấn R
               paused = False
        elif event.type == CHANGE_LV_EVT:
            levelmanager.go_to_level(event.index)
        if event.type== CHANGE_VFX:
            levelmanager.level.tilemap
        if event.type == pygame.QUIT:
            running = False


    p1.draw(screen)
    vfxmanager.update(d_time,levelmanager.level_index)
    vfxmanager.draw(levelmanager.level_index, screen)
    levelmanager.level.draw(screen)
    for en in entrances:
        pass#en.draw(screen)

    if paused:
        draw_pause_menu()
    else:
        p1.update_moving(levelmanager.level.get_tiles(), d_time)
        p1.update_hit(levelmanager.level.tilemap.game_objects, entrances)
        levelmanager.level.update(d_time, p1)

    draw_level_text(screen, levelmanager.level_index, font)
    
    #pygame.draw.rect(screen, WHITE, p1.rect) #SHOW HITBOX
    #fps = CLOCK.get_fps()
    #print(f"FPS: {fps:.2f}") #SHOW FPS
    pygame.display.update() #update màn hình
    
pygame.quit()