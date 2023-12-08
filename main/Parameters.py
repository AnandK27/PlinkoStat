# Author: Navin
# Created: December 2020
# License: MIT

class RunCode:
    CONTINUE = 1
    STOP = 0
    
class Env:
    ballSize = 5
    screenHeight = 800    
    boundaryThickness = 5
    worldX = 0
    worldY = 0 
    slotHeight = 0.35 * screenHeight
    pinEndY = screenHeight - (boundaryThickness*2) - slotHeight
    numPins = 10
    dropSlot = 5
    gap = 40
    slotThickness = 2    
    pinStartY = 0.15 * screenHeight
    pinRadius = 5
    boundaryColor = [100,100,100,255]
    slotColor = [50,50,50, 255]
    pinColor = [70,69,73, 255]
    numBalls = 300
    ballColor = [0, 180, 0, 255]
    ballReleaseX = worldX + boundaryThickness + gap*(dropSlot - 0.5) - 0.5
    ballReleaseY = worldY + (boundaryThickness*2)
    ballCreationInterval_seconds = 0.5
    waitTimeToEndSimulation_seconds = 10
    screenWidth = int(gap*(numPins-0.5) - pinRadius - boundaryThickness)