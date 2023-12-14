# modules package

## Submodules

## modules.Environment module

### *class* modules.Environment.Environment

Bases: `object`

This class contains all the parameters for the simulation environment.

#### numBalls

Number of balls to be released in the simulation.
* **Type:**
  int

#### pinLevels

Number of levels of pins.
* **Type:**
  int

#### dropSlot

Slot where the ball is dropped.
* **Type:**
  int

#### values

Values of each slot.
* **Type:**
  list

#### timeScale

Speed of the simulation.
* **Type:**
  float

### Examples

```pycon
env = Environment()
env.initialize()
env.runWorld()
```

#### \_\_init_\_()

This function initializes the entire pygame environment.
* **Parameters:**
  **None** – 
* **Returns:**
  None

#### calcExpectedValue()

This function calculates the expected value of each slot.
* **Parameters:**
  **None** – 
* **Returns:**
  None

#### calcSampleExpectedValue()

This function calculates the sample expected value of the simulation environment.
* **Parameters:**
  **None** – 
* **Returns:**
  None

#### createBin(x, y, wd, ht, color)

This function creates a bin in the simulation environment.
* **Parameters:**
  * **x** (*int*) – x-coordinate of the bin.
  * **y** (*int*) – y-coordinate of the bin.
  * **wd** (*int*) – Width of the bin.
  * **ht** (*int*) – Height of the bin.
  * **color** (*list*) – Color of the bin.
* **Returns:**
  None

#### createDynamicBall(xPosition, yPosition, radius, color)

This function creates a dynamic sphere in the simulation environment.
* **Parameters:**
  * **xPosition** (*int*) – x-coordinate of the sphere.
  * **yPosition** (*int*) – y-coordinate of the sphere.
  * **radius** (*int*) – Radius of the sphere.
  * **color** (*list*) – Color of the sphere.
* **Returns:**
  None

#### createOuterBoundary()

This function creates the outer boundary of the simulation environment.
* **Parameters:**
  **None** – 
* **Returns:**
  None

#### createPins()

This function creates the pins of the simulation environment.
* **Parameters:**
  **None** – 
* **Returns:**
  None

#### createSlots()

This function creates the slots of the simulation environment.
* **Parameters:**
  **None** – 
* **Returns:**
  None

#### createStaticBox(x, y, wd, ht, color)

This function creates a static box in the simulation environment.
* **Parameters:**
  * **x** (*int*) – x-coordinate of the box.
  * **y** (*int*) – y-coordinate of the box.
  * **wd** (*int*) – Width of the box.
  * **ht** (*int*) – Height of the box.
  * **color** (*list*) – Color of the box.
* **Returns:**
  None

#### createStaticSphere(xPosition, yPosition, radius, color)

This function creates a static sphere in the simulation environment.
* **Parameters:**
  * **xPosition** (*int*) – x-coordinate of the sphere.
  * **yPosition** (*int*) – y-coordinate of the sphere.
  * **radius** (*int*) – Radius of the sphere.
  * **color** (*list*) – Color of the sphere.
* **Returns:**
  None

#### displayBins()

This function displays the binomial distribution of the simulation environment.
* **Parameters:**
  **None** – 
* **Returns:**
  None

#### displayStats()

This function displays the statistics of the simulation environment.
* **Parameters:**
  **None** – 
* **Returns:**
  None

#### draw()

This function draws the simulation environment.
* **Parameters:**
  **None** – 
* **Returns:**
  None

#### drawBall()

This function draws the balls in the simulation environment.
* **Parameters:**
  **None** – 
* **Returns:**
  None

#### drawBoxes()

This function draws the boxes in the simulation environment.
* **Parameters:**
  **None** – 
* **Returns:**
  None

#### drawPins()

This function draws the pins in the simulation environment.
* **Parameters:**
  **None** – 
* **Returns:**
  None

#### initialize(dropSlot=8, pinLevels=13, numBalls=300, values=[100, 1000, 500, 10000, 1000, 10000, 1000, 100, 1000, 0, 500, 1000, 0, 100, 0], timeScale=1)

This function initializes the simulation environment.
* **Parameters:**
  * **dropSlot** (*int*) – Slot where the ball is dropped.
  * **pinLevels** (*int*) – Number of levels of pins.
  * **numBalls** (*int*) – Number of balls to be released in the simulation.
  * **values** (*list*) – Values of each slot.
  * **timeScale** (*float*) – Speed of the simulation.
* **Returns:**
  None

#### makeBinomialCombs(dropSlot)

This function creates the binomial distribution of the simulation environment.
* **Parameters:**
  **dropSlot** (*int*) – Slot where the ball is dropped.
* **Returns:**
  None

#### runWorld()

This function runs the simulation environment.
* **Parameters:**
  **None** – 
* **Returns:**
  None

#### setTheme(dark_theme=True)

This function sets the theme of the simulation environment.
* **Parameters:**
  **dark_theme** (*bool*) – If True, sets the dark theme. If False, sets the light theme.
* **Returns:**
  None

### *class* modules.Environment.UIProgressBar(relative_rect: Rect, manager: IUIManagerInterface | None = None, container: IContainerLikeInterface | None = None, parent_element: UIElement | None = None, object_id: ObjectID | str | None = None, anchors: Dict[str, str | UIElement] | None = None, visible: int = 1, max_val=300.0)

Bases: `UIStatusBar`

A UI that will display a progress bar from 0 to 100%
* **Parameters:**
  * **relative_rect** – The rectangle that defines the size and position of the progress bar.
  * **manager** – The UIManager that manages this element. If not provided or set to None,
    it will try to use the first UIManager that was created by your application.
  * **container** – The container that this element is within. If not provided or set to None
    will be the root window’s container.
  * **parent_element** – The element this element ‘belongs to’ in the theming hierarchy.
  * **object_id** – A custom defined ID for fine tuning of theming.
  * **anchors** – A dictionary describing what this element’s relative_rect is relative to.
  * **visible** – Whether the element is visible by default. Warning - container visibility
    may override this.

#### \_\_init_\_(relative_rect: Rect, manager: IUIManagerInterface | None = None, container: IContainerLikeInterface | None = None, parent_element: UIElement | None = None, object_id: ObjectID | str | None = None, anchors: Dict[str, str | UIElement] | None = None, visible: int = 1, max_val=300.0)

#### element_id *= 'progress_bar'*

#### *property* progress_percentage

#### set_current_progress(progress: float)

#### status_text()

Subclass and override this method to change what text is displayed, or to suppress the text.

## modules.Parameters module

### *class* modules.Parameters.DarkTheme

Bases: `object`

This class contains all the colors for the dark theme.

#### ballColor *= (144, 238, 144, 255)*

#### bgColor *= [30, 30, 30, 255]*

#### binColor *= [144, 238, 144, 60]*

#### boundaryColor *= [100, 100, 100, 255]*

#### pinColor *= [70, 69, 73, 255]*

#### slotColor *= [50, 50, 50, 255]*

#### textColor *= (190, 190, 190, 255)*

#### textHighlightColor *= (173, 216, 230, 255)*

#### textLightColor *= [100, 100, 100, 100]*

#### titleColor *= [144, 238, 144, 255]*

### *class* modules.Parameters.Env

Bases: `object`

This class contains all the parameters for the simulation environment.

#### ballCreationInterval_seconds *= 0.5*

#### ballReleaseX *= 630.0*

#### ballReleaseY *= 10*

#### ballSize *= 3*

#### boundaryThickness *= 5*

#### dropSlot *= 5*

#### numBalls *= 50*

#### numPins *= 16*

#### pinEndY *= 477.5*

#### pinHeightGap *= 30*

#### pinRadius *= 8*

#### pinStartY *= 112.5*

#### pinWidthGap *= 50*

#### screenGameWidth *= 762*

#### screenHeight *= 750*

#### screenWidth *= 1162*

#### slotHeight *= 262.5*

#### slotThickness *= 2*

#### waitTimeToEndSimulation_seconds *= 3*

#### worldX *= 400*

#### worldY *= 0*

### *class* modules.Parameters.LightTheme

Bases: `object`

This class contains all the colors for the light theme.

#### ballColor *= (0, 255, 0, 255)*

#### bgColor *= [255, 249, 242, 255]*

#### binColor *= [50, 238, 50, 50]*

#### boundaryColor *= [150, 150, 150, 255]*

#### pinColor *= [160, 190, 200, 255]*

#### slotColor *= [150, 150, 150, 255]*

#### textColor *= [30, 30, 30, 255]*

#### textHighlightColor *= (0, 0, 255, 255)*

#### textLightColor *= [160, 160, 160, 50]*

#### titleColor *= [100, 210, 100, 255]*
