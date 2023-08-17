import pygame
import sys
from Class import *

# Initializing Pygame
pygame.init()

# Initializing Pygame Essential Variable
S_WIDTH, S_HEIGHT = 700, 700
screen = pygame.display.set_mode((S_WIDTH, S_HEIGHT))
clock = pygame.time.Clock()
FPS = 60
    
# Player Sprite
player_sprite_sheet = pygame.image.load("assets/sprites/characters/player.png")
playerSurf = pygame.Surface((18, 24), pygame.SRCALPHA)
playerSurf.set_colorkey((255,0,255))
playerSurf.blit(player_sprite_sheet, (0, 0), (16, 20 + 48 * 0, 18, 24))

# Colors
empty = pygame.Color(0, 0, 0, 0)

# Counters
x_running_counter = 0
y_running_counter = 0
idle_counter = 0

# Speed of Char
speed = 5

# Flip
right = False
left = False
up = False
down = True

# Pos
x, y = S_WIDTH//2 - 9, S_HEIGHT//2 - 12

# Player
player = Player('Yooo')

while True:
    # 
    screen.fill('gray')

    # Keys
    keys = pygame.key.get_pressed()

    # Drawing Player
    screen.blit(playerSurf, (x, y))
    # player.display(screen, S_WIDTH, S_HEIGHT)
    
    # Counters
    if keys[pygame.K_d] or keys[pygame.K_a]:
        idle = False
        if x_running_counter == 59:
            x_running_counter = 0
        x_running_counter += 1
    else: 
        idle = True

    if keys[pygame.K_w] or keys[pygame.K_s]:
        idle = False
        if y_running_counter == 59:
            y_running_counter = 0
        y_running_counter += 1
    else: 
        idle = True

    if idle:
        if idle_counter == 59:
            idle_counter = 0
        idle_counter += 1

    # Player Movement
    if keys[pygame.K_a] and keys[pygame.K_d]:
        idle = True
    elif x > speed and keys[pygame.K_a]:
        x -= speed
        left = True
        right = False
        up = False
        down = False
    elif x <= S_WIDTH - 18 and keys[pygame.K_d]:
        x += speed
        right = True
        left = False
        up = False
        down = False

    if keys[pygame.K_s] and keys[pygame.K_w]:
        idle = True
    elif y > speed and keys[pygame.K_s]:
        y += speed
        down = True
        up = False
        left = False
        right = False
    elif y <= S_HEIGHT - 24 and keys[pygame.K_w]:
        y -= speed
        up = True
        down = False
        left = False
        right = False

    # Player Sprite
    playerSurf.fill(empty)
    if idle and up:
        playerSurf.blit(player_sprite_sheet, (0, 0), ((16 + (idle_counter//10) * 48), 20 + 48 * 2, 18, 24))
    elif idle and down:
        playerSurf.blit(player_sprite_sheet, (0, 0), ((16 + (idle_counter//10) * 48), 20 + 48 * 0, 18, 24))
    elif idle and right:
        playerSurf.blit(player_sprite_sheet, (0, 0), ((16 + (idle_counter//10) * 48), 20 + 48 * 1, 18, 24))
    elif idle and left:
        playerSurf.blit(player_sprite_sheet, (0, 0), ((16 + (idle_counter//10) * 48), 20 + 48 * 1, 18, 24))
        playerSurf = pygame.transform.flip(playerSurf, True, False)
    elif up:
        playerSurf.blit(player_sprite_sheet, (0, 0), ((16 + (y_running_counter//10) * 48), 20 + 48 * 5, 18, 24))
    elif down:
        playerSurf.blit(player_sprite_sheet, (0, 0), ((16 + (y_running_counter//10) * 48), 20 + 48 * 3, 18, 24))
    elif left:
        playerSurf.blit(player_sprite_sheet, (0, 0), ((16 + (x_running_counter//10) * 48), 20 + 48 * 4, 18, 24))
        playerSurf = pygame.transform.flip(playerSurf, True, False)
    elif right:
        playerSurf.blit(player_sprite_sheet, (0, 0), ((16 + (x_running_counter//10) * 48), 20 + 48 * 4, 18, 24))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    clock.tick(FPS)
    pygame.display.flip()