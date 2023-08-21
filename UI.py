import pygame
from functions import *

class StatWindow:
    def __init__(self):
        self.Surface = pygame.Surface((400, 500), pygame.SRCALPHA)

        self.healthSurf = pygame.Surface((300, 50), pygame.SRCALPHA)
        self.attackSurf = pygame.Surface((300, 50), pygame.SRCALPHA)
        self.agilitySurf = pygame.Surface((300, 50), pygame.SRCALPHA)
        self.defenseSurf = pygame.Surface((300, 50), pygame.SRCALPHA)

    def display(self, screen, player):

        self.Surface.fill('white')
        self.statTitle = font(20).render('Stat Window', True, 'black')
        self.Surface.blit(self.statTitle, self.statTitle.get_rect(center=(200, 50)))

        baselineY = 100
        initial = 25
        textSize = 15
        pointSize = 10
        empty = pygame.Color(0, 0, 0, 0)
        rect = pygame.Rect(0, 0, 20, 20)
        rectAddCenter = (240, 25)
        rectRemCenter = (290, 25)

        self.healthSurf.fill(empty)
        self.healthText = font(textSize).render('Health', True, 'black')
        self.healthSurf.blit(self.healthText, self.healthText.get_rect(midleft=(0, 12)))
        self.healthPoint = font(pointSize).render(f'{player.health}', True, 'black')
        self.healthSurf.blit(self.healthPoint, self.healthPoint.get_rect(midleft=(0, 38)))
        self.healthAddRect = rect
        self.healthAddRect.center = rectAddCenter
        pygame.draw.rect(self.healthSurf, 'green', self.healthAddRect)
        self.healthRemRect = rect
        self.healthRemRect.center = rectRemCenter
        pygame.draw.rect(self.healthSurf, 'red', self.healthRemRect)
        self.Surface.blit(self.healthSurf, self.healthSurf.get_rect(center=(200, initial + baselineY * 1)))

        self.attackSurf.fill(empty)
        self.attackText = font(textSize).render('Attack', True, 'black')
        self.attackSurf.blit(self.attackText, self.attackText.get_rect(midleft=(0, 12)))
        self.attackPoint = font(pointSize).render(f'{player.attack}', True, 'black')
        self.attackSurf.blit(self.attackPoint, self.attackPoint.get_rect(midleft=(0, 38)))
        self.attackAddRect = rect
        self.attackAddRect.center = rectAddCenter
        pygame.draw.rect(self.attackSurf, 'green', self.attackAddRect)
        self.attackRemRect = rect
        self.attackRemRect.center = rectRemCenter
        pygame.draw.rect(self.attackSurf, 'red', self.attackRemRect)
        self.Surface.blit(self.attackSurf, self.attackSurf.get_rect(center=(200, initial + baselineY * 2)))

        self.agilitySurf.fill(empty)
        self.agilityText = font(textSize).render('Agility', True, 'black')
        self.agilitySurf.blit(self.agilityText, self.agilityText.get_rect(midleft=(0, 12)))
        self.agilityPoint = font(pointSize).render(f'{player.agility}', True, 'black')
        self.agilitySurf.blit(self.agilityPoint, self.agilityPoint.get_rect(midleft=(0, 38)))
        self.agilityAddRect = rect
        self.agilityAddRect.center = rectAddCenter
        pygame.draw.rect(self.agilitySurf, 'green', self.agilityAddRect)
        self.agilityRemRect = rect
        self.agilityRemRect.center = rectRemCenter
        pygame.draw.rect(self.agilitySurf, 'red', self.agilityRemRect)
        self.Surface.blit(self.agilitySurf, self.agilitySurf.get_rect(center=(200, initial + baselineY * 3)))

        self.defenseSurf.fill(empty)
        self.defenseText = font(textSize).render('Defense', True, 'black')
        self.defenseSurf.blit(self.defenseText, self.defenseText.get_rect(midleft=(0, 12)))
        self.defensePoint = font(pointSize).render(f'{player.defense}', True, 'black')
        self.defenseSurf.blit(self.defensePoint, self.defensePoint.get_rect(midleft=(0, 38)))
        self.defenseAddRect = rect
        self.defenseAddRect.center = rectAddCenter
        pygame.draw.rect(self.defenseSurf, 'green', self.defenseAddRect)
        self.defenseRemRect = rect
        self.defenseRemRect.center = rectRemCenter
        pygame.draw.rect(self.defenseSurf, 'red', self.defenseRemRect)
        self.Surface.blit(self.defenseSurf, self.defenseSurf.get_rect(center=(200, initial + baselineY * 4)))
            
        totalStats = sum([player.health, player.attack, 
                          player.agility, player.defense])
        stats = player.lvl * 4
        overall = font(15).render(f'{totalStats} / {stats}', True, 'black')
        self.Surface.blit(overall, overall.get_rect(center=(200, 80)))

        screen.blit(self.Surface, self.Surface.get_rect(center=(350, 350)))

    def press(self, mouse_pos, player):
        totalStats = sum([player.health_property, player.attack, 
                          player.agility, player.defense])
        stats = player.lvl * 4
        rect = self.healthAddRect
        rect.x += 150
        rect.y += 100
        for i in range(1, 9):
            if i % 2 == 1:
                rect.y += 100
            else:
                rect.x += 50
            if rect.collidepoint(mouse_pos) and totalStats < stats:
                if i == 1:
                    player.health_property += 1
                elif i == 3:
                    player.attack += 1
                elif i == 5:
                    player.agility += 1
                elif i == 7:
                    player.defense += 1
            if rect.collidepoint(mouse_pos):
                if i == 2 and player.health_property > 1:
                    player.health_property -= 1
                elif i == 4 and player.attack > 1:
                    player.attack -= 1
                elif i == 6 and player.agility > 1:
                    player.agility -= 1
                elif i == 8 and player.defense > 1:
                    player.defense -= 1
            if i % 2 == 0:
                rect.x -= 50

class TurnSystem:
    def __init__(self, player, enemy):
        self.player_agi = player
        self.enemy_agi = enemy
        self.counter = max(self.player_agi, self.enemy_agi)
        self.player_counter = 0
        self.enemy_counter = 0

    def get_player(self):
        self.player_counter += self.player_agi
        if self.player_counter >= self.counter:
            self.player_counter -= self.counter
            return True

    def get_enemy(self):
        self.enemy_counter += self.enemy_agi
        if self.enemy_counter >= self.counter:
            self.enemy_counter -= self.counter
            return True