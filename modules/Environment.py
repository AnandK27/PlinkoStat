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
from modules.Parameters import *
import math
import numpy as np
import pygame_gui

from pygame_gui.core import ObjectID
from pygame_gui.core.interfaces import IContainerLikeInterface, IUIManagerInterface
from pygame_gui.core import UIElement
from pygame_gui.elements.ui_status_bar import UIStatusBar

from typing import Union, Dict, Optional


class UIProgressBar(UIStatusBar):
    """
    A UI that will display a progress bar from 0 to 100%

    :param relative_rect: The rectangle that defines the size and position of the progress bar.
    :param manager: The UIManager that manages this element. If not provided or set to None,
                    it will try to use the first UIManager that was created by your application.
    :param container: The container that this element is within. If not provided or set to None
                      will be the root window's container.
    :param parent_element: The element this element 'belongs to' in the theming hierarchy.
    :param object_id: A custom defined ID for fine tuning of theming.
    :param anchors: A dictionary describing what this element's relative_rect is relative to.
    :param visible: Whether the element is visible by default. Warning - container visibility
                    may override this.
    """
    element_id = 'progress_bar'

    def __init__(self,
                 relative_rect: pygame.Rect,
                 manager: Optional[IUIManagerInterface] = None,
                 container: Optional[IContainerLikeInterface] = None,
                 parent_element: Optional[UIElement] = None,
                 object_id: Optional[Union[ObjectID, str, ]] = None,
                 anchors: Optional[Dict[str, Union[str, UIElement]]] = None,
                 visible: int = 1, max_val = 300.0):

        self.current_progress = 0.0
        self.maximum_progress = 100.0
        self.max_val = max_val

        super().__init__(relative_rect=relative_rect,
                         manager=manager,
                         container=container,
                         parent_element=parent_element,
                         object_id=object_id,
                         anchors=anchors,
                         visible=visible)

    @property
    def progress_percentage(self):
        return self.current_progress / self.maximum_progress

    def status_text(self):
        """ Subclass and override this method to change what text is displayed, or to suppress the text. """
        return f"Number of Balls: {self.current_progress * self.max_val:.0f}"

    def set_current_progress(self, progress: float):
        # Now that we subclass UIStatusBar, set_current_progress() and self.current_progress are mostly here for backward compatibility.
        self.current_progress = progress

        # Setting this triggers updating if necessary.
        self.percent_full = progress


class Environment:

    '''
    This class contains all the parameters for the simulation environment.

    Attributes:
        numBalls (int): Number of balls to be released in the simulation.
        pinLevels (int): Number of levels of pins.
        dropSlot (int): Slot where the ball is dropped.
        values (list): Values of each slot.
        timeScale (float): Speed of the simulation.

    Examples:
        >>> env = Environment()
        >>> env.initialize()
        >>> env.runWorld()
    '''
    def __init__(self):

        ''' 
        This function initializes the entire pygame environment.

        Parameters:
            None

        Returns:
            None
        '''

        #initialize pygame
        self.display_flags = 0 
        pygame.init()
        pygame.mixer.quit()#disable sound output that causes annoying sound effects if any other external music player is playing
        self.screen = pygame.display.set_mode((Env.screenWidth, Env.screenHeight), self.display_flags)
        pygame.display.set_caption("PlinkoStat: Statics of a Plinko Board")
        pygame_icon = pygame.image.load('themes/images/icon.png')
        pygame.display.set_icon(pygame_icon)

        self.font = pygame.font.SysFont("poppins", 16)
        self.fontTitle = pygame.font.SysFont("poppins", 30, bold=True)
        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)
        self.draw_options.constraint_color = 140, 140, 140  

        
        #initialize pygame_gui elements

        self.Manager = pygame_gui.UIManager((400, Env.screenHeight), theme_path= 'themes/light_theme.json')
        self.Manager2 = pygame_gui.UIManager((Env.screenWidth, Env.screenHeight), theme_path='themes/light_theme.json')
        
        relative_rect = pygame.Rect((20, 20), (30, 30))
        relative_rect.topright = (-20, 28)
        self.themeButton = pygame_gui.elements.UIButton(relative_rect=relative_rect,
                                            text='',
                                            manager=self.Manager, anchors={'top': 'top', 'right' : 'right'}, object_id='#theme_button')

        self.slotText = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((0, 60), (200, 50)),
                                            text='Select Slot to Drop Ball',
                                            manager=self.Manager, anchors={'centerx' : 'centerx'})
        self.slotInput = pygame_gui.elements.UIDropDownMenu(relative_rect=pygame.Rect((0, -10), (70, 30)), options_list=[str(i) for i in range(1, Env.numPins)], starting_option=str(8),
                                            manager=self.Manager , anchors={'top': 'top', 'top_target' : self.slotText, 'centerx' : 'centerx'})
        
        self.levelText = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((0, 10), (200, 50)),
                                            text='Select Number of Levels',
                                            manager=self.Manager, anchors={'top': 'top', 'top_target' : self.slotInput, 'centerx' : 'centerx'})
        
        self.levelInput = pygame_gui.elements.UIDropDownMenu(relative_rect=pygame.Rect((0, -10), (70, 30)), options_list=[str(i) for i in range(3, 14) if i%2 == 1], starting_option=str(13),
                                            manager=self.Manager , anchors={'top': 'top', 'top_target' : self.levelText, 'centerx' : 'centerx'})
        
        self.numBallsText = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((0, 10), (200, 50)),
                                            text='Select Number of Balls',
                                            manager=self.Manager, anchors={'top': 'top', 'top_target' : self.levelInput, 'centerx' : 'centerx'})
        
        self.numBallsInput = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((0, -10), (200, 30)), value_range=(200, 700), start_value=300,
                                            manager=self.Manager , anchors={'top': 'top', 'top_target' : self.numBallsText, 'centerx' : 'centerx'})
        self.numBallsNumber = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((0, -10), (200, 50)), text='300', manager=self.Manager, anchors={'top': 'top', 'top_target' : self.numBallsInput, 'centerx' : 'centerx'})
        
        #enter the values for the slots
        self.valuesText = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((0, -10), (350, 50)),
                                            text='Enter Values for Slots: ',
                                            manager=self.Manager, anchors={'top': 'top', 'top_target' : self.numBallsNumber, 'centerx' : 'centerx'})
        
        self.valuesTextDisclaimer = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((0, -30), (350, 50)),
                                            text='(comma separated; max 15)',
                                            manager=self.Manager, anchors={'top': 'top', 'top_target' : self.valuesText, 'centerx' : 'centerx'})
        
        self.valuesInput = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((0, -10), (200, 30)), manager=self.Manager, anchors={'top': 'top', 'top_target' : self.valuesTextDisclaimer, 'centerx' : 'centerx'})

        self.showBins = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 20), (200, 50)),
                                            text='Hide Binomial Plot',
                                            manager=self.Manager, anchors={'top': 'top',  'top_target' : self.valuesInput, 'centerx' : 'centerx'})
        
        self.startButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((220, 20), (100, 50)),
                                            text='Start',
                                            manager=self.Manager, anchors={'top': 'top',  'top_target' : self.showBins})
        
       
        self.pauseButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((80, 20), (100, 50)),
                                            text='Pause',
                                            manager=self.Manager, anchors={'top': 'top',  'top_target' : self.showBins})
        
        self.fastButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((220, 20), (150, 50)),
                                            text='Fast Forward >>',
                                            manager=self.Manager, anchors={'top': 'top',  'top_target' : self.startButton})
        
        self.speedText = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((0, 20), (350, 50)),
                                            text='1x',
                                            manager=self.Manager, anchors={'top': 'top', 'top_target' : self.pauseButton, 'centerx' : 'centerx'})
        
        self.slowButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((30, 20), (150, 50)),
                                            text=' << Slow Down',
                                            manager=self.Manager, anchors={'top': 'top',  'top_target' : self.startButton})
        
        self.plotButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 20), (150, 50)),
                                            text='Plot',
                                            manager=self.Manager, anchors={'top': 'top',  'top_target' : self.slowButton, 'centerx' : 'centerx'})
        self.plotButton.disable()
        

    def initialize(self, dropSlot = 8, pinLevels = 13, numBalls = 300,\
                   values = random.choices([100, 500, 1000, 0, 10000, 0, 1000, 500, 100], k=Env.numPins -1), timeScale = 1):
        '''
        This function initializes the simulation environment.

        Parameters:
            dropSlot (int): Slot where the ball is dropped.
            pinLevels (int): Number of levels of pins.
            numBalls (int): Number of balls to be released in the simulation.
            values (list): Values of each slot.
            timeScale (float): Speed of the simulation.

        Returns:
            None
        '''
        self.setTheme()
        self.plotButton.disable()
        self.ballRadius = Env.ballSize
        self.pinLevels = pinLevels
        Env.numBalls = numBalls
        if not hasattr(self, 'timescale'):
            self.timeScale = timeScale

        pymunk.pygame_util.positive_y_is_up = False #NOTE: Pymunk physics coordinates normally start from the lower right-hand corner of the screen. This line makes it the opposite (coordinates 0,0 begin at the top left corner of the screen)      
        self.boundaryObjects = []
        self.worldObjects = []
        self.ballObjects = []
        self.pinObjects = []
        self.bins = []         
        self.statsPos = Vec2d(10 + Env.worldX, 10 + Env.worldY)
        self.iterations = 20
        self.maxBalls = Env.numBalls
        if not hasattr(self, 'gamePaused'):
            self.gamePaused = False
        if self.gamePaused:
            self.pauseButton.set_text("Resume")
        else:
            self.pauseButton.set_text("Pause")
        Env.dropSlot = dropSlot
        Env.pinStartY =  max(int(Env.pinEndY - (self.pinLevels)* Env.pinHeightGap), int(Env.pinEndY - 13 * Env.pinHeightGap))
        Env.ballReleaseX = Env.worldX + Env.boundaryThickness + Env.pinWidthGap*(Env.dropSlot - 0.5) - 0.5
        self.count = [0] * Env.numPins
        self.values = values
        self.space = pymunk.Space()
        self.space.gravity = (0.0, 1900.0)
        self.fps = 60 #frames per second
        self.infoString = [""] * (Env.numPins - 1)
        self.binHeight = self.makeBinomialCombs(Env.dropSlot)
        self.calcExpectedValue()
        self.createOuterBoundary()
        self.createSlots()
        self.createPins()
        self.binDisplay = True
        self.sampleExpectedValue = 0
        self.timeListSampleExpectedValue = []


        self.progress_bar = UIProgressBar(relative_rect=pygame.Rect((Env.screenWidth - 220 - Env.boundaryThickness, 20), (200, 30)), manager=self.Manager2, max_val = Env.numBalls)

        print(self.expectedValues[Env.dropSlot -1 ])
        print(np.argmax(self.expectedValues))
        print(len(self.binHeight))
        
    def setTheme(self, dark_theme=True):
        '''
        This function sets the theme of the simulation environment.

        Parameters:
            dark_theme (bool): If True, sets the dark theme. If False, sets the light theme.

        Returns:
            None
        '''

        if dark_theme:
            self.Theme = DarkTheme

            self.Manager.get_theme().load_theme('themes/dark_theme.json')
            self.Manager.ui_theme.need_to_rebuild_data_manually_changed = True
            self.Manager2.get_theme().load_theme('themes/dark_theme.json')
            self.Manager2.ui_theme.need_to_rebuild_data_manually_changed = True
        else:
            self.Theme = LightTheme
            self.Manager.get_theme().load_theme('themes/light_theme.json')
            self.Manager.ui_theme.need_to_rebuild_data_manually_changed = True
            self.Manager2.get_theme().load_theme('themes/light_theme.json')
            self.Manager2.ui_theme.need_to_rebuild_data_manually_changed = True
        

        
    def createOuterBoundary(self):   
        '''
        This function creates the outer boundary of the simulation environment.

        Parameters:
            None

        Returns:
            None
        '''           
        self.createStaticBox(Env.worldX+Env.screenGameWidth/2, Env.worldY+Env.boundaryThickness/2, Env.screenGameWidth, Env.boundaryThickness, self.Theme.boundaryColor)#top boundary
        self.createStaticBox(Env.worldX+Env.screenGameWidth/2, Env.worldY+Env.screenHeight-Env.boundaryThickness/2, Env.screenGameWidth, Env.boundaryThickness, self.Theme.boundaryColor)#bottom boundary
        self.createStaticBox(Env.worldX+Env.boundaryThickness/2, Env.worldY+Env.screenHeight/2, Env.boundaryThickness, Env.screenHeight-(2*Env.boundaryThickness), self.Theme.boundaryColor)#left boundary
        self.createStaticBox(Env.worldX+Env.screenGameWidth-Env.boundaryThickness/2, Env.worldY+Env.screenHeight/2, Env.boundaryThickness, Env.screenHeight-(2*Env.boundaryThickness), self.Theme.boundaryColor)#right boundary
    
    def createSlots(self):
        '''
        This function creates the slots of the simulation environment.

        Parameters:
            None

        Returns:
            None
        '''
        slotY = Env.screenHeight - Env.slotHeight/2 - Env.boundaryThickness
        slotStartX = int(Env.worldX + Env.boundaryThickness + Env.pinWidthGap)
        for slotX in range(slotStartX, Env.worldX + Env.screenGameWidth, Env.pinWidthGap):
            self.createStaticBox(slotX, slotY, Env.slotThickness, Env.slotHeight, self.Theme.slotColor)
    
    def createPins(self):
        '''
        This function creates the pins of the simulation environment.

        Parameters:
            None

        Returns:
            None
        '''
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
                self.createStaticSphere(pinX, pinY, Env.pinRadius, self.Theme.pinColor)#top boundary        
                
        
    def createStaticBox(self, x, y, wd, ht, color):
        '''
        This function creates a static box in the simulation environment.

        Parameters:
            x (int): x-coordinate of the box.
            y (int): y-coordinate of the box.
            wd (int): Width of the box.
            ht (int): Height of the box.
            color (list): Color of the box.

        Returns:
            None
        '''
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
        '''
        This function creates a static sphere in the simulation environment.

        Parameters:
            xPosition (int): x-coordinate of the sphere.
            yPosition (int): y-coordinate of the sphere.
            radius (int): Radius of the sphere.
            color (list): Color of the sphere.

        Returns:
            None
        '''
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
        self.pinObjects.append(shape)
        
    def createDynamicBall(self, xPosition, yPosition, radius, color):
        '''
        This function creates a dynamic sphere in the simulation environment.

        Parameters:
            xPosition (int): x-coordinate of the sphere.
            yPosition (int): y-coordinate of the sphere.
            radius (int): Radius of the sphere.
            color (list): Color of the sphere.

        Returns:
            None
        '''
        sphereMass = 5000
        sphereInertia = pymunk.moment_for_circle(sphereMass, 0, radius, (0, 0))
        body = pymunk.Body(sphereMass, sphereInertia, body_type=pymunk.Body.DYNAMIC)
        body.position = xPosition, yPosition
        shape = pymunk.Circle(body, radius, (0, 0))
        shape.elasticity = 0.65 + (random.random()-0.5)*0.1  #range 0 to 9
        shape.friction = 0
        shape.color = color
        self.space.add(body, shape)
        self.ballObjects.append(shape)

    def createBin(self, x, y, wd, ht, color):
        '''
        This function creates a bin in the simulation environment.

        Parameters:
            x (int): x-coordinate of the bin.
            y (int): y-coordinate of the bin.
            wd (int): Width of the bin.
            ht (int): Height of the bin.
            color (list): Color of the bin.

        Returns:
            None
        '''
        rect_surf = pygame.Surface(pygame.Rect(x, y, wd, ht).size, pygame.SRCALPHA)
        pygame.draw.rect(rect_surf, color, rect_surf.get_rect())
        self.screen.blit(rect_surf, (x, y))


    def makeBinomialCombs(self, dropSlot):
        '''
        This function creates the binomial distribution of the simulation environment.

        Parameters:
            dropSlot (int): Slot where the ball is dropped.

        Returns:
            None
        '''
        combs = [math.comb(self.pinLevels - 1,i) for i in range(self.pinLevels)]
        binHeight = [0.0] * (Env.numPins - 1)
        drop = dropSlot - self.pinLevels//2 - 1
        for i, x in enumerate(combs):
            if drop + i >= 0 and drop + i < Env.numPins - 1:
                binHeight[drop + i] += x
            elif drop + i < 0:
                binHeight[-(drop + i) - 1] += x
            elif drop + i >= Env.numPins - 1:
                binHeight[2*(Env.numPins -1)  - (drop + i) - 1] += x
        binHeight = [float(i)/sum(binHeight) for i in binHeight]
        return binHeight

    def calcExpectedValue(self):
        '''
        This function calculates the expected value of each slot.

        Parameters:
            None

        Returns:
            None
        '''
        self.expectedValues = [0] * (Env.numPins - 1)
        for j in range(len(self.expectedValues)):
            binHeight = self.makeBinomialCombs(j + 1)
            for i in range(len(self.values)):
                self.expectedValues[j] += self.values[i] * binHeight[i]
        pass

    def drawBall(self):
        '''
        This function draws the balls in the simulation environment.

        Parameters:
            None

        Returns:
            None
        '''
        for ball in self.ballObjects:
            body = ball.body
            v = body.position + ball.offset.cpvrotate(body.rotation_vector)
            p = v
            r = ball.radius
            pygame.draw.circle(self.screen, self.Theme.ballColor, p, int(r))
    
    def drawPins(self):
        '''
        This function draws the pins in the simulation environment.

        Parameters:
            None

        Returns:
            None
        '''

        for ball in self.pinObjects:
            body = ball.body
            v = body.position + ball.offset.cpvrotate(body.rotation_vector)
            p = v
            r = ball.radius
            pygame.draw.circle(self.screen, self.Theme.pinColor, p, int(r))

    def drawBoxes(self):
        '''
        This function draws the boxes in the simulation environment.

        Parameters:
            None

        Returns:
            None
        '''
        for poly in self.worldObjects:
            body = poly.body
            ps = [p.rotated(body.angle) + body.position for p in poly.get_vertices()]
            ps.append(ps[0])
            pygame.draw.polygon(self.screen, self.Theme.boundaryColor, ps)


    def draw(self):        
        '''
        This function draws the simulation environment.

        Parameters:
            None

        Returns:
            None
        '''
        self.screen.fill(self.Theme.bgColor)# Clear screen

        self.drawBall()
        self.drawPins()
        self.drawBoxes()
        self.displayStats()
        self.displayBins()
        self.Manager.draw_ui(self.screen)
        self.Manager2.draw_ui(self.screen)       
        pygame.display.flip()#flip the display buffer

    def displayBins(self):
        '''
        This function displays the binomial distribution of the simulation environment.

        Parameters:
            None

        Returns:
            None
        '''
        if self.binDisplay == False:
            return
        binStartX = int(Env.worldX + Env.boundaryThickness)
        binEndX = int(Env.worldX + Env.screenHeight - Env.boundaryThickness)
        for i, binX in enumerate(range(binStartX, binEndX, Env.pinWidthGap)):
            self.createBin(binX, Env.screenHeight -(0.9 * Env.slotHeight * self.binHeight[i]/max(self.binHeight)) - Env.boundaryThickness, Env.pinWidthGap, 0.9 * Env.slotHeight * self.binHeight[i]/max(self.binHeight),self.Theme.binColor)
        pass

    def displayStats(self):
        '''
        This function displays the statistics of the simulation environment.

        Parameters:
            None

        Returns:
            None
        '''
        self.screen.blit(self.fontTitle.render( f'PlinkoStat', 1, self.Theme.titleColor), (130, 20))
        self.screen.blit(self.font.render( f'Sample Expected Value: {self.sampleExpectedValue:.2f}', 1, self.Theme.textColor), self.statsPos)
        self.screen.blit(self.font.render(f'Expected Value (slot {Env.dropSlot}): {self.expectedValues[Env.dropSlot -1 ]:.2f} | Best Slot: {np.argmax(self.expectedValues)+1}' , 1, self.Theme.textColor), self.statsPos + (0, 25))
        for i in range(1,len(self.infoString)):
            self.screen.blit(self.font.render(self.infoString[i], 1, self.Theme.textColor), ((Env.worldX + Env.boundaryThickness + Env.pinWidthGap*(i-0.5)) , Env.screenHeight - Env.slotHeight - Env.boundaryThickness))
            text = self.font.render(str(self.values[i-1]), 1, self.Theme.textHighlightColor) 
            text = pygame.transform.rotate(text, 90)
            self.screen.blit(text, self.statsPos+((Env.boundaryThickness + Env.pinWidthGap*(i-1)) , Env.screenHeight - Env.slotHeight - Env.boundaryThickness + 40))
            if i == Env.dropSlot:
                self.screen.blit(self.font.render(f'{i}' , 1, self.Theme.textHighlightColor), ((Env.worldX + Env.boundaryThickness + Env.pinWidthGap*(i-0.5)) , Env.pinStartY + Env.boundaryThickness - 30))
            else:
                self.screen.blit(self.font.render(f'{i}' , 1, self.Theme.textLightColor), ((Env.worldX + Env.boundaryThickness + Env.pinWidthGap*(i-0.5)) , Env.pinStartY + Env.boundaryThickness - 30))

    def runWorld(self):
        '''
        This function runs the simulation environment.

        Parameters:
            None

        Returns:
            None
        ''' 
        clock = pygame.time.Clock()  
        self.prevTime = time.time()
        UIRefereshRate = 15/1000.0   
        while True:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key in (K_q, K_ESCAPE)):
                    sys.exit(0)

                elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.startButton:
                        if self.valuesInput.text:
                            value_temp_list = [int(i) for i in self.valuesInput.text.split(',')]
                            if len(value_temp_list) < 15:
                                value_list = random.choices(value_temp_list, k=Env.numPins -1)
                            else:
                                value_list = value_temp_list
                        else:
                            value_list = random.choices([100, 500, 1000, 0, 10000, 0, 1000, 500, 100], k=Env.numPins -1)
                        self.initialize(int(self.slotInput.selected_option), int(self.levelInput.selected_option), int(self.numBallsNumber.text), value_list)
                        self.draw()

                    elif event.ui_element == self.pauseButton:
                        self.gamePaused = not self.gamePaused
                        if self.gamePaused:
                            self.pauseButton.set_text("Resume")
                        else:
                            self.pauseButton.set_text("Pause")

                    elif event.ui_element == self.fastButton:
                        self.timeScale = min(5, self.timeScale+0.25)
                        self.speedText.set_text(f'{self.timeScale:.2f}' + "x")

                    elif event.ui_element == self.slowButton:
                        self.timeScale = max(0.5, self.timeScale-0.25)
                        self.speedText.set_text(f'{self.timeScale:.2f}' + "x")

                    elif event.ui_element == self.plotButton:
                        import matplotlib.pyplot as plt
                        fig, ax = plt.subplots(1,2, figsize=(15,6))
                        ax1 = plt.subplot(1,2,1)
                        ax1.plot(self.timeListSampleExpectedValue, label = 'sample')
                        ax1.plot([self.expectedValues[Env.dropSlot -1 ]]*len(self.timeListSampleExpectedValue), label = 'true')
                        ax1.legend()
                        ax1.title.set_text("Comparision of Sample and True Expected Value with Time")
                        ax1.set(xlabel='Number of Balls', ylabel='Expected Value')

                        ax2 = plt.subplot(1,2,2)
                        ax2.bar(range(1, len(self.expectedValues)+1), self.expectedValues)
                        ax2.bar(np.argmax(self.expectedValues)+1, self.expectedValues[np.argmax(self.expectedValues)], label = 'best')
                        ax2.bar(Env.dropSlot, self.expectedValues[Env.dropSlot -1], label = 'chosen')
                        ax2.legend()
                        ax2.title.set_text("Comparision of Expected Values of Each Slot")
                        ax2.set(xlabel='Slot Number', ylabel='Expected Value')

                        plt.show()

                    elif event.ui_element == self.showBins:
                        self.binDisplay = not self.binDisplay
                        if self.binDisplay:
                            self.showBins.set_text("Hide Binomial Plot")
                        else:
                            self.showBins.set_text("Show Binomial Plot")

                    elif event.ui_element == self.themeButton:
                        self.setTheme(not self.Theme == DarkTheme)

                elif event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                    if event.ui_element == self.numBallsInput:
                        self.numBallsNumber.set_text(str(int(event.value)))

                self.Manager.process_events(event)

            if self.gamePaused:
                self.prevTime = time.time()
                self.Manager.update(UIRefereshRate)
                self.Manager2.update(UIRefereshRate)
                self.draw()
                clock.tick(self.fps*self.timeScale)
                continue
            #---Update physics
            dt = 1.0 / float(self.fps) / float(self.iterations)
            for _ in range(self.iterations): #iterations to get a more stable simulation
                self.space.step(dt)
            #---Create new ball            
            if self.maxBalls > 0 and time.time() - self.prevTime > Env.ballCreationInterval_seconds/self.timeScale:
                self.createDynamicBall(Env.ballReleaseX + random.random(), Env.ballReleaseY, self.ballRadius, self.Theme.ballColor)
                self.maxBalls = self.maxBalls - 1
                #self.progress_bar.set_current_progress(2)
                self.progress_bar.set_current_progress((Env.numBalls - self.maxBalls)/Env.numBalls)
                self.infoString[0] = "Number of balls: " + str(self.maxBalls)
                if self.sampleExpectedValue != 0:
                    self.timeListSampleExpectedValue.append(self.sampleExpectedValue)
                self.prevTime = time.time()

            if self.maxBalls == 0 and sum(self.count) == Env.numBalls and time.time() - self.prevTime > Env.waitTimeToEndSimulation_seconds: 
                print("Simulation ended")
                self.plotButton.enable()
                self.prevTime = time.time()
                self.gamePaused = True
                self.pauseButton.set_text("Resume")

            if self.ballObjects:
                self.count = [0] * (Env.numPins- 1)
                for i in self.ballObjects:
                    if i.body.position.y > Env.screenHeight - Env.slotHeight - Env.boundaryThickness:
                        self.count[int((i.body.position.x - Env.boundaryThickness - Env.worldX)/Env.pinWidthGap)] += 1
                self.infoString[1:] = [str(self.count[i]) for i in range(0,len(self.count))]
                self.sampleExpectedValue = self.calcSampleExpectedValue()
            self.Manager.update(UIRefereshRate)
            self.Manager2.update(UIRefereshRate)
            self.draw()
            clock.tick(self.fps*self.timeScale)

    def calcSampleExpectedValue(self):
        '''
        This function calculates the sample expected value of the simulation environment.

        Parameters:
            None

        Returns:
            None
        '''
        if Env.numBalls - self.maxBalls == 0:
            return 0
        sampleExpectedValue = 0
        for i in range(len(self.count)):
            sampleExpectedValue += self.count[i] * self.values[i]
        return sampleExpectedValue/(Env.numBalls - self.maxBalls)
                                              
