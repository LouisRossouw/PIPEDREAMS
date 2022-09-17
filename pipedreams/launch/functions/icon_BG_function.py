""" This file is for UI_trayIcon.pyw file - performFunction , every 10 seconds the icon will run these backroound functions """

import datetime
import requests

import PySimpleGUI as sg
from PIL import ImageGrab

import utils as utils


def performFunctions(performFunctions_count, PERFORMFUNCTION_ITERATION_COUNT, icons_dict, config, logger):
    """ the tool will run through a list of functions that it can perform at every iteration of its while loop:
        for example, we can add a function here that gets called that checks for any new items / assets added, and a notification system will popup,
        Or, a function that checks email for any new emails, 
    """

    # run function IF performFunctions_count == the limit, and then reset it to 0
    if performFunctions_count == PERFORMFUNCTION_ITERATION_COUNT:

        # quick_signal = sg.SystemTray(filename=icons_dict["sig_2"])

        """ add functions to run, here! """

        connected_to_internet(config, icons_dict)
        function_01(config)
        function_02(config)
        logger_newday(logger)
        print("this is running")


        # just a visual refrence to show that its performing this function
        # quick_signal.read(timeout=100)
        # quick_signal.update(filename=icons_dict["sig_1"])
        # quick_signal.read(timeout=100)
        # quick_signal.close()
        
        # Reset back to zero, so that the above functions will only run on every x iteration.
        performFunctions_count = 0
    
    return(performFunctions_count)



def logger_newday(logger):
    """ adds a new day entry into the user_DreamLOG.log file. """

    if ITS_A_NEWDAY() == True:
        logger.info("")
        logger.info((" * ") * 20 + (" - NEW DAY - ") + (" * ") * 20)
        logger.info("")
        print("newdays")
    else:
        pass




def ITS_A_NEWDAY():
    """ 
    returns True or False if it is a new day, it returns True at midnight when the two DateTimes dont match, 
    there is a specific time window when the two dates wont match, and other external code can perform actions during this time frame. 
    """

    time_window = 35
    time_stamp_NOW = utils.get_time()
    time_stamp_PAST = utils.get_time() - time_window # minus 35 seconds

    datetime_NOW = datetime.datetime.fromtimestamp(time_stamp_NOW).date()
    datetime_PAST = datetime.datetime.fromtimestamp(time_stamp_PAST).date()

    # the 35 second difference will let the if statement execute at midnight when there is a
    # difference in the current date between that 35 second window.
    if datetime_NOW != datetime_PAST:
        isit_a_day = True
    else:
        isit_a_day = False

    return(isit_a_day)




def screen_size():
    img = ImageGrab.grab()
    return (img.size)




def notification(Title, Message, icons_dict):
    """ Simple notification popup """

    sg.SystemTray.notify(title=" "*20 + Title, 
                        message=" "*20 + Message,
                        icon=icons_dict["icon_path_1"],
                        fade_in_duration=100,
                        display_duration_in_ms=2000,
                        alpha=0.8,
                        location=(screen_size()[0] / 2, 0),
                        )




def connected_to_internet(config, icons_dict):
    """ checks if connected to the internet """
    if config["func_check_internet"] == True:

        url = "http://www.google.com/"
        timeout = 5
        try:
            _ = requests.head(url, timeout=timeout)
            connected =  True
        except requests.ConnectionError:
            print("No internet connection available.")
            connected = False

            quick_signal = sg.SystemTray(filename=icons_dict["sig_4"])
            quick_signal.read(timeout=500)
            quick_signal.update(filename=icons_dict["sig_5"])
            quick_signal.close()

            notification("No Internet", "No Internet Connection", icons_dict)

        return(connected)




def function_01(config):
    """ function 1 wip """

    if config["func_1"] == True:
        pass




def function_02(config):
    """ function 2 wip """

    if config["func_2"] == True:
        pass




if __name__ == "__main__":

    # config = {"func_1":True}
    # icons_dict = {"icon_path_1":None}
    # notification("No Internet", "No Internet Connection", icons_dict)

    ITS_A_NEWDAY()

