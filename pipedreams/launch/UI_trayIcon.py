import os
import sys
import time
import PySimpleGUI as sg

sys.path.append(os.path.dirname(os.path.dirname(__file__))) #/PIPEDREAMS/PipeDreams

import launch.start_UI_production as start_UI_production
import launch.start_UI_dev as start_UI_dev

import utils as utils
import admin.Tools.admin as admin

import functions.icon_BG_function as BG_function





def Clear_Cache():
    """ Clears system cache """
    print("yess")

def returnConfig():
    """ returns the config for the toolbar """

    admin_dir = f"{(os.path.dirname(os.path.dirname(__file__)))}/admin"
    UI_toolBar_config_path = f"{admin_dir}/UI_toolBar.yaml"
    config = utils.yaml_config(UI_toolBar_config_path)

    return(config)
    



def getPaths():
    """ returns common paths based on a predictable structure """

    resources_path = f"{(os.path.dirname(os.path.dirname(__file__)))}/pipeline/resources"

    return(resources_path)




def returnIconPath(paths, config):
    """ returns the icons paths """

    icon_theme = config["icon_theme"]

    icon_path_1 = f"{paths}/windows_tray_icons/tray_icon_animations/{icon_theme}/px_1.png"
    icon_path_2 = f"{paths}/windows_tray_icons/tray_icon_animations/{icon_theme}/px_2.png"

    sig_1 = f"{paths}/windows_tray_icons/tray_icon_animations/signal/sg_1.png"
    sig_2 = f"{paths}/windows_tray_icons/tray_icon_animations/signal/sg_2.png"
    sig_3 = f"{paths}/windows_tray_icons/tray_icon_animations/signal/sg_3.png"
    sig_4 = f"{paths}/windows_tray_icons/tray_icon_animations/signal/sg_4.png"
    sig_5 = f"{paths}/windows_tray_icons/tray_icon_animations/signal/sg_5.png"

    icons={
        "icon_path_1" : icon_path_1,
        "icon_path_2" : icon_path_2,

        "sig_1" : sig_1,
        "sig_2" : sig_2,
        "sig_3" : sig_3,
        "sig_4" : sig_4,
        "sig_5" : sig_5,
        
        }

    return(icons)





def animCount(anim_count, tray, icons_dict):
    """ Animates the icon by changing the image path and resseting the count so the image loops """

    if anim_count == 1:
        tray.Update(filename=icons_dict["icon_path_1"])
    if anim_count == 2:
        tray.Update(filename=icons_dict["icon_path_2"])

    if anim_count == 2:
        anim_count = 0

    return(anim_count)



def performFunctions(performFunctions_count, PERFORMFUNCTION_ITERATION_COUNT, icons_dict, config):
    """ the tool will run through a list of functions that it can perform at every iteration of its while loop:
        for example, we can add a function here that gets called that checks for any new items / assets added, and a notification system will popup,
        Or, a function that checks email for any new emails, 
    """

    # run function IF performFunctions_count == the limit, and then reset it to 0
    if performFunctions_count == PERFORMFUNCTION_ITERATION_COUNT:

        # quick_signal = sg.SystemTray(filename=icons_dict["sig_2"])

        """ add functions to run, here! """

        BG_function.connected_to_internet(config, icons_dict)
        BG_function.function_01(config)
        BG_function.function_02(config)

        # just a visual refrence to show that its performing this function
        # quick_signal.read(timeout=100)
        # quick_signal.update(filename=icons_dict["sig_1"])
        # quick_signal.read(timeout=100)
        # quick_signal.close()
        
        # Reset back to zero, so that the above functions will only run on every x iteration.
        performFunctions_count = 0
    
    return(performFunctions_count)


# Settings for the Ui and functionality 
config = returnConfig()

THEME = config["theme"]
WEBSITE = config["website"]
ICON_ANIMATED = config["icon_animated"]
PERFORMFUNCTION_ITERATION_COUNT = config["backround_check_every"]
CHECK_PERFORMFUNCTION = config["backround_check"]


def main(python_exe):
    """ Runs the Main tray toolbar """

    sg.theme(THEME)

    icons_dict = returnIconPath(getPaths(), config)
    menu_def = ['UNUSED', ['PipeDreams', 'Utils',['Create Project'],'---', 'Tools', ['Clear Cache'], 'Dev',['PipeDreams_Dev', 'Admin'] ,'---', 'Settings', 'About', 'Exit']]
    
    tray = sg.SystemTray(menu=menu_def, filename=icons_dict["icon_path_1"])
    window= ''

    anim_count = 0
    performFunctions_count = 0

    # UI loop
    while True:

        anim_count += 1
        performFunctions_count +=1

        event = tray.read(timeout=500)
        # print(anim_count, performFunctions_count)

        if event == 'Exit':
            break


        if event == "PipeDreams":
            start_UI_production.run(python_exe)


        if event == "PipeDreams_Dev":
            start_UI_dev.run(python_exe)

        
        if event == "Admin":
            if utils.check_admin()[0] == "Tivoli":
                admin.admin_start()
            else:
                pass

        if event == "Settings":
            print("Settings wip")

        if event == "About":
            os.system("start \"\" "+ (WEBSITE))

        if event == "Clear Cache":
            Clear_Cache()


        elif event in('UI', sg.EVENT_SYSTEM_TRAY_ICON_DOUBLE_CLICKED) and not window:
            anim_count = 1
            tray.Update(filename=icons_dict["icon_path_1"])
            start_UI_production.run()


        elif event == 'Hide' and window:
            anim_count = 1
            tray.Update(filename=icons_dict["icon_path_1"])
            window.close()
            window = None


        if window:
            event, values = window.read(timeout=1000)
            
            if event in (sg.WIN_CLOSED, 'Minimize\nTo Tray'):
                anim_count = 1
                window.close()
                window = None
                continue





        # animates tray Icon, only 2 frames currently allowed
        if ICON_ANIMATED == True:
            anim_count = animCount(anim_count, tray, icons_dict)

        if CHECK_PERFORMFUNCTION == True:
            performFunctions_count = performFunctions(performFunctions_count, 
                                                        PERFORMFUNCTION_ITERATION_COUNT,
                                                        icons_dict,
                                                        config)



    tray.close()
    if window:
        window.close()




