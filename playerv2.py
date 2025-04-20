import pygame
#from setting import WIDTH, HEIGHT
from pygame.math import Vector2
from animations import Animator
def cd_is_over (last_time, duration):
    "return True if from last time to now is equal or longer than durration"
    return pygame.time.get_ticks() - last_time >= duration
class player:
    """create a player with default moving input method and animation |
    x and y is the topleft position of player when game start,
    the size of player depend on size of .png image on animation and scale factor"""
    
    def __init__(self, x, y, move_speed=8, scale_factor=3):
        
        self.frame_w = 31 #self.sprite_sheet.get_width() // self.num_frames
        self.frame_h = 31 #self.sprite_sheet.get_height()
        self.scale_factor=scale_factor
        self.rect=pygame.Rect(x, y, 15*scale_factor, 25*scale_factor)
        
        self.animation_speed=700
        self.animator=Animator({
            "idle": ("assets/images/idle.png", 2),
            "walk": ("assets/images/walk.png", 8),
            "jump": ("assets/images/jump.png", 4),
            "fall": ("assets/images/fall.png", 4),
            "dead": ("assets/images/dead.png", 8)}
            , scale_factor, self.animation_speed)
        
        #PlaYER moVEment VAriaAble
        self.move_speed=move_speed
        self.velocity=Vector2(0,0)
        self.gravity=0.35
        self.jump_force=-12
        self.isGrounded=False
        self.knockback_timer=0
        self.is_knock_back=False
        #self.hitstop_timer=0
        #self.hitstop=False

        self.isAlive=True
        self.hp=10
        self.last_hitted=pygame.time.get_ticks()

    def update_moving (self,grounds,d_time):
        self.velocity.x=0
        self.moving (grounds, d_time)
        #GRAVITY
        self.velocity.y += self.gravity*d_time
        self.update_knockback(d_time)
        """UPDATE MOVING AND COLLISION"""
        self.rect.x += int(self.velocity.x*d_time)
        self.in_collision_x(grounds)
        
        self.rect.y +=int(self.velocity.y*d_time)
        self.in_collision_y(grounds)
        """ANIMATION CONDITION AND UPDATE"""
        if self.isGrounded and self.velocity.x==0:
            self.animator.state="idle"
        elif self.velocity.y<0:
            self.animator.state="jump"
        elif self.velocity.y>0:
            self.animator.state='fall'
        #print(self.state)
        self.animator.play_animate(self.velocity.x)
    """MOVING AND GROUND COLLISION"""
    def moving (self, grounds,d_time):
        """this need to put in running loop game"""
        key_in=pygame.key.get_pressed()
        self.velocity.x=0
        #JUMPING
        if key_in[pygame.K_SPACE] and self.isGrounded:
            self.velocity.y = self.jump_force
            self.isGrounded = False
        #extra jump
        if key_in[pygame.K_k] and self.isGrounded:
            self.velocity.y=self.jump_force*2
            self.isGrounded=False
        #MOVING
        if key_in[pygame.K_LEFT]:
            self.velocity.x = -self.move_speed #sang trái
            self.state="walk"
            #print(self.move_speed)
        if key_in[pygame.K_RIGHT]:
            self.velocity.x = self.move_speed #sang phải
            self.state="walk"
            #print(self.move_speed)
        
    def check_collision(self,tiles):
        return [tile for tile in tiles if self.rect.colliderect(tile.rect)]
    def in_collision_x (self, tiles):
        colliders=self.check_collision(tiles)
        for obj in colliders:
            if self.rect.colliderect(obj.rect):
                if self.velocity.x>0:
                    self.rect.right=obj.rect.left
                elif self.velocity.x<0:
                    self.rect.left=obj.rect.right
                    self.velocity.x = 0 #DỪNG DI CHUYỂN
    def in_collision_y (self, tiles):
        colliders=self.check_collision(tiles)
        for obj in colliders:
            if self.rect.colliderect(obj.rect):
                if self.velocity.y<0:
                    self.rect.top = obj.rect.bottom
                    self.velocity.y=0
                    #pygame.time.delay(500)
                if self.velocity.y>0:
                    self.rect.bottom = obj.rect.top #ĐẶT NV LÊN NỀN
                    self.velocity.y = 0 #DỪNG DI CHUYỂN CHIỀU DỌC
                    self.isGrounded=True


    """OTHER GAME OBJECT COLLISION"""
    def update_knockback(self,d_time):
        if self.is_knock_back:
            """VÀO ĐÂY ĐỂ SET THỜI GIAN BỊ KNOCKBACK"""
            if self.knockback_timer<15:
                #pygame.time.wait(100) #hitstop time
                self.velocity.x-=self.move_speed*d_time*1.5
                #self.velocity.y=0
                self.velocity.y=-12*self.gravity*d_time
                self.knockback_timer+=d_time
            else:
                self.is_knock_back=False
                self.knockback_timer=0
    def in_check_hit (self, objects):
        """RETURN THE OBJECT TYPE.
        *this need to put in running loop game"""
        for obj in objects:
            if self.rect.colliderect(obj.rect):
                return obj.type  # trả về loại đối tượng bị va chạm
        return None  # k va chạm
    
    def update_hit(self, enemies, hazards,d_time): #xử lý va chạm
        """this need to put in running loop game"""

        collision_type = self.in_check_hit(enemies + hazards)
        if cd_is_over(self.last_hitted, 1000):
            if collision_type == "enemy":  # Chạm quái vật
                print("⚔️ Bị quái vật tấn công",pygame.time.get_ticks())
                self.is_knock_back=True
                #self.hitstop=True
                #self.hitstop_timer=0
                print (self.velocity.x)
                self.last_hitted=pygame.time.get_ticks()
                
            elif collision_type == "hazard":  # Chạm vật nguy hiểm (nước/gai)
                print("💀 Chết",pygame.time.get_ticks())
                self.state='dead'
                self.isAlive=False
                self.velocity.x = 0
                self.velocity.y = 0
                #self.last_hitted=pygame.time.get_ticks()

    def draw (self, screen):
        screen.blit(self.animator.get_avatar(),(self.rect.left-7*self.scale_factor,self.rect.top-6*self.scale_factor))