import os
import time
import requests

import PySimpleGUI as sg
from PIL import ImageGrab



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
    config = {"func_1":True}

    icons_dict = {"icon_path_1":None}
    notification("No Internet", "No Internet Connection", icons_dict)

