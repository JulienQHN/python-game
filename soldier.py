from re import A
import pygame
import os

class Soldier(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed, ammo, bullet_img):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.ammo = ammo
        self.start_ammo = ammo
        self.shoot_cooldown = 0
        self.health = 5
        self.max_health = self.health
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        pygame.font.init()            
        myfont = pygame.font.SysFont('Comic Sans MS', 30)
        textsurface = myfont.render(str(self.health), False, (0, 0, 0))
        
        #load all images for the players
        animation_types = ['Death','Idle', 'Run']
        for animation in animation_types:
            #reset temporary list of images
            temp_list = []
            #count number of files in the folder
            num_of_frames = len(os.listdir(f'Sprite/png/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(f'Sprite/png/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(150), int(150)))
                temp_list.append(img)
                
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.update_animation()
        self.check_alive()
        #update cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
    
    def life(self):
         myfont = pygame.font.SysFont('Comic Sans MS', 30)
         myfont.render( str(self.health) +'/5', False, (0, 0, 0))
         
         return myfont
        
    def move(self, moving_left, moving_right, GRAVITY):
        dx = 0
        dy = 0

        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1

        #saut
        if self.jump == True and self.in_air == False:
            self.vel_y = -18
            self.jump = False
            self.in_air = True

        #gravité
        self.vel_y += GRAVITY
        if self.vel_y > 8:
            self.vel_y
        dy += self.vel_y

        #check collision with floor
        if self.rect.bottom + dy > 750:
            dy = 750 - self.rect.bottom
            self.in_air = False

        #update rectangle position
        self.rect.x += dx
        self.rect.y += dy

    def moveEnemy(self, moving_left_enemy, moving_right_enemy, GRAVITY):
            #reset movement variables
            dx = 0
            dy = 0
        
            if moving_left_enemy:
                dx = -self.speed
                self.flip = True
                self.direction = -1
            if moving_right_enemy:
                dx = self.speed
                self.flip = False
                self.direction = 1

            #jump
            if self.jump == True and self.in_air == False:
                self.vel_y = -18
                self.jump = False
                self.in_air = True

            #apply gravity
            self.vel_y += GRAVITY
            if self.vel_y > 8:
                self.vel_y
            dy += self.vel_y

            #check collision with floor
            if self.rect.bottom + dy > 750:
                dy = 750 - self.rect.bottom
                self.in_air = False

            #update rectangle position
            self.rect.x += dx
            self.rect.y += dy

    def shoot(self, bullet_group, bullet_img):
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 20
            bullet = Bullet(self.rect.centerx + (0.6 * self.rect.size[0] * self.direction), self.rect.centery, self.direction, bullet_img)
            bullet_group.add(bullet)
            #reduce ammo
            self.ammo -= 1

    def update_animation(self):
        #update animation
        ANIMATION_COOLDOWN = 100
        #update image depending on current frame
        if self.action < len(self.animation_list) and self.frame_index < len(self.animation_list[self.action]):
            self.image = self.animation_list[self.action][self.frame_index]
        
        #check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        #if the animation has run out the reset back to the start
        if self.action < len(self.animation_list):
            
            if self.frame_index >= len(self.animation_list[self.action]):
                if self.action == 3:
                    self.frame_index = len(self.animation_list[self.action]) - 1
                else:
                    self.frame_index = 0


    def update_action(self, new_action):
        #check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            #update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
            
    
    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(3)
            

    def draw(self, screen):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
     
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, bullet_img):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self, SCREEN_WIDTH, player, bullet_group, enemy):
        
        #move bullet
        self.rect.x += (self.direction * self.speed)
        #check if bullet has gone off screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()

        #check collision with characters
        if pygame.sprite.spritecollide(player, bullet_group, False):
            if player.alive:
                player.health -= 1
                self.kill()
                
        if pygame.sprite.spritecollide(enemy, bullet_group, False):
            if enemy.alive:
                enemy.health -= 1
                self.kill()
            
         
                
         
