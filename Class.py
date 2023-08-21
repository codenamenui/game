import pygame, random, os
from functions import *

class Entities:
    def __init__(self, name, health, attack, agility, defense):
        self.name = name
        self.health = health
        self.current_hp = health * 10
        self.overall_hp = health * 10
        self.attack = attack
        self.agility = agility
        self.defense = defense

    def launch_atk(self, enemy):
        if 'crit' in self.components:
            dmg = 0
            combo = True
            while combo:
                if random.random() < self.components['crit'].combo_rate:
                    combo = False
                if random.random() < self.components['crit'].crit_rate:
                    dmg += int(self.attack * (400 / (400 + self.defense))) * self.components['crit'].crit_dmg
                else: 
                    dmg += int(self.attack * (400 / (400 + self.defense))) * self.components['crit'].crit_dmg
            enemy.current_hp -= dmg
        else:
            enemy.current_hp -= int(self.attack * (400 / (400 + self.defense + 100)))

    def display_health(self, screen, S_WIDTH, S_HEIGHT, offset = 100):
        rect = pygame.Rect(0, 0, (500 * (self.current_hp/self.overall_hp)), 40)
        outline_rect = pygame.Rect(0, 0, 500, 40)
        rect.midleft = (100, S_HEIGHT - offset)
        outline_rect.center = (S_WIDTH//2, S_HEIGHT - offset)
        pygame.draw.rect(screen, 'purple', rect)
        pygame.draw.rect(screen, 'black', outline_rect, 1)
        health_text = font(30).render(f'{self.current_hp}/{self.overall_hp}', True, 'black')
        screen.blit(health_text, health_text.get_rect(center=(outline_rect.center)))

class SpriteComponent:
    def __init__(self, path, x, y, width, height, offset, initial):
        self.sprite_sheet = pygame.image.load(path)
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.charSurf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        # self.charSurf = pygame.Surface((self.width, self.height))
        self.offset_x, self.offset_y = offset[0], offset[1]
        self.initial_x, self.initial_y = initial[0], initial[1]

    def display_sprite(self, screen, sprite_y, counter, flip):
        empty = pygame.Color(0, 0, 0, 0)
        self.charSurf.fill(empty)
        self.charSurf.blit(self.sprite_sheet, (0, 0), ((self.initial_x + (counter//10) * self.offset_x), 
                             self.initial_y + self.offset_y * sprite_y, self.width, self.height))
        if flip:
            self.charSurf = pygame.transform.flip(self.charSurf, True, False)
        screen.blit(self.charSurf, (self.x, self.y))

    def battle_sprite(self, screen, sprite_y, counter, x, y):
        empty = pygame.Color(0, 0, 0, 0)
        self.charSurf.fill(empty)
        self.charSurf.blit(self.sprite_sheet, (0, 0), ((self.initial_x + (counter//10) * self.offset_x), 
                           self.initial_y + self.offset_y * sprite_y, self.width, self.height))
        screen.blit(self.charSurf, (x, y))

class CollisionComponent:
    def __init__(self):
        pas

class CritComponent:
    def __init__(self, add_stats=[]):
        if add_stats == []:
            self.luck = 0
            self.combo_rate = 0.01
            self.crit_rate = 0.01
            self.crit_dmg = 1.5
        else:
            self.luck = add_stats[0]
            self.combo_rate = add_stats[1]
            self.crit_rate = add_stats[2]
            self.crit_dmg = add_stats[3]

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

    def set_default(self):
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

class EncounterComponent:
    def __init__(self):
        self.encounter_speed = 2
        self.encounter_max = 100
        self.gauge = 0

    def check(self, player):
        if not player.components['movement'].idle:
            self.gauge += self.encounter_speed
            if self.gauge >= self.encounter_max:
                player.components['movement'].set_default()
                self.gauge = 0
                return True
        return False

    def display_encounter(self, screen):
        pygame.draw.rect(screen, 'orange', (50, 600, (self.gauge/self.encounter_max * 600), 50))
        pygame.draw.rect(screen, 'black', (50, 600, 600, 50), 1)

class Player(Entities):
    def __init__(self, 
                 name,
                 stats=[]):

        self.components = {}
        self.turn = True
        # self.lvl = lvl
        # self.exp = exp

        if stats == []:
            Entities.__init__(self, name, 0, 0, 0, 0)
        else:
            Entities.__init__(self, name, *stats)

    def display_explore(self, keys, screen, S_WIDTH, S_HEIGHT):
        self.components['movement'].counter(keys)
        self.components['movement'].move(self.components['sprite'], keys, S_WIDTH, S_HEIGHT)
        args = self.components['movement'].animation()
        self.components['sprite'].display_sprite(screen, *args)

    def display_battle(self, screen, S_WIDTH, S_HEIGHT):
        self.components['movement'].counter({pygame.K_a : False, pygame.K_d : False,
                                             pygame.K_s : False, pygame.K_w : False})
        args = self.components['movement'].animation()
        self.components['sprite'].battle_sprite(screen, args[0], args[1], S_WIDTH//2, S_HEIGHT - 200)

class Monster(Entities):

    # Scaling = (health, attack, agility, defense)
    monster_types = {
        1 : ((3, 0.5, 1, 2), (1, 10), 'Slime', SpriteComponent(path("sprites/characters/slime.png"), 
                                               450, 600 , 20,
                                               20, (32, 30), (6, 6))),
        2 : ((2, 1.5, 1, 2), (10, 20), 'Goblin', SpriteComponent(path("sprites/characters/slime.png"), 
                                               450, 600 , 20,
                                               20, (32, 30), (6, 6)))
    }

    types = {
        1 : {
                'scaling' : (3, 0.5, 1, 2),
                'lvlrange' : (1, 10),
                'name' : 'Slime',
                'sprite' : SpriteComponent(path("sprites/characters/slime.png"), 
                                           450, 600 , 20,
                                           20, (32, 30), (6, 6)),
                'frames' : 6,
                'y' : 1
            },
        2 : {
                'scaling' : (2, 1.5, 1, 2),
                'lvlrange' : (10, 20),
                'name' : 'Goblin',
                'sprite' : SpriteComponent(path("sprites/characters/slime.png"), 
                                           450, 600 , 20,
                                           20, (32, 30), (6, 6)),
                'frames' : 6,
                'y' : 1
            }
    }

    def __init__(self, t):
        self.components = {'sprite' : self.types[t]['sprite']}
        self.lvl = random.randint(*(self.types[t]['lvlrange']))
        stat_points = (self.lvl) * 4
        scaling = self.types[t]['scaling']
        scaling_overall = sum(scaling)
        health = int(round(stat_points * scaling[0] / scaling_overall, 0))
        attack = int(round(stat_points * scaling[1] / scaling_overall, 0))
        agility = int(round(stat_points * scaling[2] / scaling_overall, 0))
        defense = int(round(stat_points * scaling[3] / scaling_overall, 0))
        super().__init__(self.types[t]['name'], health, attack, agility, defense)
        self.counter = 0
        self.frames = self.types[t]['frames']
        self.sprite_y = self.types[t]['y']

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

    def animation(self):
        self.counter += 1
        if self.counter > self.frames * 10 - 1:
            self.counter = 0

    def display_battle(self, screen, S_WIDTH, S_HEIGHT):
        self.animation()
        self.components['sprite'].battle_sprite(screen, self.sprite_y, self.counter, 
                                                S_WIDTH//2, S_HEIGHT - 500)