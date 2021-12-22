# -*- coding: utf-8 -*-
"""
Created on Mon Dec  6 20:38:03 2021

@author: WU
"""
import pygame as pg
import random
import os

bullet_img = pg.image.load(os.path.join("img", "bullet.png"))

class Bullet (pg.sprite.Sprite): #bullets object
    def __init__ (self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(bullet_img, (10, 30))
        #self.image = pg.Surface((5, 5))
        #self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10
        
    def update (self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill() #移除子彈