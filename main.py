import pygame
import sys
import os
import random
from Class import Player, SpriteComponent, Entities, Monsters
from functions import path

# Initializing Pygame
pygame.init()

# Initializing Pygame Essential Variable
S_WIDTH, S_HEIGHT = 700, 700
clock = pygame.time.Clock()
FPS = 60
screen = pygame.display.set_mode((S_WIDTH, S_HEIGHT))

# Player
player = Player('Yooo', 5)
player.components['Sprite'] = SpriteComponent(path("sprites/characters/player.png"),
                                              S_WIDTH//2 - 9, S_HEIGHT//2 - 12,
                                              18, 24)

while True:

    screen.fill('gray')
    # Keys
    keys = pygame.key.get_pressed()

    # Drawing Player
    player.display(keys, screen, S_WIDTH, S_HEIGHT)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    clock.tick(FPS)
    pygame.display.flip()