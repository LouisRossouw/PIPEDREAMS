
import os
import time
import loggers

from infi.systray import SysTrayIcon

import utils as utils
import start_UI_production as start_UI_production
import start_UI_dev as start_UI_dev
import functions.icon_BG_function as BG_function


resources_dir = utils.getPaths()

# Icons
path_to_icon = f"{resources_dir}\\windows_tray_icons\\tray_icon_mini_animations\\default_colors\\px_1.ico"

Pipedreams_PRO_ICO = f"{resources_dir}\\windows_tray_icons\\tray_icon_mini_animations\\black_colors\\px_1.ico"
Pipedreams_DEV_ICO = f"{resources_dir}\\windows_tray_icons\\tray_icon_mini_animations\\black_colors\\px_2.ico"
admin = f"{resources_dir}\\windows_tray_icons\\tray_icon_mini_animations\\admin_boet\\px_1.ico"

hover_text = "PipeDreams"




def Pipedreams_UI_PRODUCTION(sysTrayIcon):
    start_UI_production.run()


def Pipedreams_UI_DEV(sysTrayIcon):
    start_UI_dev.run()


def about(sysTrayIcon):
    os.system("start \"\" https://louisrossouw.com")


def close_app(sysTrayIcon):
    print ('Closing PipeDreams.')


def run_admin(sysTrayIcon):
    """ will run the Admins menu """
    pass





def menu():
    """ Builds the trayIcons Menus """
    menu_options = (('PipeDreams', Pipedreams_PRO_ICO, Pipedreams_UI_PRODUCTION),
                    ('Dev', Pipedreams_DEV_ICO, (('PipeDreams Dev', admin, Pipedreams_UI_DEV),('Admin', admin, run_admin),)),
                    ('About', admin, about),
                )

    return(menu_options)


def run(config):

    logger.info(" *** Starting TrayIcon Mini *** ")

    sysTrayIcon = SysTrayIcon(path_to_icon, hover_text, menu(), on_quit=close_app, default_menu_index=0)
    sysTrayIcon.start()


    THEME = config["theme"]
    ICON_SPEED = 0.5
    WEBSITE = config["website"]
    ICON_ANIMATED = config["icon_animated"]
    PERFORMFUNCTION_ITERATION_COUNT = config["backround_check_every"]
    CHECK_PERFORMFUNCTION = config["backround_check"]

    icons_dict = utils.returnIconPath(utils.getPaths(), config, type="min")


    anim_count = 0
    performFunctions_count = 0

    while True:

        anim_count += 1
        performFunctions_count += 1

        time.sleep(ICON_SPEED)

        # animates tray Icon, only 2 frames currently allowed
        if ICON_ANIMATED == True:
            anim_count = utils.animCount(anim_count, sysTrayIcon, icons_dict, type="min")

        if CHECK_PERFORMFUNCTION == True:
            performFunctions_count = BG_function.performFunctions(
                                                                    performFunctions_count, 
                                                                    PERFORMFUNCTION_ITERATION_COUNT,
                                                                    icons_dict,
                                                                    config,
                                                                    logger
                                                                )


logger_name = "UI_trayIcon_MINI"
logger = loggers.create_logger(logger_name)


# Settings for the Ui and functionality 
config = utils.get_UI_toolBar_config()

try:
    run(config)
except Exception as e:
    logger.exception(e)
    

    





