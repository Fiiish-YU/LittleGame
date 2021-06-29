# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 13:32:28 2020

@author: xun
"""

import pygame
from random import *

class SmallEnemy(pygame.sprite.Sprite):
    
    #energy = 1
    
    def __init__(self,bg_size):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load("images/enemy1.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.width,self.height = bg_size[0],bg_size[1]
        self.speed = 2
        self.active = True
        self.rect.left,self.rect.top = \
                                       randint(0,self.width - self.rect.width),\
                                       randint(-5*self.height,0)
        self.mask = pygame.mask.from_surface(self.image)
        #self.energy = SmallEnemy.energy
        
    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()
            
    def reset(self):
        self.active = True
        #self.energy = SmallEnemy.energy
        self.rect.left,self.rect.top = \
                                       randint(0,self.width - self.rect.width),\
                                       randint(-5*self.height,0)
                                       

class MidEnemy(pygame.sprite.Sprite):
    
    energy = 8          
    
    def __init__(self,bg_size):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load("images/enemy2.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.width,self.height = bg_size[0],bg_size[1]
        self.rect.left,self.rect.top = \
                                       randint(0,self.width - self.rect.width),\
                                       randint(-10*self.height,-self.height)
        self.speed = 2
        self.active = True
        self.mask = pygame.mask.from_surface(self.image)
        self.energy = MidEnemy.energy
        
    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()
            
    def reset(self):
        self.active = True
        self.energy = MidEnemy.energy
        self.rect.left,self.rect.top = \
                                       randint(0,self.width - self.rect.width),\
                                       randint(-10*self.height,-self.height)
                                       
class BigEnemy(pygame.sprite.Sprite):
    
    energy = 20
    
    def __init__(self,bg_size):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load("images/enemy3.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.width,self.height = bg_size[0],bg_size[1]
        self.rect.left,self.rect.top = \
                                       randint(0,self.width - self.rect.width),\
                                       randint(-15*self.height,-5*self.height)
        self.speed = 1
        self.active = True
        self.mask = pygame.mask.from_surface(self.image)
        self.energy = BigEnemy.energy
        
    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()
            
    def reset(self):
        self.active = True
        self.energy = BigEnemy.energy
        self.rect.left,self.rect.top = \
                                       randint(0,self.width - self.rect.width),\
                                       randint(-15*self.height,-5*self.height)                                       