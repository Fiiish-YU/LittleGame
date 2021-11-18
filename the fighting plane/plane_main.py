# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 21:49:24 2020

@author: xun
"""
# main.py

import pygame
import sys 
import traceback
import myplane
import bullet
import enemy
import supply
import os

from pygame.locals import *
from random import *

#设置颜色
BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)
RED = (255,0,0)

#初始化
pygame.init()
pygame.mixer.init()  #混音器初始化
#设置窗口位置
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (600,50)
#设置窗口大小以及标题栏
bg_size = width,height = 480,700  #背景尺寸
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption("飞机大战")

background = pygame.image.load("images/background.png").convert() #载入背景图片

#载入游戏音乐
pygame.mixer.music.load("C:/Users/xun/Music/AudioConvert/banma.wav") #背景音乐
pygame.mixer.music.set_volume(0.2)

#载入游戏开始画面
gamebegin_image = pygame.image.load("images/game_begin.png").convert_alpha()

def add_small_enemies(group1,group2,num):
    for i in range(num):
        e1 = enemy.SmallEnemy(bg_size)
        group1.add(e1)
        group2.add(e1)

def add_mid_enemies(group1,group2,num):
    for i in range(num):
        e2 = enemy.MidEnemy(bg_size)
        group1.add(e2)
        group2.add(e2)
        
def add_big_enemies(group1,group2,num):
    for i in range(num):
        e3 = enemy.BigEnemy(bg_size)
        group1.add(e3)
        group2.add(e3)

def inc_speed(target,inc):
    for each in target:
        each.speed += inc

def main():

    pygame.mixer.music.play(-1)

    #生成我方飞机
    me = myplane.MyPlane(bg_size) 
    #生成敌机
    enemies = pygame.sprite.Group()
    small_enemies = pygame.sprite.Group()
    add_small_enemies(small_enemies,enemies,15)
    mid_enemies = pygame.sprite.Group()
    add_mid_enemies(mid_enemies,enemies,4) 
    big_enemies = pygame.sprite.Group()
    add_big_enemies(big_enemies,enemies,2)
    
    #生成子弹
    bullet1 = []
    bullet1_index = 0
    BULLET1_NUM = 4
    for i in range(BULLET1_NUM):
        bullet1.append(bullet.Bullet1((me.rect.centerx-5,me.rect.centery-30)))
    #生成超级子弹
    bullet2 = []
    bullet2_index = 0
    BULLET2_NUM = 8
    for i in range(BULLET2_NUM // 2):
        bullet2.append(bullet.Bullet2((me.rect.centerx-23,me.rect.centery)))
        bullet2.append(bullet.Bullet2((me.rect.centerx+12,me.rect.centery)))
    
    clock = pygame.time.Clock()
    
    #统计得分
    score = 0
    score_font = pygame.font.Font("font/SHOWG.TTF",36)
    #判断是否暂停游戏
    paused = False  
    pause_nor_image = pygame.image.load("images/pause1.png").convert_alpha()
    pause_pressed_image = pygame.image.load("images/pause2.png").convert_alpha()
    resume_nor_image = pygame.image.load("images/resume2.png").convert_alpha()
    resume_pressed_image = pygame.image.load("images/resume1.png").convert_alpha()
    paused_rect = pause_nor_image.get_rect()
    paused_rect.left,paused_rect.top = width - paused_rect.width-8,1
    paused_image = pause_nor_image
    
    level = 1  #设置游戏难度
    
    #全屏炸弹
    bomb_image = pygame.image.load("images/bomb.png").convert_alpha()
    bomb_rect = bomb_image.get_rect()
    bomb_font = pygame.font.Font("font/SHOWG.TTF",36)
    bomb_num = 3
    
    #每30s补给包
    bullet_supply = supply.Bullet_Supply(bg_size)
    bomb_supply = supply.Bomb_Supply(bg_size)
    SUPPLY_TIME = USEREVENT
    pygame.time.set_timer(SUPPLY_TIME,20*1000)
    
    #超级子弹定时器
    DOUBLE_BULLET_TIME = USEREVENT + 1
    is_double_bullet = False
    
    #我方飞机生命
    life_image = pygame.image.load("images/life.png").convert_alpha()
    life_rect = life_image.get_rect()
    life_num = 3

    #载入游戏结束画面材料
    gameover_font = pygame.font.Font("font/SHOWG.TTF",36)
    again_image = pygame.image.load("images/start_again.png").convert_alpha()
    #again_rect = again_image.get_rect()
    gameover_image = pygame.image.load("images/game_over.png").convert_alpha()
    #gameover_rect = gameover_image.get_rect()
    
    #我方无敌状态计时
    INVINCIBLE_TIME = USEREVENT + 2
    
    #限制记录文件打开
    recorded = False
    
    switch_image = True  #用于切换图片
    delay = 100 #延迟
    
    running = True
    
    while running:
        for event in pygame.event.get():  #事件响应
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1 and paused_rect.collidepoint(event.pos):
                    paused = not paused
                    if paused:
                        paused_image = resume_nor_image
                    else:
                        paused_image = pause_nor_image
            elif event.type == MOUSEMOTION:
                if paused_rect.collidepoint(event.pos):
                    if paused:
                        paused_image = resume_pressed_image
                    else:
                        paused_image = pause_pressed_image
                else:
                    if paused:
                        paused_image = resume_nor_image
                    else:
                        paused_image = pause_nor_image
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if not paused and bomb_num > 0:
                        bomb_num -= 1
                        for each in enemies:
                            if each.rect.bottom > 0:
                                each.active = False
            elif event.type == SUPPLY_TIME:
                if choice([True,False]):
                    bomb_supply.reset()
                else:
                    bullet_supply.reset()
            elif event.type == DOUBLE_BULLET_TIME:
                is_double_bullet = False
                pygame.time.set_timer(DOUBLE_BULLET_TIME,0)
            elif event.type == INVINCIBLE_TIME:
                me.invincible = False                 
                pygame.time.set_timer(INVINCIBLE_TIME ,0)
                
        #根据分数提升难度
        if level == 1 and score > 500:
            level = 2
            add_small_enemies(small_enemies,enemies,3)  #增加敌机
            add_mid_enemies(mid_enemies,enemies,2)
            add_big_enemies(big_enemies,enemies,1)
            inc_speed(small_enemies,0.5)         #增加速度
        elif level == 2 and score > 5000:
            level = 3
            add_small_enemies(small_enemies,enemies,5)
            add_mid_enemies(mid_enemies,enemies,3)
            add_big_enemies(big_enemies,enemies,2)
            inc_speed(small_enemies,1)
            inc_speed(mid_enemies,0.5)
        elif level == 3 and score > 30000:
            level = 4
            add_small_enemies(small_enemies,enemies,5)
            add_mid_enemies(mid_enemies,enemies,3)
            add_big_enemies(big_enemies,enemies,2)
            inc_speed(small_enemies,1)
            inc_speed(mid_enemies,0.5)
        elif level == 4 and score > 60000:
            level = 5
            add_small_enemies(small_enemies,enemies,5)
            add_mid_enemies(mid_enemies,enemies,3)
            add_big_enemies(big_enemies,enemies,2)
            inc_speed(small_enemies,1)
            inc_speed(mid_enemies,0.5)
        
        screen.blit(background,(0,0))
        
        if life_num and not paused:
            #检测用户键盘操作
            key_pressed = pygame.key.get_pressed()
            if key_pressed[K_w] or key_pressed[K_UP]:
                me.moveUp()
            if key_pressed[K_s] or key_pressed[K_DOWN]:
                me.moveDown()     
            if key_pressed[K_a] or key_pressed[K_LEFT]:
                me.moveLeft()
            if key_pressed[K_d] or key_pressed[K_RIGHT]:
                me.moveRight()
                
            #画背景屏幕      
            screen.blit(background,(0,0)) 
            #绘制补给并检测是否获得
            if bomb_supply.active:
                bomb_supply.move()
                screen.blit(bomb_supply.image,bomb_supply.rect)
                if pygame.sprite.collide_mask(bomb_supply,me):
                    if bomb_num < 3:
                        bomb_num +=1
                    bomb_supply.active = False
            if bullet_supply.active:
                bullet_supply.move()
                screen.blit(bullet_supply.image,bullet_supply.rect)
                if pygame.sprite.collide_mask(bullet_supply,me):
                    is_double_bullet = True
                    pygame.time.set_timer(DOUBLE_BULLET_TIME,10*1000)
                    bullet_supply.active = False
            #发射子弹
            if not(delay % 10):
                if is_double_bullet:
                    bullets = bullet2
                    bullets[bullet2_index].reset((me.rect.centerx-23,me.rect.centery))
                    bullets[bullet2_index+1].reset((me.rect.centerx+12,me.rect.centery))
                    bullet2_index = (bullet2_index + 2) % BULLET2_NUM
                else:
                    bullets = bullet1
                    bullet1[bullet1_index].reset((me.rect.centerx-5,me.rect.centery-30))
                    bullet1_index = (bullet1_index+1)%BULLET1_NUM
            #检测子弹是否击中敌机
            for b in bullets:
                if b.active:
                    b.move()
                    screen.blit(b.image,b.rect)
                    enemy_hit = pygame.sprite.spritecollide(b,enemies,False,pygame.sprite.collide_mask)
                    if enemy_hit:
                        b.active = False
                        for e in enemy_hit:
                            if e in mid_enemies or e in big_enemies:
                                e.energy -= 1
                                if e.energy == 0:
                                    e.active = False 
                            else:
                                e.active = False
            
            #绘制敌机&毁灭
            for each in big_enemies:  #大型敌机
                if each.active:
                    each.move()
                    screen.blit(each.image,each.rect)
                    #绘制血槽
                    pygame.draw.line(screen,BLACK,\
                                     (each.rect.left,each.rect.top - 5),\
                                     (each.rect.right,each.rect.top - 5), 2 )
                    energy_remain = each.energy / enemy.BigEnemy.energy
                    if energy_remain > 0.2:
                        energy_color = GREEN
                    else:
                        energy_color = RED
                    pygame.draw.line(screen,energy_color,\
                                     (each.rect.left,each.rect.top - 5),\
                                     (each.rect.left + each.rect.width * energy_remain, \
                                     each.rect.top - 5 ),2)           
                else:
                    score += 1000
                    each.reset()
            for each in mid_enemies:  #中型敌机
                if each.active:
                    each.move()
                    screen.blit(each.image,each.rect)
                    #绘制血槽
                    pygame.draw.line(screen,BLACK,\
                                     (each.rect.left,each.rect.top - 5),\
                                     (each.rect.right,each.rect.top - 5), 2 )
                    energy_remain = each.energy / enemy.MidEnemy.energy
                    if energy_remain > 0.2:
                        energy_color = GREEN
                    else:
                        energy_color = RED
                    pygame.draw.line(screen,energy_color,\
                                     (each.rect.left,each.rect.top - 5),\
                                     (each.rect.left + each.rect.width * energy_remain, \
                                     each.rect.top - 5 ),2)                   
                else:
                    score += 600 
                    each.reset()
            for each in small_enemies:  #小型敌机
                if each.active:
                    each.move()
                    screen.blit(each.image,each.rect)
                else:
                    score += 100
                    each.reset()
            #检测飞机是否被撞(碰撞检测)
            enemies_down = pygame.sprite.spritecollide(me,enemies,False,pygame.sprite.collide_mask)
            if enemies_down and not me.invincible:
                me.active = False
                for e in enemies_down:
                    e.active = False
            #画我方飞机        
            if me.active:
                if switch_image:
                    screen.blit(me.image1,me.rect)   
                else:
                    screen.blit(me.image2,me.rect) 
            else:
                life_num -= 1
                me.reset()
                pygame.time.set_timer(INVINCIBLE_TIME,3*1000)
                
            #绘制炸弹
            bomb_text = bomb_font.render("× %d" % bomb_num,True,WHITE)
            text_rect = bomb_text.get_rect()
            screen.blit(bomb_image,(10,height - 10 - bomb_rect.height))
            screen.blit(bomb_text,(10 + bomb_rect.width,height - 5 - text_rect.height))
            #绘制生命数量
            if life_num:
                for i in range(life_num):
                    screen.blit(life_image,(width-10-(i+1)*life_rect.width,height-10-life_rect.height))
            #绘制得分        
            score_text = score_font.render("Score : %s" % str(score),True,WHITE)
            screen.blit(score_text,(10,5))
        #绘制游戏结束
        elif life_num == 0:
            pygame.time.set_timer(SUPPLY_TIME,0)
            if not recorded:
                with open("record.txt","r") as f:
                    record_score = int(f.read())
                if score > record_score:
                    with open("record.txt","w") as f:
                        f.write(str(score))
            #结束画面
            record_score_text = score_font.render("Best : %d" % record_score,True,WHITE)
            screen.blit(record_score_text,(50,50))
            gameover_text = gameover_font.render("Your score : %s" % str(score),True,WHITE)
            screen.blit(gameover_text,(90,150))
            screen.blit(again_image,(140,320))
            screen.blit(gameover_image,(140,400))
            #检测用户鼠标
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                if 140 < pos[0] < 340 and 320 < pos[1] < 360:
                       main()
                elif 140 < pos[0] < 340 and 400 < pos[1] < 440:
                       pygame.quit()
                       sys.exit()
      
        #绘制暂停按钮
        screen.blit(paused_image,paused_rect)
        
        #切换图片----
        if not(delay % 5):
            switch_image = not switch_image
        delay -= 1
        if not delay:
            delay = 100
        
        pygame.display.flip()
        
        clock.tick(60)
        
if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()
