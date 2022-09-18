import os
import yaml
import time
from pathlib import Path

import PySimpleGUI as sg

# Fixes blurry issues on UI for win10 high DPI displays
# from ctypes import windll
# windll.shcore.SetProcessDpiAwareness(1)


def get_UI_config():
    """ returns the UI specific config """

    main_path = Path(__file__).parents[1]
    config_path = (f"{main_path}/admin/UI_toolBar.yaml")
    file_data = yaml.safe_load(open(config_path, 'r'))

    return file_data




def get_preferences():
    """ get users prefrences. """

    userName = os.environ['COMPUTERNAME']
    this_dir = Path(__file__).parents[1]
    path = f"{this_dir}/admin/data/user_preferences/{userName}_preferences.yaml"

    user_preferences = yaml.safe_load(open(path, 'r'))

    return(user_preferences)




def UI_get_icons():
    """ returns a list of existing icon themes. """

    resources_path = f"{Path(__file__).parents[1]}/pipeline/resources/windows_tray_icons/tray_icon_animations"
    icon_themes = os.listdir(resources_path)

    themes = []
    for icon in icon_themes:
        if icon != "signal":
            themes.append(icon)

    return(themes)




def write_yaml(path, data):
    """ writes out a yaml file. """

    with open(path, 'w') as file:
        yaml.dump(data, file)




def save_preferences(UI_config, values):

    for val in values:
        UI_config[val] = values[val] # updates existing keys in config with the new ones

    # Save / overwirte user preferences.
    userName = os.environ['COMPUTERNAME']
    this_dir = Path(__file__).parents[1]
    path = f"{this_dir}/admin/data/user_preferences/{userName}_preferences.yaml"

    write_yaml(path, UI_config)

    pipedreams_pyw = f"{Path(__file__).parents[2]}/PipeDreams.exe"
    os.startfile(pipedreams_pyw)
    exit()




def Run_user_preferences(icon_1):
    """ builds a UI for the project creator """


    UI_config = get_preferences()


    THEME = UI_config['CREATE_THEME']
    CREATE_WINDOW_NUDGE = UI_config["CREATE_WINDOW_NUDGE"]
    CREATE_WINDOW_SIZE = UI_config["CREATE_WINDOW_SIZE"]
    CREATE_FONT_HEADING = UI_config["FONT_HEADING"]

    CREATE_TEXT_COLOR_MULTILINE = UI_config["TEXT_COLOR_MULTILINE"]
    CREATE_FONT_MULTILINE = UI_config["FONT_MULTILINE"]
    CREATE_BG_MULTILINE = UI_config["BG_MULTILINE"]

    CREATE_WINDOW_TEXT_COLOR = UI_config["WINDOW_TEXT_COLOR"]
    CREATE_WINDOW_BG_COLOR = UI_config["WINDOW_BG_COLOR"]

    ICON_THEME = UI_config["icon_theme"]
    ICON_ANIMATED = UI_config["icon_animated"]
    MINIMIZED_TRAYICON = UI_config["MINIMIZED_TRAYICON"]

    # Theme
    sg.theme(THEME) 

    # Build UI layout
    layout = [  
                [sg.Text("Icon Theme:"), sg.InputCombo((UI_get_icons()), key="icon_theme", default_value=ICON_THEME),],
                [sg.Checkbox("Icon Animated", key='icon_animated', default=ICON_ANIMATED),],
                [sg.Checkbox("Minimized TrayIcon", key='MINIMIZED_TRAYICON', default=MINIMIZED_TRAYICON),],

                [sg.Push(), sg.Button('Save', key="-SAVE-")] ]

    # Build UI
    window = sg.Window('Video Converter', 
                        layout,
                        no_titlebar=False, 
                        resizable=False, 
                        use_custom_titlebar=True, 
                        finalize=False, 
                        keep_on_top=True,
                        titlebar_background_color=CREATE_WINDOW_BG_COLOR,
                
                        alpha_channel=1,
                        titlebar_text_color=CREATE_WINDOW_TEXT_COLOR,
                        icon=icon_1,
                        titlebar_icon=icon_1,

                        )


    # Read UI
    event, values = window.read()


    if event == "-SAVE-":
        save_preferences(UI_config, values)





if __name__ == "__main__":

    # print(os.getpid())
    # pipedreams_pyw = f"{Path(__file__).parents[2]}"

    Run_user_preferences("")


