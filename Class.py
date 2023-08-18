import pygame, random, os
from functions import font

"""
Notes

- LVL = 5 stat points
"""

class Entities:
    def __init__(self, name, health, attack, agility, defense):
        self.name = name
        self.health = health
        self.attack = attack
        self.agility = agility
        self.defense = defense
        self.current_health = health

    def display_health(self, screen, S_WIDTH, S_HEIGHT, offset = 100):
        rect = pygame.Rect(0, 0, 500, 40)
        rect.center = (S_WIDTH//2, S_HEIGHT - offset)
        pygame.draw.rect(screen, 'purple', rect)
        pygame.draw.rect(screen, 'black', rect, 1)
        health_text = font(30).render(f'{self.current_health}/{self.health}', True, 'black')
        screen.blit(health_text, health_text.get_rect(center=(rect.center[0], rect.center[1] - 2)))

class SpriteComponent:
    def __init__(self, path, x, y, width, height):
        self.img = pygame.image.load(path)
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.x_running_counter = 0
        self.y_running_counter = 0
        self.idle_counter = 0
        self.playerSurf = pygame.Surface((width, height), pygame.SRCALPHA)
        self.idle = True
        self.down = True
        self.up = False
        self.left = False
        self.right = False

    def display_sprite(self, screen):
        empty = pygame.Color(0, 0, 0, 0)
        self.playerSurf.fill(empty)
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

        self.playerSurf.blit(self.img, (0, 0), ((16 + (counter//10) * 48), 20 + 48 * sprite_y, self.width, self.height))
        if self.left:
            self.playerSurf = pygame.transform.flip(self.playerSurf, True, False)
        # screen.blit(self.playerSurf, (self.x, self.y))
        screen.blit(pygame.transform.scale_by(self.playerSurf, 1.5), (self.x, self.y))

    def move(self, keys, speed, S_WIDTH, S_HEIGHT):

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

class Monsters(Entities):

    # Scaling = (health, attack, agility, defense)
    monster_types = {
        1 : ((3, 0.5, 1, 2), (1, 10), 'Slime'),
        2 : ((2, 1.5, 1, 2), (10, 20), 'Goblin')
    }

    def __init__(self, m_type):
        self.lvl = random.randint(*(self.monster_types[m_type][1]))
        stat_points = (self.lvl) * 4
        scaling = self.monster_types[m_type][0]
        scaling_overall = sum(scaling)
        health = int(round(stat_points * scaling[0] / scaling_overall, 0))
        attack = int(round(stat_points * scaling[1] / scaling_overall, 0))
        agility = int(round(stat_points * scaling[2] / scaling_overall, 0))
        defense = int(round(stat_points * scaling[3] / scaling_overall, 0))
        super().__init__(self.monster_types[m_type][2], health, attack, agility, defense)

    def __str__(self):
        return f'''MONSTER : {self.name}
        LVL : {self.lvl}
        HEALTH : {self.health}
        ATTACK : {self.attack}
        AGILITY : {self.agility}
        DEFENSE : {self.defense}
        REAL STAT : {self.lvl * 4}
        ACTUAL STAT : {sum([self.health, self.attack, self.agility, self.defense])}
        '''

class Player(Entities, SpriteComponent):
    def __init__(self, 
                 name,
                 speed,
                 stats=[], 
                 add_stats=[]):

        self.speed = speed
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
        self.display_health(screen, S_WIDTH, S_HEIGHT)
        directions = self.components['Sprite'].move(keys, self.speed, S_WIDTH, S_HEIGHT)
        self.components['Sprite'].display_sprite(screen)