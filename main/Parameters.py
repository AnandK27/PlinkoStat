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
    ballReleaseX = worldX + boundaryThickness + pinWidthGap*(dropSlot - 0.5) 
    ballReleaseY = worldY + (boundaryThickness*2)
    ballCreationInterval_seconds = 0.5
    waitTimeToEndSimulation_seconds = 10

class DarkTheme:
    boundaryColor = [100,100,100,255]
    slotColor = [50,50,50, 255]
    pinColor = [70,69,73, 255]
    ballColor = THECOLORS["lightgreen"]
    binColor =  [144, 238, 144, 60]
    textColor = THECOLORS['gray']
    textLightColor = [100,100, 100, 100]
    textHighlightColor = THECOLORS['lightblue']
    bgColor = [30,30,30,255]

class LightTheme:
    boundaryColor = [150,150,150,255]
    slotColor = [150,150,150, 255]
    pinColor = [160, 190, 200, 255]
    ballColor = THECOLORS["green"]
    binColor =  [50, 238, 50, 50]
    textColor = [30,30,30, 255]
    textHighlightColor = THECOLORS['blue']
    textLightColor = [160,160,160, 50]
    bgColor = [255, 249, 242,255]

    if __name__ == "__main__":
        print(THECOLORS["gray"])