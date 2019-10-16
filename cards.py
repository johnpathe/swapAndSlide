#!/usr/bin/python3

import pygame

#Ace first
#Hearts first

SJ = pygame.image.load('images/sj.png')
SQ = pygame.image.load('images/sq.png')
SK = pygame.image.load('images/sk.png')
SA = pygame.image.load('images/sa.png')

CJ = pygame.image.load('images/cj.png')
CQ = pygame.image.load('images/cq.png')
CK = pygame.image.load('images/ck.png')
CA = pygame.image.load('images/ca.png')

DJ = pygame.image.load('images/dj.png')
DQ = pygame.image.load('images/dq.png')
DK = pygame.image.load('images/dk.png')
DA = pygame.image.load('images/da.png')

HJ = pygame.image.load('images/hj.png')
HQ = pygame.image.load('images/hq.png')
HK = pygame.image.load('images/hk.png')
HA = pygame.image.load('images/ha.png')

cardImages = [
    [HA,HK,HQ,HJ],
    [DA,DK,DQ,DJ],
    [CA,CK,CQ,CJ],
    [SA,SK,SQ,SJ]
]



def cardPos(x,y, cw, ch):
    positionsList = []
    # spacing..gap between X columns is 100, gap between Y rows is 130
    
    positionsList.append((x      ,y,cw,ch))
    positionsList.append((x + 100,y,cw,ch))
    positionsList.append((x + 200,y,cw,ch))
    positionsList.append((x + 300,y,cw,ch))
    
    positionsList.append((x      ,y + 130,cw,ch))
    positionsList.append((x + 100,y + 130,cw,ch))
    positionsList.append((x + 200,y + 130,cw,ch))
    positionsList.append((x + 300,y + 130,cw,ch))
    
    positionsList.append((x,      y + 260,cw,ch))
    positionsList.append((x + 100,y + 260,cw,ch))
    positionsList.append((x + 200,y + 260,cw,ch))
    positionsList.append((x + 300,y + 260,cw,ch))
    
    positionsList.append((x,      y + 390,cw,ch))
    positionsList.append((x + 100,y + 390,cw,ch))
    positionsList.append((x + 200,y + 390,cw,ch))
    positionsList.append((x + 300,y + 390,cw,ch))
    
    return positionsList



