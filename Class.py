import pygame
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

    def display(self, screen, width, height):
        rect = pygame.Rect(0, 0, 500, 50)
        rect.center = (width//2, height - 100)
        pygame.draw.rect(screen, 'purple', rect)
        pygame.draw.rect(screen, 'black', rect, 2)
        health_text = font(32).render(f'{self.current_health}/{self.health}', True, 'black')
        screen.blit(health_text, health_text.get_rect(center=rect.center))

class Monsters(Entities):

    monster_types = {
        1 : ((2, 1.5, 1, 2), 'Goblin')
    }

    def __init__(self, lvl, m_type):
        stat_points = lvl * 4
        scaling = monster_types[m_type][0]
        scaling_overall = sum(scaling)
        health = stat_points * scaling[0] / scaling_overall
        attack = stat_points * scaling[1] / scaling_overall
        agility = stat_points * scaling[2] / scaling_overall
        defense = stat_points * scaling[3] / scaling_overall
        super().__init__(monster_types[m_type][1], health, attack, agility, defense)

class Player(Entities):
    def __init__(self, 
                 name,
                 stats=[], 
                 add_stats=[]):

        if stats == []:
            super().__init__(name, 0, 0, 0, 0)
        else:
            super().__init__(name, *stats)

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

