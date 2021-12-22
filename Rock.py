# -*- coding: utf-8 -*-
"""
Created on Tue Dec  7 21:46:34 2021

@author: WU
"""
import pygame as pg
import random
import os
WIDTH = 500
HIGH = 600

rocks_img = [] #upload different rocks
for i in range(7):
    rocks_img.append(pg.image.load(os.path.join("img"
                                        , f"rock{i}.png")))
    
class Rock (pg.sprite.Sprite): #rocks object
    def __init__ (self):
        pg.sprite.Sprite.__init__(self)

        self.image_ori = random.choice(rocks_img)
        self.image = self.image_ori.copy()
        self.rect = self.image.get_rect() #障礙物框起來
        self.radius = self.rect.width / 2
        #pg.draw.circle(self.image, (255, 0, 0), self.rect.center
                       #, self.radius)
        self.rect.x = random.randrange(0, WIDTH - 10)
        self.speedx = random.randrange(-1, 1)
        self.speedy = random.randrange(3, 6)
        self.rect.y = 0
        self.total_degree = 0
        self.rot_degree = random.randrange(-3, 3)
        
    def update (self):
        self.restatus()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HIGH or self.rect.x > WIDTH or self.rect.centerx < 0:
            self.rect.x = random.randrange(0, WIDTH - 10)
            self.rect.y = 0
    
    def restatus (self):
        self.total_degree += self.rot_degree
        self.total_degree %= 360
        self.image = pg.transform.rotate(self.image_ori
                                         , self.total_degree)
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center