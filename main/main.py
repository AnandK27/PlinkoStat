# Author: Navin
# Created: December 2020
# License: MIT
 
# Installation instructions:
# It is recommended that you install Python as part of a virtual environment like pyEnv so that it does not mess up your system's Python. Python3 is preferred.
# Install dependent libraries:
# >>> pip3 install pygame
# >>> pip3 install pymunk
# Now simply run using: 
# >>> python3 main.py

import os
import logging, traceback


#-----------------------------------------------
#-----------------------------------------------
#             PROGRAM STARTS HERE
#-----------------------------------------------
#-----------------------------------------------
if __name__ == '__main__':

    from Parameters import Env
    from Environment import *
    
    noErrors = True
    sim = Environment(Env.ballSize)    
    
    try:
        sim.initialize()
        sim.runWorld()
    except BaseException as e:
        noErrors = False
        print(e)
        logging.error(traceback.format_exc(None, True))
