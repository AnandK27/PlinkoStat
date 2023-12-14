import logging, traceback


if __name__ == '__main__':

    # This file imports the modules and runs the simulation (encapsulation).
    
    from modules.Environment import *
    
    noErrors = True
    sim = Environment()    
    
    try:
        sim.initialize()
        sim.runWorld()
    except BaseException as e:
        # If an error occurs, log the error and print it to the console.
        noErrors = False
        print(e)
        logging.error(traceback.format_exc(None, True))
