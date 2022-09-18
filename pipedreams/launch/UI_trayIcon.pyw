import os
import sys
import time
import loggers
import PySimpleGUI as sg

sys.path.append(os.path.dirname(os.path.dirname(__file__))) #/PIPEDREAMS/PipeDreams

import launch.start_UI_production as start_UI_production
import launch.start_UI_dev as start_UI_dev

import utils as utils
import UI_settings as UI_settings
import admin.Tools.admin as admin

import functions.icon_BG_function as BG_function








def Clear_Cache():
    """ Clears system cache """
    print("wip")



userName = os.environ['COMPUTERNAME']

logger_name = "UI_trayIcon"
logger = loggers.create_logger(logger_name)

# Settings for the Ui and functionality 
config = utils.get_UI_toolBar_config()



THEME = config["theme"]
WEBSITE = config["website"]
ICON_ANIMATED = config["icon_animated"]
PERFORMFUNCTION_ITERATION_COUNT = config["backround_check_every"]
CHECK_PERFORMFUNCTION = config["backround_check"]


def main():
    """ Runs the Main tray toolbar """

    sg.theme(THEME)

    icons_dict = utils.returnIconPath(utils.getPaths(), config, type="side")
    menu_def = ['UNUSED', ['PipeDreams','---', 'Tools', ['Clear Cache'], 'Dev',['PipeDreams_Dev', 'Admin'] ,'---', 'Settings', 'About', 'Exit']]
     
    tray = sg.SystemTray(menu=menu_def, filename=icons_dict["icon_path_1"])
    window= ''

    anim_count = 0
    performFunctions_count = 0

    logger.info("UI_trayIcon loaded.")


    # UI loop
    while True:

        anim_count += 1
        performFunctions_count +=1

        event = tray.read(timeout=500)
        # print(anim_count, performFunctions_count)

        if event == 'Exit':
            break


        if event == "PipeDreams":
            start_UI_production.run()


        if event == "PipeDreams_Dev":
            start_UI_dev.run()

        
        if event == "Admin":
            if utils.check_admin()[0] == "Tivoli":
                admin.admin_start()
            else:
                pass

        if event == "Settings":
            UI_settings.Run_user_preferences("")



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
            anim_count = utils.animCount(anim_count, tray, icons_dict, type="side")

        if CHECK_PERFORMFUNCTION == True:
            performFunctions_count = BG_function.performFunctions(
                                                                    performFunctions_count, 
                                                                    PERFORMFUNCTION_ITERATION_COUNT,
                                                                    icons_dict,
                                                                    config, 
                                                                    logger
                                                                )


    tray.close()
    if window:
        window.close()

try:
    main()
except Exception as error:
    logger.exception(error)