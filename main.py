import pygame
from playerv2 import player
from setting import *
from gameObjectv2 import enemy, hazard, entrance
from tile_map import TileMap
from level import LevelManager
from particle import ParticleSystem
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
      2: (WIDTH-60,HEIGHT//2),
      4: (WIDTH-60,HEIGHT//2)}),
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
     {1: (40,HEIGHT//2-100),
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

enemies=pygame.sprite.Group()
enemies.add(enemy(200, 500),
            enemy(850, 800))
hazards=pygame.sprite.Group()
hazards.add(hazard(700,500))

entrances=pygame.sprite.Group()
entrances.add(
    entrance(-20, 0, 1, 50, HEIGHT//2),
    entrance(-20, HEIGHT//2, 3, 50, HEIGHT//2),
    entrance(WIDTH-30, 0, 2,60,HEIGHT//2),
    entrance(WIDTH-30, HEIGHT//2, 4,60,HEIGHT//2)
    )



particle_system = ParticleSystem(pool_size=200)
polygon = [(1260, 0), (1680, 0), (1440, HEIGHT), (840, HEIGHT)]
particle_system.start_dust_effect(polygon)
particle_system.add_water_spawn(1, x=500, y=100)
particle_system.add_water_spawn(2, x=600, y=150)
sunlight=pygame.Surface((WIDTH,HEIGHT),pygame.SRCALPHA)



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
line=pygame.Rect(0,HEIGHT//2,WIDTH,10)
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
        if event.type == pygame.QUIT:
            running = False

    
    
    particle_system.update(d_time, dust_bounds=polygon)
    particle_system.draw(screen)
    
    
    levelmanager.level.draw(screen)
    for e in enemies:
        e.draw(screen)
        #e.in_moving(p1)
    for h in hazards:
        h.draw(screen)
    for en in entrances:
        en.draw(screen)
    pygame.draw.rect(screen,WHITE,line)
    p1.draw(screen)
    if paused:
        draw_pause_menu()
    else:
        p1.update_moving(levelmanager.level.get_tiles(), d_time)
        p1.update_hit(enemies, hazards, entrances)
    pygame.draw.polygon(sunlight, (255,255,180,40), polygon)
    screen.blit(sunlight, (0,0))
    
    
    draw_level_text(screen, levelmanager.level_index, font)
    
    #pygame.draw.rect(screen, WHITE, p1.rect) #SHOW HITBOX
    #fps = CLOCK.get_fps()
    #print(f"FPS: {fps:.2f}") #SHOW FPS
    pygame.display.update() #update màn hình
    
pygame.quit()