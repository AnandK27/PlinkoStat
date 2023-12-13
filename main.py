import logging, traceback


if __name__ == '__main__':

    from modules.Parameters import Env
    from modules.Environment import *
    
    noErrors = True
    sim = Environment()    
    
    try:
        sim.initialize()
        sim.runWorld()
    except BaseException as e:
        noErrors = False
        print(e)
        logging.error(traceback.format_exc(None, True))
