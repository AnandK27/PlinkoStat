# Author: Navin
# Created: December 2020
# License: MIT
    
class Env:
    ballSize = 5
    numBalls = 50
    numPins = 10
    boundaryThickness = 5
    gap = 40
    pinRadius = 5
    screenHeight = 800    
    screenWidth = int(gap*(numPins-0.5) - pinRadius - boundaryThickness)
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
    ballColor = [0, 180, 0, 255]
    ballReleaseX = worldX + boundaryThickness + gap*(dropSlot - 0.5) - 0.5
    ballReleaseY = worldY + (boundaryThickness*2)
    ballCreationInterval_seconds = 0.5
    waitTimeToEndSimulation_seconds = 10