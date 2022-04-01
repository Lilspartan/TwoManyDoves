import time
import thumby
import math
import random

# BITMAP: width: 8, height: 8
playerR = bytearray([0,255,255,49,63,241,255,0])
playerC = bytearray([0,255,241,63,63,241,255,0])
playerL = bytearray([0,255,241,63,49,255,255,0])

gameRunning = True

'''
Game States:

playing - playing the game
win - won the game
lose - lost the game
pause - paused the game
'''
gameState = "playing"

class Player:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.maxTilesW = round(thumby.display.width / self.width)
        self.maxTilesH = round(thumby.display.height / self.height)
        self.tile = round(self.maxTilesW / 2)
        self.direction = 0
        self.maxBullets = 3
        self.sprite = playerC
        self.offset = 2
    
    def turn(self, dir):
        if (dir == -1):
            self.sprite = playerL
        elif (dir == 0):
            self.sprite = playerC
        elif (dir == 1):
            self.sprite = playerR
        
    def move(self, dir):
        self.tile += dir
        self.direction = dir
        self.turn(dir)
    
    def draw(self):
        if (self.direction == -1):
            thumby.display.blit(self.sprite, self.tile * self.width, thumby.display.height - (self.height + self.offset), self.width, self.height, 0, 0, 0)
        elif (self.direction == 0):
            thumby.display.blit(self.sprite, self.tile * self.width, thumby.display.height - (self.height + self.offset), self.width, self.height, 0, 0, 0)
        elif (self.direction == 1):
            thumby.display.blit(self.sprite, self.tile * self.width, thumby.display.height - (self.height + self.offset), self.width, self.height, 0, 0, 0)

class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 2
        self.height = 3
        self.sprite = bytearray([3])
        self.speed = 1
        
    def update(self, t):
        if (t0 % 5 == 0):
            self.y -= self.speed
        if (self.y < -5):
            self.speed = 0
        
    def draw(self):
        thumby.display.blit(self.sprite, self.x, self.y, self.width, self.height, 0, 0, 0)
     
class DoveObject:
    doves = []
    row1 = [1, 1, 1, 1, 1, 1]
    row2 = [1, 1, 0, 1, 1, 0]
    doves.append(row1)
    doves.append(row2)
    
    def __init__(self, doveWidth, doveHeight):
        self.width = doveWidth * len(DoveObject.doves[0])
        self.height = doveHeight * len(DoveObject.doves)
        self.tileX = 0
        self.tileY = 0
        self.doveWidth = doveWidth
        self.doveHeight = doveHeight
        self.direction = 1
        self.maxTilesW = round(thumby.display.width / self.doveWidth)
        self.maxTilesH = round(thumby.display.height / self.doveHeight)
        self.spriteLeft = bytearray([2,7,29,191,254,62,60,24])
        self.spriteRight = bytearray([24,60,62,254,191,29,7,2])
        
    def drawBBox(self):
        thumby.display.drawRectangle(self.tileX * self.doveWidth, self.tileY * self.doveHeight, (self.tileX * self.doveWidth) + self.width, (self.tileY * self.doveHeight) + self.height, 1)
        
    def displayDove(self, indexOuter, indexInner):
        if (self.direction == 1):
            thumby.display.blit(self.spriteRight, (self.tileX * self.doveWidth) + (indexInner * self.doveWidth), (indexOuter * self.doveHeight), self.doveWidth, self.doveHeight, 0, 0, 0)
        if (self.direction == -1):
            thumby.display.blit(self.spriteLeft, (self.tileX * self.doveWidth) + (indexInner * self.doveWidth), (indexOuter * self.doveHeight), self.doveWidth, self.doveHeight, 0, 0, 0)
        
    def draw(self):
        for dr in range(len(DoveObject.doves)):
            for d in range(len(DoveObject.doves[dr])):
                if (DoveObject.doves[dr][d] == 1):
                    self.displayDove(dr, d)
        
    def turn(self, direction):
        self.direction = direction
        
    def move(self):
        if (self.direction == 1):
            self.tileX += 1
        else:
            self.tileX -= 1
            
        print(self.maxTilesW)
        
        if (self.tileX == 3):
            self.direction = -1
        elif (self.tileX == 0):
            self.direction = 1
    
player = Player(8, 8)    
bullet = Bullet(0, -10)

doveObject = DoveObject(8, 8)

while (gameRunning):
    t0 = time.ticks_ms()   # Get time (ms)
    thumby.display.fill(0) # Fill canvas to black
        
    
    if (2 > 0):
        if(thumby.buttonR.justPressed() == True):
            player.move(1)
        if(thumby.buttonL.justPressed() == True):
            player.move(-1)
        
        if (player.tile >= player.maxTilesW):
            player.tile = 0
        elif (player.tile < 0):
            player.tile = player.maxTilesW - 1
        
        #Shoot new bullet
        if ((thumby.buttonA.justPressed() or thumby.buttonB.justPressed() or thumby.buttonU.justPressed()) and bullet.speed == 0):
            bullet = Bullet(round((player.tile * player.width) + player.width / 2), thumby.display.height - player.height - 5)
            player.turn(0)
        
        #Draw every bullet
        bullet.update(t0)
        bullet.draw()
        
        # doveObject.drawBBox()
        doveObject.draw()
        
        if (t0 % 100 == 0):
            doveObject.move();
        
        # Draw the player sprite
        player.draw()
    else:
        thumby.display.drawText("YOU WIN", 0, 0, 1)
    
    thumby.display.update()
     
    
