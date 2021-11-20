import sys
import os
import traceback

import pygame
from pygame.locals import *
from random import *
import random
import numpy as np

# game initiation
pygame.init()

# set the wigte place
os.environ['SDL_VIDED_WINDOW_POS'] = "%d.%d" % (600,50)

# set the size of window and caption
row = 6
column = 6
block_color =  (0,0,0)
num_color = ((255,255,255),(255,200,200),(255,150,150),(255,100,100),(255,50,50),(255,0,0))
bg_size = width,height = 100*column,100*row
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption("game 2048")

# move the block num
def move(direction,num):
    num_new = np.zeros((row,column))
    if direction == 'left':
        num = num.transpose()
        for i in range(row):
            index = np.where(num[i]>0)
            a = len(index[0])
            if a != 0:
                for j in range(a):
                    num_new[i][j] = num[i][index[0][j]]
        num_new = num_new.transpose()
    elif direction == 'right':
        num = num.transpose()
        for i in range(row):
            index = np.where(num[i]>0)
            a = len(index[0])
            b = row-a
            if a != 0:
                for j in range(a):
                    num_new[i][j+b] = num[i][index[0][j]]
        num_new = num_new.transpose()
    elif direction == 'up':
        for i in range(row):
            index = np.where(num[i]>0)
            a = len(index[0])
            if a != 0:
                for j in range(a):
                    num_new[i][j] = num[i][index[0][j]]
    elif direction == 'down':
        for i in range(row):
            index = np.where(num[i]>0)
            a = len(index[0])
            b = column-a
            if a != 0:
                for j in range(a):
                    num_new[i][j+b] = num[i][index[0][j]]
    return num_new

# merge the same num beside
def merge(direction,num,score,end,update):
    num_new = np.zeros((row,column))
    if direction == 'left':
        num = num.transpose()
        for i in range(column):
            j = 0
            n = []
            while True:
                if num[i][j] == num[i][j+1]:
                    n.append(num[i][j]*2)
                    score += num[i][j]
                    if j+2 < column-1:
                        j += 2
                    elif j+2 == column-1:
                        n.append(num[i][j+2])
                        break
                    elif j+2 == column:
                        break
                if num[i][j] != num[i][j+1]:
                    n.append(num[i][j])
                    if j+1 < column-1:
                        j += 1
                    elif j+1 == column-1:
                        n.append(num[i][j+1])
                        break
            for m in range(len(n)):
                num_new[i][m] = n[m]
        num_new = num_new.transpose()
    elif direction == 'right':
        num = num.transpose()
        for i in range(column):
            j = 0
            n = []
            while True:
                b = column-j-1
                if num[i][b] == num[i][b-1]:
                    n.append(num[i][b]*2)
                    if j+2 < column-1:
                        j += 2
                    elif j+2 == column-1:
                        n.append(num[i][b-2])
                        break
                    elif j+2 == column:
                        break
                if num[i][b] != num[i][b-1]:
                    n.append(num[i][b])
                    if j+1 < column-1:
                        j += 1
                    elif j+1 == column-1:
                        n.append(num[i][b-1])
                        break
            for m in range(len(n)):
                num_new[i][column-1-m] = n[m]
        num_new = num_new.transpose()
    elif direction == 'up':
        for i in range(row):
            j = 0
            n = []
            while j < column-1:
                if num[i][j] == num[i][j+1]:
                    n.append(num[i][j]*2)
                    if j+2 < column-1:
                        j += 2
                    elif j+2 == column-1:
                        n.append(num[i][j+2])
                        break
                    elif j+2 == column:
                        break
                if num[i][j] != num[i][j+1]:
                    n.append(num[i][j])
                    if j+1 < column-1:
                        j += 1
                    elif j+1 == column-1:
                        n.append(num[i][j+1])
                        break
            for m in range(len(n)):
                num_new[i][m] = n[m]
    elif direction == 'down':
        for i in range(row):
            j = 0
            n = []
            while j < column-1:
                b = column-j-1
                if num[i][b] == num[i][b-1]:
                    n.append(num[i][b]*2)
                    if j+2 < column-1:
                        j += 2
                    elif j+2 == column-1:
                        n.append(num[i][b-2])
                        break
                    elif j+2 == column:
                        break
                if num[i][b] != num[i][b-1]:
                    n.append(num[i][b])
                    if j+1 < column-1:
                        j += 1
                    elif j+1 == column-1:
                        n.append(num[i][b-1])
                        break
            for m in range(len(n)):
                num_new[i][row-1-m] = n[m]
    index = np.where(num == 0)
    if len(index[0]) < 2:
        end = True
        update = False
    return num_new,score,end,update

# generate the 2 new num which value is 2
def generate(num,update):
    if update:
        index = np.where(num == 0)
        index = list(zip(index[0],index[1]))
        a = random.sample(index,2)
        num[a[0][0]][a[0][1]] = 2
        num[a[1][0]][a[1][1]] = 2
        update = False
    return num,update

def drawblock():
    for i in range(row):
        for j in range(column):
            pygame.draw.rect(screen,block_color,(i*100+3,j*100+3,94,94))

def drawnum(num,score_font,score):
    index = np.where(num > 0)
    index = list(zip(index[0],index[1]))
    for i in range(len(index)):
        if num[index[i][0]][index[i][1]] == 2:
            score_text = score_font.render(str(int(num[index[i][0]][index[i][1]])),True,num_color[0])
            screen.blit(score_text,(int(index[i][0])*100+40,int(index[i][1])*100+40))
        elif num[index[i][0]][index[i][1]] == 4:
            score_text = score_font.render(str(int(num[index[i][0]][index[i][1]])),True,num_color[0])
            screen.blit(score_text,(int(index[i][0])*100+40,int(index[i][1])*100+40))
        elif num[index[i][0]][index[i][1]] == 8:
            score_text = score_font.render(str(int(num[index[i][0]][index[i][1]])),True,num_color[1])
            screen.blit(score_text,(int(index[i][0])*100+40,int(index[i][1])*100+40))
        elif num[index[i][0]][index[i][1]] == 16:
            score_text = score_font.render(str(int(num[index[i][0]][index[i][1]])),True,num_color[1])
            screen.blit(score_text,(int(index[i][0])*100+40,int(index[i][1])*100+40))
        elif num[index[i][0]][index[i][1]] == 32:
            score_text = score_font.render(str(int(num[index[i][0]][index[i][1]])),True,num_color[2])
            screen.blit(score_text,(int(index[i][0])*100+40,int(index[i][1])*100+40))
        elif num[index[i][0]][index[i][1]] == 64:
            score_text = score_font.render(str(int(num[index[i][0]][index[i][1]])),True,num_color[2])
            screen.blit(score_text,(int(index[i][0])*100+40,int(index[i][1])*100+40))
        elif num[index[i][0]][index[i][1]] == 128:
            score_text = score_font.render(str(int(num[index[i][0]][index[i][1]])),True,num_color[3])
            screen.blit(score_text,(int(index[i][0])*100+40,int(index[i][1])*100+40))
        elif num[index[i][0]][index[i][1]] == 256:
            score_text = score_font.render(str(int(num[index[i][0]][index[i][1]])),True,num_color[3])
            screen.blit(score_text,(int(index[i][0])*100+40,int(index[i][1])*100+40))
        elif num[index[i][0]][index[i][1]] == 512:
            score_text = score_font.render(str(int(num[index[i][0]][index[i][1]])),True,num_color[4])
            screen.blit(score_text,(int(index[i][0])*100+40,int(index[i][1])*100+40))
        elif num[index[i][0]][index[i][1]] == 1024:
            score_text = score_font.render(str(int(num[index[i][0]][index[i][1]])),True,num_color[4])
            screen.blit(score_text,(int(index[i][0])*100+40,int(index[i][1])*100+40))
        elif num[index[i][0]][index[i][1]] == 2048:
            score_text = score_font.render(str(int(num[index[i][0]][index[i][1]])),True,num_color[5])
            screen.blit(score_text,(int(index[i][0])*100+40,int(index[i][1])*100+40))


def main():
    clock = pygame.time.Clock()

    # 设置分数
    score = 0
    score_font = pygame.font.Font("font/arial.ttf",30)
    
    update = True
    running = True
    direction = None
    start = False
    end = False

    # 初始化数组
    num = np.zeros((row,column))
    num,update = generate(num,update)

    # 进入游戏循环
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYUP:
                if event.key == K_LEFT:
                    update = True
                    direction = 'left'
                elif event.key == K_RIGHT:
                    update = True
                    direction = 'right'
                elif event.key == K_UP:
                    update = True
                    direction = 'up'
                elif event.key == K_DOWN:
                    update = True
                    direction = 'down'
                if event.key == K_RETURN and not start and not end:
                    start = True

        if not start:   # 绘制开始界面
            screen.fill((255,255,255))
            pygame.draw.rect(screen,(255,100,100),(width/2-70,height/2-25,140,50))
            score_text = score_font.render('START',True,num_color[0])
            screen.blit(score_text,(width/2-50,height/2-20))
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                if width/2-70 < pos[0] < width/2+70 and height/2-25 < pos[1] < height/2+25:
                    start = True
        
        if end:  # 绘制结束界面
            start = False
            screen.fill((255,255,255))
            pygame.draw.rect(screen,(255,100,100),(width/2-70,height/2-60,140,50))
            pygame.draw.rect(screen,(255,100,100),(width/2-70,height/2+10,140,50))
            score_text = score_font.render('SCORE:'+str(int(score)),True,num_color[4])
            screen.blit(score_text,(width/2-70,height/2-150))
            score_text = score_font.render('RESTART',True,num_color[0])
            screen.blit(score_text,(width/2-70,height/2-50))
            score_text = score_font.render('CLOSE',True,num_color[0])
            screen.blit(score_text,(width/2-50,height/2+20))
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                if width/2-70 < pos[0] < width/2+70 and height/2-60 < pos[1] < height/2-10: # 重新开始
                    start = True
                    end = False
                    update = True
                    num = np.zeros((row,column))
                    num,update = generate(num,update)
                if width/2-70 < pos[0] < width/2+70 and height/2+10 < pos[1] < height/2+60:  # 结束并退出游戏
                    pygame.quit()
                    sys.exit()

        if start: # 开始游戏
            
            # 更新操作结果
            if update:
                num = move(direction,num)
                num,score,end,update = merge(direction,num,score,end,update)
                num,update = generate(num,update)
            # 绘制背景
            screen.fill((255,255,255))
            # 绘制数字背景
            drawblock()
            # 绘制数字
            drawnum(num,score_font,score)
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()