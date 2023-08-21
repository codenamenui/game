import pygame
import sys
import os
import random
from Entities import *
from UI import *
from functions import path
import time

# Initializing Pygame
pygame.init()

# Initializing Pygame Essential Variable
S_WIDTH, S_HEIGHT = 700, 700
clock = pygame.time.Clock()
FPS = 60
screen = pygame.display.set_mode((S_WIDTH, S_HEIGHT))

# Objects
player = Player('Yooo', 13232320, [100000, 2, 1222, 1])
player.components['sprite'] = SpriteComponent(path("sprites/characters/player.png"),
                                              S_WIDTH//2 - 9, S_HEIGHT//2 - 12,
                                              18, 24, (48, 48), (16, 20))
player.components['movement'] = MovementComponent(5)
player.components['crit'] = CritComponent([10, 0.5, 0.5, 2])
player.components['encounter'] = EncounterComponent()

monster = Monster(2)

stats = StatWindow()

encounter_speed = 1
encounter_max = 100

frame = 'explore'
while True:

    while frame == 'explore':
        screen.fill('gray')
            
        mouse_pos = pygame.mouse.get_pos()

        # Keys
        keys = pygame.key.get_pressed()
        mouse_keys = pygame.mouse.get_pressed()

        # Drawing Player
        player.display_explore(keys, screen, S_WIDTH, S_HEIGHT)

        if player.components['encounter'].check(player):
            turn = TurnSystem(player.agility, monster.agility)
            frame = 'battle'
        player.components['encounter'].display_encounter(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    frame = 'stats'

        clock.tick(FPS)
        pygame.display.flip()

    while frame == 'stats':
        screen.fill('gray')
            
        mouse_pos = pygame.mouse.get_pos()

        stats.display(screen, player)

        # Keys
        keys = pygame.key.get_pressed()
        mouse_keys = pygame.mouse.get_pressed()

        if mouse_keys[0]:
            stats.press(mouse_pos, player)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    frame = 'explore'

        clock.tick(FPS)
        pygame.display.flip()


    while frame == 'battle': 
        screen.fill('gray')
        
        # Keys
        keys = pygame.key.get_pressed()
        mouse_keys = pygame.mouse.get_pressed()

        # Display Health Bars
        player.display_health(screen, S_WIDTH, S_HEIGHT, offset=100)
        monster.display_health(screen, S_WIDTH, S_HEIGHT, offset=600)

        monster.display_battle(screen, S_WIDTH, S_HEIGHT)
        player.display_battle(screen, S_WIDTH, S_HEIGHT)

        if turn.get_player():
            player.launch_atk(monster)
        if player.current_hp <= 0 or monster.current_hp <= 0:
            monster = Monster(2)
            player.current_hp = player.overall_hp
            frame = 'explore'
        if turn.get_enemy():
            monster.launch_atk(player)
        if player.current_hp <= 0 or monster.current_hp <= 0:
            monster = Monster(2)
            player.current_hp = player.overall_hp
            frame = 'explore'

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        clock.tick(FPS)
        pygame.display.flip()