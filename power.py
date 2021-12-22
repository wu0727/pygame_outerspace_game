# -*- coding: utf-8 -*-
"""
Created on Mon Dec  6 20:48:34 2021

@author: WU
"""

import pygame as pg
import random
import os

WIDTH = 500
HIGH = 600

#shield_sound = pg.mixer.Sound(os.path.join("sound", "pow1.wav"))
#gunup_sound = pg.mixer.Sound(os.path.join("sound", "pow0.wav"))
power_img = {}
power_img['shield'] = pg.image.load(os.path.join("img", "shield.png"))
power_img['gun'] = pg.image.load(os.path.join("img", "gun.png"))

class power (pg.sprite.Sprite): #explsoin object
    def __init__ (self, center):
        pg.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun'])
        self.image = power_img[self.type]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 3
        
        
    def update (self):
        self.rect.y += self.speedy
        if self.rect.top > HIGH:
            self.kill()