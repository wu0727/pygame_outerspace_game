# -*- coding: utf-8 -*-
"""
Created on Fri Nov 19 22:59:23 2021

@author: WU
"""

import pygame as pg
import random
import os

import power
import Bullet
import Rock
import draw

WIDTH = 500
HIGH = 600
FPS = 60
RGB = (0, 0, 0)

pg.init() #初始化pygame
screen = pg.display.set_mode((WIDTH, HIGH))
clock = pg.time.Clock()
pg.display.set_caption("星之遊戲")

background = pg.image.load(os.path.join("img", "background.png")).convert()
play_img = pg.image.load(os.path.join("img", "player.png"))
play_mini_img = pg.transform.scale(play_img, (25, 19))

pg.display.set_icon(play_mini_img)

rocks_img = [] #upload different rocks
for i in range(7):
    rocks_img.append(pg.image.load(os.path.join("img"
                                        , f"rock{i}.png")))
expl_anime = {} 
expl_anime['lg'] = [] #big explosion
expl_anime['sm'] = [] #small explosion
for i in range(9):
    expl_img = pg.image.load(os.path.join("img", f"expl{i}.png"))
    expl_anime['lg'].append(pg.transform.scale(expl_img, (75, 75)))
    expl_anime['sm'].append(pg.transform.scale(expl_img, (30, 30)))

player_expl = []
for i in range(9):
    playexpl_img = pg.image.load(os.path.join("img", f"player_expl{i}.png"))
    player_expl.append(pg.transform.scale(playexpl_img, (75, 75)))
power_img = {}
power_img['shield'] = pg.image.load(os.path.join("img", "shield.png"))
power_img['gun'] = pg.image.load(os.path.join("img", "gun.png"))

shoot_sound = pg.mixer.Sound(os.path.join("sound", "shoot.wav"))
explore_sounds = [
pg.mixer.Sound(os.path.join("sound", "expl0.wav")),
pg.mixer.Sound(os.path.join("sound", "expl1.wav"))
] #explore sound
player_explsound = pg.mixer.Sound(os.path.join("sound", "rumble.ogg"))
shield_sound = pg.mixer.Sound(os.path.join("sound", "pow0.wav"))
gunup_sound = pg.mixer.Sound(os.path.join("sound", "pow1.wav"))
background_sound = pg.mixer.Sound(os.path.join("sound", "background.ogg"))
background_sound.set_volume(0.4) #set the voice
 
font_name = pg.font.match_font('arial')


def draw_init():
    draw_text(screen,"Outer Space Service Fight!" , 48, WIDTH / 2, HIGH / 4)
    draw_text(screen,"← → move, Space is shoot bullet" , 22, WIDTH / 2, HIGH / 2)
    draw_text(screen,"put any key yo start the game!" , 18, WIDTH / 2, HIGH * 3 / 4)
    pg.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS)
        #get the input
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return True
            elif event.type == pg.KEYUP:
                waiting = False
                return False
def draw_text (surf, text, size, x, y):
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)


bullet_img = pg.image.load(os.path.join("img", "bullet.png"))

class Player (pg.sprite.Sprite): #player object
    def __init__ (self):
        pg.sprite.Sprite.__init__ (self)
        self.image = pg.transform.scale(play_img, (50, 38))      
        self.rect = self.image.get_rect() #將圖片框起來
        self.radius = self.rect.width / 2
        self.rect.center = (WIDTH / 2, HIGH - 10)
        self.health = 100
        self.life = 3    
        self.hidden = False
        self.hide_time = 0
        self.gun = 1
        self.gun_time = 0
        #pg.draw.circle(self.image, (255,0 , 0), self.rect.center
        #               , self.radius)
    def update (self):
        now = pg.time.get_ticks()
        if self.gun > 1 and now - self.gun_time > 3000:
            self.gun = 1
            self.gun_time = now
        if self.hidden and now - self.hide_time > 1000:
            self.hidden = False
            self.rect.center = (WIDTH / 2, HIGH - 10)
        
        key_pressed = pg.key.get_pressed()
        if key_pressed[pg.K_a]: #depress a of keyboard
            if self.rect.x < 0:
                self.rect.x = 0
            self.rect.x -= 5
        elif key_pressed[pg.K_d]: #depress d of keyboard
            if self.rect.x > WIDTH - self.rect.width:
                self.rect.x = WIDTH - self.rect.width
            self.rect.x += 5
    def shoot(self):
        if not self.hidden:
            if self.gun == 1:
                bullet = Bullet.Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)  
                bullets.add(bullet)
                shoot_sound.play()
            else:
                bullet1 = Bullet.Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet.Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)  
                bullets.add(bullet1)
                all_sprites.add(bullet2)  
                bullets.add(bullet2)
                shoot_sound.play()
    def hide(self):
        self.hidden = True
        self.hide_time = pg.time.get_ticks()
        self.rect.center = (WIDTH / 2, HIGH * 2)
        
    def gunup(self):
        self.gun += 1
        self.gun_time = pg.time.get_ticks()
        
class Explosion (pg.sprite.Sprite): #explsoin object
    def __init__ (self, center, size):
        pg.sprite.Sprite.__init__(self)
        self.size = size
        self.image = expl_anime[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pg.time.get_ticks()
        self.frame_rate = 50
        
    def update (self):
        now = pg.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(expl_anime[self.size]):
                self.kill()
            else:
                self.image = expl_anime[self.size][self.frame]
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = center


all_sprites = pg.sprite.Group()
player = Player()
all_sprites.add(player)

rocks = pg.sprite.Group()
bullets = pg.sprite.Group()
powers = pg.sprite.Group()
for i in range(8):
    rock = Rock.Rock()
    all_sprites.add(rock)
    rocks.add(rock)

score = 0
background_sound.play() #play the background music

#game loop
show_init = True
running = True
while running:
    if show_init:
        close = draw_init()
        if close:
            break
        show_init = False
    clock.tick(FPS) #一秒鐘最多只能十次
    # get player move
    

    for event in pg.event.get(): #回傳所有發生事件(列表
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN: #判斷按下鍵盤
            if event.key == pg.K_SPACE: #判斷按下空白建
                player.shoot()
            
    #update game
    all_sprites.update()
    hits = pg.sprite.groupcollide(rocks, bullets, True, True)
    for hit in hits:
        random.choice(explore_sounds).play()
        score += hit.radius / 2
        r = Rock.Rock()
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(r)
        all_sprites.add(expl)
        rocks.add(r)
        if random.random() > 0.9: #drop the power
           po = power.power(hit.rect.center)
           all_sprites.add(po)
           powers.add(po)   #add the power to sprite
    #player.update()
    powerHitPlayer = pg.sprite.spritecollide(player, powers, True)
    for hit in powerHitPlayer:
        if hit.type == 'shield':
            shield_sound.play()
            player.health += 20
            if player.health > 100:
                player.health = 100
        else:
            player.gunup()
            gunup_sound.play()
    hitsPlay = pg.sprite.spritecollide(player, rocks, True, pg.sprite.collide_circle)
    for hit in hitsPlay:
        random.choice(explore_sounds).play()
        r = Rock.Rock()
        expl = Explosion(player.rect.center, 'sm')
        
        all_sprites.add(r)
        rocks.add(r)
        player.health -= hit.radius
        if player.health <= 0:
            player.life -= 1
            player.health = 100
            player_explsound.play()
            expl = Explosion(player.rect.center, 'lg')
            player.hide()
        all_sprites.add(expl)
        
    if player.life == 0 and not(expl.alive()):
        running = False
    #rock.update()
    
    #show screen
    screen.blit(background, (0, 0))
    all_sprites.draw(screen)
    draw_text(screen, "Score:" + str(score), 18, WIDTH / 2, 10)
    draw.draw_HP(screen, player.health, 5, 15)
    draw.player_HP(screen, player.life, play_mini_img, WIDTH - 140, 30)
    pg.display.update()    

pg.quit()