# -*- coding: utf-8 -*-
"""
Created on Tue Dec  7 22:32:58 2021

@author: WU
"""
import pygame as pg


WIDTH = 500
HIGH = 600
FPS = 60
RGB = (0, 0, 0)




def draw_HP (surf, hp, x, y):
    if hp < 0 : hp = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (hp / 100) * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    pg.draw.rect(surf, (0, 255, 0), fill_rect)
    pg.draw.rect(surf, (255, 255, 255), outline_rect, 2)

def player_HP (surf, live, img, x, y):
    for i in range(live):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)