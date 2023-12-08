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

#from pymunk.shape_filter import ShapeFilter

class Environment:
    def __init__(self, ballRadius, dropSlot = 3, pinLevels = 9):
        self.ballRadius = ballRadius
        Env.dropSlot = dropSlot
        Env.ballReleaseX = Env.worldX + Env.boundaryThickness + Env.gap*(Env.dropSlot - 0.5) - 0.5
        Env.pinStartY =  max(int(Env.pinStartY + (10 -pinLevels)* Env.gap), Env.pinStartY)
        pymunk.pygame_util.positive_y_is_up = False #NOTE: Pymunk physics coordinates normally start from the lower right-hand corner of the screen. This line makes it the opposite (coordinates 0,0 begin at the top left corner of the screen)
        self.screen = None
        self.draw_options = None       
        self.decimalPrecision = 2        
        self.boundaryObjects = []
        self.worldObjects = []
        self.display_flags = 0          
        self.statsPos = Vec2d(15, 10)
        self.UNDETERMINED = -1
        self.highFriction = 20   
        self.iterations = 20
        self.maxBalls = Env.numBalls

    def initialize(self):
        self.space = pymunk.Space()
        self.space.gravity = (0.0, 1900.0)
        self.fps = 50 #frames per second
        #self.space.damping = 0.999 
        self.infoString = ""           
        self.createOuterBoundary()
        self.createSlots()
        self.createPins()        
        
        pygame.init()
        pygame.mixer.quit()#disable sound output that causes annoying sound effects if any other external music player is playing
        self.screen = pygame.display.set_mode((Env.screenWidth, Env.screenHeight), self.display_flags)
        self.font = pygame.font.SysFont("poppins", 14)
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
        slotStartX = int(Env.worldX + Env.boundaryThickness + Env.gap)
        for slotX in range(slotStartX, Env.screenWidth, Env.gap):
            self.createStaticBox(slotX, slotY, Env.slotThickness, Env.slotHeight, Env.slotColor)#top boundary
    
    def createPins(self):
        # slotStartY = Env.screenHeight - Env.slotHeight - Env.boundaryThickness
        # slotStartY = slotStartY - Env.boundaryThickness
        pinEndY = Env.pinEndY
        pinStartY = int(Env.worldY + Env.boundaryThickness + Env.pinStartY)
        pinStartX = int(Env.worldX + Env.boundaryThickness + Env.gap / 2)
        pinIncr = int(Env.gap / 2)
        alternate = False
        for pinY in range(pinStartY, int(pinEndY), Env.gap):                    
            if alternate: 
                pinStartX = pinStartX + pinIncr
                alternate = False
            else: 
                pinStartX = pinStartX - pinIncr
                alternate = True

            for pinX in range(pinStartX, int(pinStartX + Env.gap * Env.numPins - (1-alternate)*Env.gap), Env.gap):
                self.createStaticSphere(pinX, pinY, Env.pinRadius, Env.pinColor)#top boundary        
        
    def createStaticBox(self, x, y, wd, ht, colour):
        body = pymunk.Body(body_type = pymunk.Body.KINEMATIC)
        body.position = Vec2d(x, y)
        body.width = wd
        body.height = ht
        shape = pymunk.Poly.create_box(body, (wd, ht))
        shape.color = colour
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
        shape.elasticity = 0.5  #range 0 to 9
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
        shape.elasticity = 0.5
        shape.friction = 0
        shape.color = color
        self.space.add(body, shape)
        self.worldObjects.append(shape)                           

    def draw(self):        
        #self.screen.fill(THECOLORS["black"])# Clear screen
        self.screen.fill((30, 30, 30))# Clear screen  
        self.space.debug_draw(self.draw_options)# Draw space
        self.displayStats(self.infoString);        
        pygame.display.flip()#flip the display buffer

    def displayStats(self, displayStr):
        if isinstance(displayStr, str): self.screen.blit(self.font.render(displayStr, 1, THECOLORS["gray"]), self.statsPos)
        else:
            sep = 15
            for i in range(0,len(displayStr),1): self.screen.blit(self.font.render(displayStr[i], 1, THECOLORS["gray"]), self.statsPos+(0,i*sep))

    def runWorld(self): 
        runState = RunCode.CONTINUE
        clock = pygame.time.Clock()
        simulating = True    
        self.prevTime = time.time()
        countdownToEndSimulation = False     
        while simulating:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key in (K_q, K_ESCAPE)):
                    sys.exit(0)

            #---Update physics
            dt = 1.0 / float(self.fps) / float(self.iterations)
            for _ in range(self.iterations): #iterations to get a more stable simulation
                self.space.step(dt)
            #---Create new ball            
            if self.maxBalls > 0 and time.time() - self.prevTime > Env.ballCreationInterval_seconds:
                self.createDynamicBall(Env.ballReleaseX + random.random(), Env.ballReleaseY, self.ballRadius, Env.ballColor)
                self.maxBalls = self.maxBalls - 1
                self.infoString = "Number of balls: " + str(self.maxBalls)
                self.prevTime = time.time()
            if self.maxBalls == 0 and not countdownToEndSimulation: 
                countdownToEndSimulation = True
                self.prevTime = time.time()
            if countdownToEndSimulation:                
                self.infoString = "Stopping simulation in: " + str(int(Env.waitTimeToEndSimulation_seconds - (time.time() - self.prevTime)))
                if time.time() - self.prevTime > Env.waitTimeToEndSimulation_seconds:
                    runState = RunCode.STOP 
            #---draw all objects            
            self.draw()
            
            clock.tick(self.fps)
            if runState == RunCode.STOP:
                #TODO: could add code to delete objects that were created
                break  
                                              
