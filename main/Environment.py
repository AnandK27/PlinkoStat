# Author: Navin
# Created: December 2020
# License: MIT

import sys
import time
import pygame
import random
import pymunk
from pymunk import Vec2d
import pymunk.pygame_util
from pygame.color import *
from pygame.locals import *
from pygame.locals import *
from Parameters import *
import math
import numpy as np

from pymunk.shape_filter import ShapeFilter

class Environment:
    def __init__(self):
        pass

    def initialize(self, dropSlot = 13, pinLevels = 13, numBalls = 500, values = random.choices([100, 500, 1000, 0, 10000, 0, 1000, 500, 100], k=Env.numPins -1), timeScale = 1, binDisplay = True):
        self.ballRadius = Env.ballSize
        self.pinLevels = pinLevels
        Env.numBalls = numBalls
        self.timeScale = timeScale
        pymunk.pygame_util.positive_y_is_up = False #NOTE: Pymunk physics coordinates normally start from the lower right-hand corner of the screen. This line makes it the opposite (coordinates 0,0 begin at the top left corner of the screen)
        self.screen = None
        self.draw_options = None       
        self.decimalPrecision = 2        
        self.boundaryObjects = []
        self.worldObjects = []
        self.ballObjects = []
        self.bins = []
        self.display_flags = 0          
        self.statsPos = Vec2d(15, 10)
        self.UNDETERMINED = -1
        self.highFriction = 20   
        self.iterations = 20
        self.maxBalls = Env.numBalls
        if not hasattr(self, 'gamePaused'):
            self.gamePaused = False
        Env.dropSlot = dropSlot
        Env.pinStartY =  max(int(Env.pinEndY - (self.pinLevels)* Env.pinHeightGap), int(Env.pinEndY - 13 * Env.pinHeightGap))
        Env.ballReleaseX = Env.worldX + Env.boundaryThickness + Env.pinWidthGap*(Env.dropSlot - 0.5) - 0.5
        self.count = [0] * Env.numPins
        self.values = values
        self.space = pymunk.Space()
        self.space.gravity = (0.0, 1900.0)
        self.fps = 60 #frames per second
        #self.space.damping = 0.999 
        self.infoString = [""] * (Env.numPins - 1)
        self.binHeight = self.makeBinomialCombs(Env.dropSlot)
        self.calcExpectedValue()
        self.createOuterBoundary()
        self.createSlots()
        self.createPins()
        self.binDisplay = binDisplay
        print(self.expectedValues[Env.dropSlot -1 ])
        print(np.argmax(self.expectedValues))
        self.sampleExpectedValue = 0

      
        
        pygame.init()
        pygame.mixer.quit()#disable sound output that causes annoying sound effects if any other external music player is playing
        self.screen = pygame.display.set_mode((Env.screenWidth, Env.screenHeight), self.display_flags)
        self.font = pygame.font.SysFont("poppins", 20)
        #width, height = self.screen.get_size()
        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)
        self.draw_options.constraint_color = 140, 140, 140              
        #self.draw_options.flags = pymunk.SpaceDebugDrawOptions.DRAW_SHAPES        
        self.draw_options.flags ^= pymunk.SpaceDebugDrawOptions.DRAW_COLLISION_POINTS #turn off the collision points.
        
    def createOuterBoundary(self):              
        self.createStaticBox(Env.worldX+Env.screenWidth/2, Env.worldY+Env.boundaryThickness/2, Env.screenWidth, Env.boundaryThickness, Env.boundaryColor)#top boundary
        self.createStaticBox(Env.worldX+Env.screenWidth/2, Env.worldY+Env.screenHeight-Env.boundaryThickness/2, Env.screenWidth, Env.boundaryThickness, Env.boundaryColor)#bottom boundary
        self.createStaticBox(Env.worldX+Env.boundaryThickness/2, Env.worldY+Env.screenHeight/2, Env.boundaryThickness, Env.screenHeight-(2*Env.boundaryThickness), Env.boundaryColor)#left boundary
        self.createStaticBox(Env.worldX+Env.screenWidth-Env.boundaryThickness/2, Env.worldY+Env.screenHeight/2, Env.boundaryThickness, Env.screenHeight-(2*Env.boundaryThickness), Env.boundaryColor)#right boundary
    
    def createSlots(self):
        slotY = Env.screenHeight - Env.slotHeight/2 - Env.boundaryThickness
        slotStartX = int(Env.worldX + Env.boundaryThickness + Env.pinWidthGap)
        for slotX in range(slotStartX, Env.screenWidth, Env.pinWidthGap):
            self.createStaticBox(slotX, slotY, Env.slotThickness, Env.slotHeight, Env.slotColor)
    
    def createPins(self):
        # slotStartY = Env.screenHeight - Env.slotHeight - Env.boundaryThickness
        # slotStartY = slotStartY - Env.boundaryThickness
        pinEndY = Env.pinEndY
        pinStartY = int(Env.worldY + Env.boundaryThickness + Env.pinStartY)
        pinStartX = int(Env.worldX + Env.boundaryThickness + Env.pinWidthGap/ 2)
        pinIncr = int(Env.pinWidthGap / 2)
        alternate = False
        for pinY in range(pinStartY, int(pinEndY), Env.pinHeightGap):                    
            if alternate: 
                pinStartX = pinStartX + pinIncr
                alternate = False
            else: 
                pinStartX = pinStartX - pinIncr
                alternate = True

            for pinX in range(pinStartX, int(pinStartX + Env.pinWidthGap * Env.numPins - (1-alternate)*Env.pinWidthGap), Env.pinWidthGap):
                self.createStaticSphere(pinX, pinY, Env.pinRadius, Env.pinColor)#top boundary        
                
        
    def createStaticBox(self, x, y, wd, ht, color):
        body = pymunk.Body(body_type = pymunk.Body.KINEMATIC)
        body.position = Vec2d(x, y)
        body.width = wd
        body.height = ht
        shape = pymunk.Poly.create_box(body, (wd, ht))
        shape.color = color
        shape.friction = 0
        shape.elasticity = 0.5
        self.space.add(body, shape)
        self.worldObjects.append(shape)  
        
    def createStaticSphere(self, xPosition, yPosition, radius, color):
        sphereMass = 5000
        sphereInertia = pymunk.moment_for_circle(sphereMass, 0, radius, (0, 0))
        body = pymunk.Body(sphereMass, sphereInertia, body_type=pymunk.Body.KINEMATIC)
        #x = random.randint(115, 350)
        body.position = xPosition, yPosition
        shape = pymunk.Circle(body, radius, (0, 0))
        shape.elasticity = 0.45 + (random.random()-0.5)*0.1  #range 0 to 9
        shape.friction = 0
        shape.color = color
        self.space.add(body, shape)
        self.worldObjects.append(shape)
        
    def createDynamicBall(self, xPosition, yPosition, radius, color):
        sphereMass = 5000
        sphereInertia = pymunk.moment_for_circle(sphereMass, 0, radius, (0, 0))
        body = pymunk.Body(sphereMass, sphereInertia, body_type=pymunk.Body.DYNAMIC)
        body.position = xPosition, yPosition
        shape = pymunk.Circle(body, radius, (0, 0))
        shape.elasticity = 0.65 + (random.random()-0.5)*0.1  #range 0 to 9
        shape.friction = 0
        shape.color = color
        shape.filter = ShapeFilter(group = 1)
        self.space.add(body, shape)
        self.ballObjects.append(shape)

    def createBin(self, x, y, wd, ht, color):
        rect_surf = pygame.Surface(pygame.Rect(x, y, wd, ht).size, pygame.SRCALPHA)
        pygame.draw.rect(rect_surf, color, rect_surf.get_rect())
        self.screen.blit(rect_surf, (x, y))

    def makeBinomialCombs(self, dropSlot):
        combs = [math.comb(self.pinLevels - 1,i) for i in range(self.pinLevels)]
        binHeight = [0.0] * (Env.numPins - 1)
        drop = dropSlot - self.pinLevels//2 - 1
        for i, x in enumerate(combs):
            if drop + i >= 0 and drop + i < Env.numPins - 1:
                binHeight[drop  + i] += x
            elif dropSlot - self.pinLevels//2 + i < 0:
                binHeight[-(drop + i) - 1] += x
            elif dropSlot - self.pinLevels//2 + i >= Env.numPins - 1:
                binHeight[2*(Env.numPins -1)  - (drop + i) - 1] += x
        binHeight = [float(i)/sum(binHeight) for i in binHeight]
        return binHeight

    def calcExpectedValue(self):
        self.expectedValues = [0] * (Env.numPins - 1)
        for j in range(len(self.expectedValues)):
            binHeight = self.makeBinomialCombs(j + 1)
            for i in range(len(self.values)):
                self.expectedValues[j] += self.values[i] * binHeight[i]
        pass


    def draw(self):        
        #self.screen.fill(THECOLORS["black"])# Clear screen
        self.screen.fill((30, 30, 30))# Clear screen  
        self.space.debug_draw(self.draw_options)# Draw space
        self.displayStats()
        self.displayBins()        
        pygame.display.flip()#flip the display buffer

    def displayBins(self):
        if self.binDisplay == False:
            return
        binStartX = int(Env.worldX + Env.boundaryThickness)
        binEndX = int(Env.screenHeight - Env.boundaryThickness- Env.pinWidthGap)
        for i, binX in enumerate(range(binStartX, binEndX, Env.pinWidthGap)):
            self.createBin(binX, Env.screenHeight -(0.9 * Env.slotHeight * self.binHeight[i]/max(self.binHeight)) - Env.boundaryThickness, Env.pinWidthGap, 0.9 * Env.slotHeight * self.binHeight[i]/max(self.binHeight), [144, 238, 144, 100])
        pass

    def displayStats(self):
        self.screen.blit(self.font.render(self.infoString[0], 1, THECOLORS["gray"]), self.statsPos)
        self.screen.blit(self.font.render(f'Sample Expected Value: {self.sampleExpectedValue:.2f}' , 1, THECOLORS["gray"]), self.statsPos + (0, 20))
        self.screen.blit(self.font.render(f'Expected Value: {self.expectedValues[Env.dropSlot -1 ]:.2f} | Best Slot: {np.argmax(self.expectedValues)}' , 1, THECOLORS["gray"]), self.statsPos + (0, 40))
        for i in range(1,len(self.infoString)):
            self.screen.blit(self.font.render(self.infoString[i], 1, THECOLORS["gray"]), self.statsPos+((Env.worldX + Env.boundaryThickness + Env.pinWidthGap*(i-1)) , Env.screenHeight - Env.slotHeight - Env.boundaryThickness))
            if i-1 < len(self.values):
                text = self.font.render(str(self.values[i-1]), 1, THECOLORS["lightblue"]) 
                text = pygame.transform.rotate(text, 90)
                self.screen.blit(text, self.statsPos+((Env.worldX + Env.boundaryThickness + Env.pinWidthGap*(i-1.25)) , Env.screenHeight - Env.slotHeight - Env.boundaryThickness + 40))

    def runWorld(self): 
        clock = pygame.time.Clock()  
        self.prevTime = time.time()    
        while True:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key in (K_q, K_ESCAPE)):
                    sys.exit(0)
                elif event.type == KEYDOWN and event.key == K_p:
                    self.gamePaused = not self.gamePaused
                elif event.type == KEYDOWN and event.key == K_r:
                    self.initialize()
                    self.draw()
                elif event.type == KEYDOWN and event.key == K_w:
                    #speed up
                    self.timeScale = min(3, self.timeScale*1.25)
                elif event.type == KEYDOWN and event.key == K_s:
                    #slow down
                    self.timeScale = max(0.5, self.timeScale/1.25)
            if self.gamePaused:
                self.prevTime = time.time()
                continue
            #---Update physics
            dt = 1.0 / float(self.fps) / float(self.iterations)
            for _ in range(self.iterations): #iterations to get a more stable simulation
                self.space.step(dt)
            #---Create new ball            
            if self.maxBalls > 0 and time.time() - self.prevTime > Env.ballCreationInterval_seconds/self.timeScale:
                self.createDynamicBall(Env.ballReleaseX + random.random(), Env.ballReleaseY, self.ballRadius, Env.ballColor)
                self.maxBalls = self.maxBalls - 1
                self.infoString[0] = "Number of balls: " + str(self.maxBalls)
                self.prevTime = time.time()

            if self.maxBalls == 0 and sum(self.count) == Env.numBalls and time.time() - self.prevTime > Env.waitTimeToEndSimulation_seconds: 
                self.prevTime = time.time()
                self.gamePaused = True

            if self.ballObjects:
                self.count = [0] * (Env.numPins- 1)
                for i in self.ballObjects:
                    if i.body.position.y > Env.screenHeight - Env.slotHeight - Env.boundaryThickness:
                        self.count[int((i.body.position.x - Env.boundaryThickness)/Env.pinWidthGap)] += 1
                self.infoString[1:] = [str(self.count[i]) for i in range(0,len(self.count))]
                self.sampleExpectedValue = self.calcSampleExpectedValue()
            self.draw()
            
            clock.tick(self.fps*self.timeScale)

    def calcSampleExpectedValue(self):
        if Env.numBalls - self.maxBalls == 0:
            return 0
        sampleExpectedValue = 0
        for i in range(len(self.count)):
            sampleExpectedValue += self.count[i] * self.values[i]
        return sampleExpectedValue/(Env.numBalls - self.maxBalls)
                                              
