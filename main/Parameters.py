# Author: Navin
# Created: December 2020
# License: MIT
from pygame.color import *

class Env:
    ballSize = 3
    numBalls = 50
    numPins = 16
    boundaryThickness = 5
    pinWidthGap = 50
    pinHeightGap = 30
    pinRadius = 8
    screenHeight = 800    
    screenWidth = int(pinWidthGap*(numPins-0.5) - pinRadius - boundaryThickness)
    worldX = 0
    worldY = 0 
    slotHeight = 0.35 * screenHeight
    pinEndY = screenHeight - (boundaryThickness*2) - slotHeight
    dropSlot = 5
    slotThickness = 2    
    pinStartY = 0.15 * screenHeight
    boundaryColor = [100,100,100,255]
    slotColor = [50,50,50, 255]
    pinColor = [70,69,73, 255]
    ballColor = THECOLORS["lightgreen"]
    ballReleaseX = worldX + boundaryThickness + pinWidthGap*(dropSlot - 0.5) 
    ballReleaseY = worldY + (boundaryThickness*2)
    ballCreationInterval_seconds = 0.5
    waitTimeToEndSimulation_seconds = 10

    if __name__ == "__main__":
        print(THECOLORS["lightgreen"])