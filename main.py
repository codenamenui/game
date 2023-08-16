import pygame

# Initializing Pygame
pygame.init()

# Initializing Pygame Essential Variable
S_WIDTH, S_HEIGHT = 700, 700
screen = pygame.display.set_mode((S_WIDTH, S_HEIGHT))
clock = pygame.time.Clock()
FPS = 60

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
