import pygame, random, os
from functions import font

class Entities:
    def __init__(self, name, health, attack, agility, defense):
        self.name = name
        self.health = health
        self.current_health = health
        self.attack = attack
        self.agility = agility
        self.defense = defense

class SpriteComponent:
    def __init__(self, path, x, y, width, height, offset, initial):
        self.sprite_sheet = pygame.image.load(path)
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.playerSurf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.offset_x, self.offset_y = offset[0], offset[1]
        self.initial_x, self.initial_y = initial[0], initial[1]

    def display_sprite(self, screen, sprite_y, counter, flip):
        empty = pygame.Color(0, 0, 0, 0)
        self.playerSurf.fill(empty)
        self.playerSurf.blit(self.sprite_sheet, (0, 0), ((self.initial_x + (counter//10) * self.offset_x), 
                             self.initial_y + self.offset_y * sprite_y, self.width, self.height))
        if flip:
            self.playerSurf = pygame.transform.flip(self.playerSurf, True, False)
        screen.blit(self.playerSurf, (self.x, self.y))

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

    def counter(self, keys):
        if keys[pygame.K_d] or keys[pygame.K_a]:
            self.idle = False
            if self.x_running_counter == 59:
                self.x_running_counter = 0
            self.x_running_counter += 1
        elif keys[pygame.K_w] or keys[pygame.K_s]:
            self.idle = False
            if self.y_running_counter == 59:
                self.y_running_counter = 0
            self.y_running_counter += 1
        else: 
            self.idle = True
            if self.idle_counter == 59:
                self.idle_counter = 0
            self.idle_counter += 1

    def move(self, sprite, keys, S_WIDTH, S_HEIGHT):
        # Player Movement
        if keys[pygame.K_a] and keys[pygame.K_d]:
            self.idle = True
        elif keys[pygame.K_a]:
            sprite.x -= self.speed
            self.left = True
            self.right = False
            self.up = False
            self.down = False
        elif keys[pygame.K_d]:
            sprite.x += self.speed
            self.right = True
            self.left = False
            self.up = False
            self.down = False

        if keys[pygame.K_s] and keys[pygame.K_w]:
            self.idle = True
        elif keys[pygame.K_s]:
            sprite.y += self.speed
            self.down = True
            self.up = False
            self.left = False
            self.right = False
        elif keys[pygame.K_w]:
            sprite.y -= self.speed
            self.up = True
            self.down = False
            self.left = False
            self.right = False

        if sprite.x >= S_WIDTH - sprite.width:
            sprite.x = S_WIDTH - sprite.width
        elif sprite.x < 0:
            sprite.x = 0 

        if sprite.y >= S_HEIGHT - sprite.height:
            sprite.y = S_HEIGHT - sprite.height
        elif sprite.y < 0:
            sprite.y = 0

    def animation(self):
        if self.idle and self.up:
            sprite_y = 2
        elif self.idle and self.down:
            sprite_y = 0
        elif self.idle and self.right:
            sprite_y = 1
        elif self.idle and self.left:
            sprite_y = 1
        elif self.up:
            sprite_y = 5
        elif self.down:
            sprite_y = 3
        elif self.left:
            sprite_y = 4
        elif self.right:
            sprite_y = 4

        if self.idle:
            counter = self.idle_counter
        elif self.up or self.down:
            counter = self.y_running_counter
        elif self.right or self.left:
            counter = self.x_running_counter

        return (sprite_y, counter, self.left)

class EquipmentComponent:
    def __init__(self):
        pass

class ShopComponent:
    def __init__(self):
        pass

class Player(Entities):
    def __init__(self, 
                 name,
                 stats=[], 
                 add_stats=[]):

        self.components = {}

        if stats == []:
            Entities.__init__(self, name, 0, 0, 0, 0)
        else:
            Entities.__init__(self, name, *stats)

        if add_stats == []:
            self.luck = 0
            self.combo_rate = 1
            self.crit_rate = 1
            self.crit_dmg = 2
        else:
            self.luck = add_stats[0]
            self.combo_rate = add_stats[1]
            self.crit_rate = add_stats[2]
            self.crit_dmg = add_stats[3]

    def display(self, keys, screen, S_WIDTH, S_HEIGHT):
        self.components['movement'].counter(keys)
        self.components['movement'].move(self.components['sprite'], keys, S_WIDTH, S_HEIGHT)
        args = self.components['movement'].animation()
        self.components['sprite'].display_sprite(screen, *args)