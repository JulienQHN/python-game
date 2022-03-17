import pygame
import pygame_menu
import os
from soldier import Soldier
from world_data import World
pygame.init()

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

def start_the_game():
    pygame.display.set_caption('Shooter')
    clock = pygame.time.Clock()
    FPS = 60
    GRAVITY = 0.75

    #define player action variables
    moving_left = False
    moving_right = False
    moving_left_enemy = False
    moving_right_enemy = False
    shoot = False
    shoot_enemy = False

    #load images
    #bullet
    bullet_img = pygame.image.load('Objects/Other/Skateboard3.png').convert_alpha()
    bg = pygame.image.load("Background/bg.jpg")
    tile_size = 50

    pygame.font.init()
    
    #create sprite groups
    bullet_group = pygame.sprite.Group()
    player = Soldier('player', 700, 700, 3, 5, 20, bullet_img)
    enemy = Soldier('enemy', 700, 700, 3, 5, 20, bullet_img)
    world = World(tile_size)

    run = True
    while run:
        clock.tick(FPS)
        screen.blit(bg, (0,0))
        player.update()
        player.draw(screen)
        enemy.update()
        enemy.draw(screen)
        world.draw(screen)

        #update and draw groups
        bullet_group.update(SCREEN_WIDTH, player, bullet_group, enemy)
        bullet_group.draw(screen)

        #update player actions
        if player.alive:
            #shoot bullets
            if shoot:
                player.shoot(bullet_group, bullet_img)
            animation_types = ['Death','Idle', 'Run']
            if player.in_air:
                player.update_action(1)#2: jump
            elif moving_left or moving_right:
                player.update_action(2)#1: run
            else:
                player.update_action(1)#0: idle
            player.move(moving_left, moving_right, GRAVITY)
        
        else:
            menu = pygame_menu.Menu('ENEMI A GAGNER', 400, 300,
                            theme=pygame_menu.themes.THEME_GREEN)
            menu.add.button('REJOUER LA PARTIE', start_the_game)
            menu.add.button('QUITER', pygame_menu.events.EXIT)
            menu.mainloop(screen)
        
        if enemy.alive:
            #shoot bullets
            if shoot_enemy:
                enemy.shoot(bullet_group, bullet_img)
            animation_types = ['Death','Idle', 'Run']
            if enemy.in_air:
                enemy.update_action(1)#2: jump
            elif moving_left_enemy or moving_right_enemy:
                enemy.update_action(2)#1: run
            else:
                enemy.update_action(1)#0: idle
            enemy.moveEnemy(moving_left_enemy, moving_right_enemy, GRAVITY)
        else:
            menu = pygame_menu.Menu('PLAYER A GAGNER', 400, 300,
                            theme=pygame_menu.themes.THEME_GREEN)
            menu.add.button('REJOUER LA PARTIE', start_the_game)
            menu.add.button('QUITER', pygame_menu.events.EXIT)
            menu.mainloop(screen)

        for event in pygame.event.get():
            #quit game
            if event.type == pygame.QUIT:
                run = False
            #keyboard presses
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    moving_left = True
                if event.key == pygame.K_d:
                    moving_right = True
                if event.key == pygame.K_LALT:
                    shoot = True
                if event.key == pygame.K_z and player.alive:
                    player.jump = True
                if event.key == pygame.K_ESCAPE:
                    run = False
                if event.key == pygame.K_k:
                    moving_left_enemy = True
                if event.key == pygame.K_m:
                    moving_right_enemy = True
                if event.key == pygame.K_RCTRL:
                    shoot_enemy = True
                if event.key == pygame.K_o and player.alive:
                    enemy.jump = True
                if event.key == pygame.K_ESCAPE:
                    run = False

            #keyboard button released
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_q:
                    moving_left = False
                if event.key == pygame.K_d:
                    moving_right = False
                if event.key == pygame.K_LALT:
                    shoot = False
                
                if event.key == pygame.K_k:
                        moving_left_enemy = False
                if event.key == pygame.K_m:
                    moving_right_enemy = False
                if event.key == pygame.K_RCTRL:
                    shoot_enemy = False
        pygame.font.init()
        myfont = pygame.font.SysFont('Comic Sans MS', 30)
        textsurface = myfont.render('5 points de vie chaqun tkt', False, (0, 0, 0))
        screen.blit(textsurface,(400,400))
        pygame.display.update()
menu = pygame_menu.Menu('LE MENU', 400, 300,
                        theme=pygame_menu.themes.THEME_GREEN)
menu.add.button('JOUER', start_the_game)
menu.add.button('QUITER', pygame_menu.events.EXIT)
menu.mainloop(screen)
pygame.quit()