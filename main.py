import pygame
import sys
import os
import random
from Class import *
from functions import path

# Initializing Pygame
pygame.init()

# Initializing Pygame Essential Variable
S_WIDTH, S_HEIGHT = 700, 700
clock = pygame.time.Clock()
FPS = 60
screen = pygame.display.set_mode((S_WIDTH, S_HEIGHT))

# Player
player = Player('Yooo', [1, 2, 1, 1])
player.components['sprite'] = SpriteComponent(path("sprites/characters/player.png"),
                                              S_WIDTH//2 - 9, S_HEIGHT//2 - 12,
                                              18, 24, (48, 48), (16, 20))
player.components['movement']= MovementComponent(5)
player.components['crit'] = CritComponent([10, 0.5, 0.5, 2])

monster = Monster(2)

frame = 'explore'
while True:

    while frame == 'menu':
        screen.fill('gray')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        clock.tick(FPS)
        pygame.display.flip()

    while frame == 'explore':
        screen.fill('gray')
        
        # Keys
        keys = pygame.key.get_pressed()
        mouse_keys = pygame.mouse.get_pressed()

        player.display_health(screen, S_WIDTH, S_HEIGHT)
        monster.display_health(screen, S_WIDTH, S_HEIGHT, 600)

        # Drawing Player
        player.display(keys, screen, S_WIDTH, S_HEIGHT)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                player.launch_atk(monster)

        clock.tick(FPS)
        pygame.display.flip()

    while frame == 'battle':

        screen.fill('gray')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        clock.tick(FPS)
        pygame.display.flip()