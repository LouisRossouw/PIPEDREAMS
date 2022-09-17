import os
import sys
import time
import json
import yaml
import datetime

main_path = os.path.dirname(os.path.dirname((__file__)))
sys.path.append(main_path) # /PIPEDREAMS/PipeDreams




def get_UI_toolBar_config():
    """ returns either pipeline forced defaults or user preferences. """

    pipeline_config = open_PipeLine_Config()
    allow_user_preferences = pipeline_config["allow_user_preferences"]

    if allow_user_preferences == False:
        UI_toolBar_config = f"{main_path}/admin/UI_toolBar.yaml"
    elif allow_user_preferences == True:
        UI_toolBar_config = get_user_preferences()

    config = yaml_config(UI_toolBar_config)

    return(config)





def get_user_preferences():
    """ returns user preferences, creates it if it does not exist. """

    userName = os.environ['COMPUTERNAME']
    user_prefs = f"{main_path}/admin/data/user_preferences/{userName}_preferences.yaml"

    if os.path.exists(user_prefs) != True:

        UI_toolBar_config = yaml_config(f"{main_path}/admin/UI_toolBar.yaml")
        with open(user_prefs, 'w') as file:
            yaml.dump(UI_toolBar_config, file)

    return(user_prefs)





def cmd_line_start(cmd_line_start_path):
    """ Opens the cmd line interface """

    # logger.info("Attemping to load dcc launcher UI")
    os.startfile(cmd_line_start_path)




def get_date():
    """ returns current time """

    current_time = datetime.datetime.now().date()

    return(current_time)




def get_time():
    """ returns current time """

    current_time = time.time()

    return(current_time)




def getDevPath():
    """ returns path to Dev directory """

    Pipedreams_path = f"{os.path.dirname(os.path.dirname(os.path.dirname((__file__))))}\PipeDreams\pipeline\dev"
    
    return(Pipedreams_path)




def getProductionPath():
    """ returns path to Dev directory """

    Pipedreams_path = f"{os.path.dirname(os.path.dirname(os.path.dirname((__file__))))}\PipeDreams\pipeline\production"
    
    return(Pipedreams_path)




def getLatestVersion(directory_path):
    """ returns the latest version number """

    config_version = open_PipeLine_Config()["development_build"]

    if config_version == "":
        ## add a algo to first check if config wants to use a spefici version, if not then use the latest version
        existing_versions = os.listdir(directory_path)
        print(directory_path)
        version = existing_versions[-1]

    else:
        version = config_version

    print("Pipeline " + version)

    return(version)




def yaml_config(config_path):
    """ Open yaml configs. """
    config = yaml.safe_load(open(config_path))
    return(config)



admin_config = yaml_config(f"{main_path}/admin/admin_config.yaml")
artist_config = yaml_config(f"{main_path}/admin/artist_config.yaml")



def getUsers():
    """ Returns users records """
    userName = os.environ['COMPUTERNAME']

    admin_config = yaml_config(f"{main_path}/admin/admin_config.yaml")
    artist_config = yaml_config(f"{main_path}/admin/artist_config.yaml")

    return(userName, admin_config, artist_config)




def check_admin():
    """ Checks the users in the data list """

    data = getUsers()
    userNames = data[0]
    admin_config = data[1]

    privilages = []


    for admin in admin_config["Admin"]:
        admin_list = admin_config["Admin"][admin]

        for usr in admin_list:
            if userNames == usr:
                privilages.append(admin)

    privilages.append("null") # creates empty at the end of the array, to avoid Index out of range error.

    return(privilages)




def check_title():
    """ gets the users title """

    data = getUsers()
    userNames = data[0]
    artist_config = data[2]

    title = []

    for role in artist_config["Team"]:
        team_list = artist_config["Team"][role]

        for usr in team_list:
            if userNames == usr:
                title.append(role)

    title.append("null") # creates empty at the end of the array, to avoid Index out of range error.

    return(title)




def open_PipeLine_Config():
    """ opens the pipeline_config """

    # Open config
    config_path = os.path.abspath(__file__)
    config_path_dir = (f"{os.path.dirname(os.path.dirname(config_path))}")
    config = yaml.safe_load(open(f'{os.path.dirname(config_path_dir)}/PipeDreams/admin/pipeline_config.yaml', 'r'))

    return(config)




def write_to_json(json_path, data):
    """ Create and write to json file """

    with open(json_path, 'w') as f:
        json.dump(data, f, indent=6)




def read_json(json_path):
    """ Reads json file """
    with open(json_path) as f:
        json_file = json.loads(f.read())

    return (json_file)




def checkUser_list(pipeline_version, cmd_line_start_path, privilages, title, pipeline_version_path, userName):
    """ load user list, and save out information such as the pipeline version they set to use and the path, 
    this is to help keep things dynamic with pipeline
    versions and production vs development versions """

    user_data_base = f"{os.path.dirname(os.path.dirname(__file__))}/admin/data/user_data_base/{userName}.json"

    if os.path.exists(user_data_base) != True:
        data = {}
        write_to_json(user_data_base, data)

    userData = read_json(user_data_base)

    userData[userName] = {  
                        "lastSeen" : get_time(),
                        "privilages" : privilages,
                        "title" : title,
                        "pipeline_version" : pipeline_version,
                        "pipeline_start_type" : cmd_line_start_path,
                        "pipeline_version_path" : pipeline_version_path
                        }

    write_to_json(user_data_base, userData)



def return_toolBar_Config():
    """ returns the config for the toolbar """

    admin_dir = f"{(os.path.dirname(os.path.dirname(__file__)))}/admin"
    UI_toolBar_config_path = f"{admin_dir}/UI_toolBar.yaml"
    config = yaml_config(UI_toolBar_config_path)

    return(config)




def getPaths():
    """ returns common paths based on a predictable structure """

    resources_path = f"{(os.path.dirname(os.path.dirname(__file__)))}/pipeline/resources"

    return(resources_path)




def returnIconPath(paths, config, type):
    """ returns the icons paths """

    icon_theme = config["icon_theme"]

    if type == "side":

        icon_path_1 = f"{paths}/windows_tray_icons/tray_icon_animations/{icon_theme}/px_1.png"
        icon_path_2 = f"{paths}/windows_tray_icons/tray_icon_animations/{icon_theme}/px_2.png"

        sig_1 = f"{paths}/windows_tray_icons/tray_icon_animations/signal/sg_1.png"
        sig_2 = f"{paths}/windows_tray_icons/tray_icon_animations/signal/sg_2.png"
        sig_3 = f"{paths}/windows_tray_icons/tray_icon_animations/signal/sg_3.png"
        sig_4 = f"{paths}/windows_tray_icons/tray_icon_animations/signal/sg_4.png"
        sig_5 = f"{paths}/windows_tray_icons/tray_icon_animations/signal/sg_5.png"


    elif type == "min":

        icon_path_1 = f"{paths}/windows_tray_icons/tray_icon_mini_animations/{icon_theme}/px_1.ico"
        icon_path_2 = f"{paths}/windows_tray_icons/tray_icon_mini_animations/{icon_theme}/px_2.ico"

        sig_1 = f"{paths}/windows_tray_icons/tray_icon_mini_animations/signal/sg_1.png"
        sig_2 = f"{paths}/windows_tray_icons/tray_icon_mini_animations/signal/sg_2.png"
        sig_3 = f"{paths}/windows_tray_icons/tray_icon_mini_animations/signal/sg_3.png"
        sig_4 = f"{paths}/windows_tray_icons/tray_icon_mini_animations/signal/sg_4.png"
        sig_5 = f"{paths}/windows_tray_icons/tray_icon_mini_animations/signal/sg_5.png"


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


def animCount(anim_count, tray, icons_dict, type):
    """ Animates the icon by changing the image path and resseting the count so the image loops """

    # IF the UI type is the side, then we can feed it .png files.
    if type == "side":

        if anim_count == 1:
            tray.Update(filename=icons_dict["icon_path_1"])
        if anim_count == 2:
            tray.Update(filename=icons_dict["icon_path_2"])

        if anim_count == 2:
            anim_count = 0

    # IF the UI type is the minimized, then we need to feed it .ico files.
    elif type == "min":

        if anim_count == 1:
            tray.update(icon=icons_dict["icon_path_1"])
        if anim_count == 2:
            tray.update(icon=icons_dict["icon_path_2"])

        if anim_count == 2:
            anim_count = 0

    return(anim_count)





if __name__ == "__main__":
    # print(get_date())
    mypref = get_UI_toolBar_config()

