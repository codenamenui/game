import pygame, random, os
from functions import font

class Entities:
    def __init__(self, name, health, attack, agility, defense):
        self.name = name
        self.health = health
        self.attack = attack
        self.agility = agility
        self.defense = defense
        self.current_health = health

class SpriteComponent:
    def __init__(self, path, x, y, width, height, offset, initial):
        self.sprite_sheet = pygame.image.load(path)
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.playerSurf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.offset_x, self.offset_y = offset[0], offset[1]
        self.initial_x, self.initial_y = initial[0], initial[1]

    def display_sprite(self, sprite_y, counter, flip):
        empty = pygame.Color(0, 0, 0, 0)
        self.playerSurf.fill(empty)
        self.playerSurf.blit(self.img, (0, 0), ((self.initial_x + (counter//10) * self.offset_x), 
                             self.initial_y + self.offset_y * sprite_y, self.width, self.height))
        if flip:
            self.playerSurf = pygame.transform.flip(self.playerSurf, True, False)
        screen.blit(pygame.transform.scale_by(self.playerSurf), (self.x, self.y))

class CollisionComponent:
    def __init__(self):
        pass

class CritComponent:
    def __init__(self):
        pass

class MovementComponent:
    def __init__(self, speed):
        self.speed = speed
        self.x_running_counter = 0
        self.y_running_counter = 0
        self.idle_counter = 0
        self.idle = True
        self.down = True
        self.up = False
        self.left = False
        self.right = False

    def move(self, SpriteComponent, keys, speed, S_WIDTH, S_HEIGHT):

        if keys[pygame.K_d] or keys[pygame.K_a]:
            self.idle = False
            if self.x_running_counter == 59:
                self.x_running_counter = 0
            self.x_running_counter += 1
        else: 
            self.idle = True

        if keys[pygame.K_w] or keys[pygame.K_s]:
            self.idle = False
            if self.y_running_counter == 59:
                self.y_running_counter = 0
            self.y_running_counter += 1
        else: 
            self.idle = True

        if self.idle:
            if self.idle_counter == 59:
                self.idle_counter = 0
            self.idle_counter += 1

        # Player Movement
        if keys[pygame.K_a] and keys[pygame.K_d]:
            self.idle = True
        elif keys[pygame.K_a]:
            self.x -= speed
            self.left = True
            self.right = False
            self.up = False
            self.down = False
        elif keys[pygame.K_d]:
            self.x += speed
            self.right = True
            self.left = False
            self.up = False
            self.down = False

        if keys[pygame.K_s] and keys[pygame.K_w]:
            self.idle = True
        elif keys[pygame.K_s]:
            self.y += speed
            self.down = True
            self.up = False
            self.left = False
            self.right = False
        elif keys[pygame.K_w]:
            self.y -= speed
            self.up = True
            self.down = False
            self.left = False
            self.right = False

        if self.x >= S_WIDTH - self.width:
            self.x = S_WIDTH - self.width
        elif self.x < 0:
            self.x = 0 

        if self.y >= S_HEIGHT - self.height:
            self.y = S_HEIGHT - self.height
        elif self.y < 0:
            self.y = 0



class EquipmentComponent:
    def __init__(self):
        pass

class ShopComponent:
    def __init__(self):
        pass

