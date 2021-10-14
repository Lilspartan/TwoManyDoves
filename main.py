import time
import thumby
import math

# BITMAP: width: 8, height: 8
playerR = (0,254,254,18,30,242,254,0)
playerC = (0,254,242,30,30,242,254,0)
playerL = (0,254,242,30,18,254,254,0)

gameRunning = True

class Player:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.maxTilesW = round(thumby.DISPLAY_W / self.width)
        self.maxTilesH = round(thumby.DISPLAY_H / self.height)
        self.tile = round(self.maxTilesW / 2)
        self.direction = 0
        self.maxBullets = 3
    
    def move(self, dir):
        self.tile += dir
        self.direction = dir
    
    def draw(self):
        if (self.direction == -1):
            thumby.display.blit(playerL, self.tile * self.width, thumby.DISPLAY_H - (self.height + 2), self.width, self.height)
        elif (self.direction == 0):
            thumby.display.blit(playerC, self.tile * self.width, thumby.DISPLAY_H - (self.height + 2), self.width, self.height)
        elif (self.direction == 1):
            thumby.display.blit(playerR, self.tile * self.width, thumby.DISPLAY_H - (self.height + 2), self.width, self.height)

class Dove:
    direction = 1
    moveDelay = 100
    numberofDoves = 7
    
    def __init__(self, width, height, tileX, tileY):
        self.width = width
        self.height = height
        self.spriteLeft = (4,14,26,62,188,252,60,56)
        self.spriteRight = (56,60,252,188,62,26,14,4)
        self.alive = True
        self.maxTilesW = round(thumby.DISPLAY_W / self.width)
        self.maxTilesH = round(thumby.DISPLAY_H / self.height)
        self.tileX = tileX
        self.tileY = tileY
        
    def checkHit(self):
        if (self.alive == True):
            if ((bullet.y <= (self.tileY * self.height) + self.height and bullet.y >= self.tileY * self.height) and (bullet.x <= (self.tileX * self.width) + self.width and bullet.x >= self.tileX * self.width)):
                self.alive = False
                Dove.numberofDoves -= 1
                bullet.y = -10
    
    def checkWall(self):    
        if (self.alive == True):
            if (self.tileX >= self.maxTilesW and Dove.direction == 1):
                Dove.direction = -1
            elif (self.tileX < 0 and Dove.direction == -1):
                Dove.direction = 1
    
    def move(self):
        if (self.alive == True):
            if (Dove.direction == 1):
                self.tileX += 1
            elif (Dove.direction == -1):
                self.tileX -= 1
    
    def draw(self):
        if (self.alive == True):
            if (Dove.direction == -1):
                thumby.display.blit(self.spriteLeft, self.tileX * self.width, self.tileY * self.height, self.width, self.height)
            elif (Dove.direction == 1):
                thumby.display.blit(self.spriteRight, self.tileX * self.width, self.tileY * self.height, self.width, self.height)

class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 2
        self.height = 3
        self.sprite = (7, 7)
        self.speed = 1
        
    def update(self, t):
        if (t0 % 5 == 0):
            self.y -= self.speed
        if (self.y < -5):
            self.speed = 0
        
    def draw(self):
        thumby.display.blit(self.sprite, self.x, self.y, self.width, self.width)
        
player = Player(8, 8)    
bullet = Bullet(0, -10)

doves = []
        
def newGame():
    #Make Doves
    for x in range(Dove.numberofDoves):
        doves.append(Dove(8, 8, x, 0));


newGame()

while (gameRunning):
    t0 = time.ticks_ms()   # Get time (ms)
    thumby.display.fill(0) # Fill canvas to black
    
    if (Dove.numberofDoves > 0):
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
            bullet = Bullet(round((player.tile * player.width) + player.width / 2), thumby.DISPLAY_H - player.height - 5)
        
        #Draw every bullet
        bullet.update(t0)
        bullet.draw()
        
        #Draw doves
        for d in range(len(doves)):
            if (t0 % Dove.moveDelay == 0):
                doves[d].checkWall()
            
        for d in range(len(doves)):
            if (t0 % Dove.moveDelay == 0):
                doves[d].move()
            doves[d].checkHit()
            doves[d].draw()
        
        # Draw the player sprite
        player.draw()
    else:
        thumby.display.drawText("YOU WIN", 0, 0, 1)
    
    thumby.display.update()
