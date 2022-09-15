""" 
- this script launches a command line style program when the users input is ""a"" into windows cmd
- before the user can set shot this script must first determine who the user is and his/her privilages, based on the users
- privilages, they will or will not get access to certain commands and features.
"""

import os
import sys
import yaml
import time
import json


main_path = os.path.dirname(os.path.dirname((__file__)))
sys.path.append(main_path) # /PIPEDREAMS/PipeDreams

import admin.Tools.utils.Utils as utils

import logging



# create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# create file handler which logs even debug messages
fh = logging.FileHandler('pipedreams/admin/logs/DreamLOG.log')
fh.setLevel(logging.DEBUG)

# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

logger.disabled = False



userName = os.environ['COMPUTERNAME']

admin_config = utils.yaml_config(f"{main_path}/admin/admin_config.yaml")
artist_config = utils.yaml_config(f"{main_path}/admin/artist_config.yaml")





def check_admin(userNames):
    """ Checks the users in the data list """

    privilages = []

    for admin in admin_config["Admin"]:
        admin_list = admin_config["Admin"][admin]

        for usr in admin_list:
            if userNames == usr:
                privilages.append(admin)
            else:
                privilages.append("None")

    return(privilages)



def check_title(userNames):
    """ gets the users title """

    title = []

    for role in artist_config["Team"]:
        team_list = artist_config["Team"][role]

        for usr in team_list:
            if userNames == usr:
                title.append(role)

    return(title)



def open_PipeLine_Config():
    """ opens the pipeline_config """

    # Open config
    config_path = os.path.abspath(__file__)
    config_path_dir = (f"{os.path.dirname(os.path.dirname(config_path))}")
    config = yaml.safe_load(open(f'{os.path.dirname(config_path_dir)}/PipeDreams/admin/pipeline_config.yaml', 'r'))

    return(config)



def getProductionPath():
    """ returns path to Dev directory """

    Pipedreams_path = f"{os.path.dirname(os.path.dirname(os.path.dirname((__file__))))}\PipeDreams\pipeline\production"
    
    return(Pipedreams_path)


def getLatestVersion(directory_path):
    """ returns the latest version number """

    config_version = open_PipeLine_Config()["production_build"]

    if config_version == "":
        ## add a algo to first check if config wants to use a spefici version, if not then use the latest version
        existing_versions = os.listdir(directory_path)
        version = existing_versions[-1]

    else:
        version = config_version

    print("Pipeline " + version)

    return(version)



def cmd_line_start(cmd_line_start_path):
    """ Opens the cmd line interface """
    
    os.startfile(cmd_line_start_path)





def run():
    """ main function of this script """


    # check if part of admin team
    privilages = check_admin(userName)[0]

    # check Title
    title = check_title(userName)

    # check user that is accessing the pipeline via cmd tool
    if privilages == "Tivoli":

        print(userName, privilages, title[0])

        # get path to dev directory to launch the latest dev pipeline
        production_path = getProductionPath()
        pipeline_version = getLatestVersion(production_path)
        pipeline_version_path = f"{production_path}/{pipeline_version}"
        cmd_line_start_path = f"{production_path}/{pipeline_version}/Main/UI/UI_start_compact.pyw"


        # check and update user list details
        checkUser_list(pipeline_version, cmd_line_start_path, privilages, title, pipeline_version_path)

        # start cmd line interface
        cmd_line_start(cmd_line_start_path)



    else:
        # launch cmd line for artist with basic privilages

        print(userName, privilages, title)

        # get path to dev directory to launch the latest dev pipeline
        production_path = getProductionPath()
        pipeline_version = getLatestVersion(production_path)
        pipeline_version_path = f"{production_path}/{pipeline_version}"
        cmd_line_start_path = f"{production_path}/{pipeline_version}/Main/UI/UI_start_compact.pyw"


        # check and update user list details
        checkUser_list(pipeline_version, cmd_line_start_path, privilages, title, pipeline_version_path)

        # start cmd line interface
        cmd_line_start(cmd_line_start_path)

        logger.warning(f"{userName} accessing production build {str(pipeline_version)}")





def write_to_json(json_path, data):
    """ Create and write to json file """

    with open(json_path, 'w') as f:
        json.dump(data, f, indent=6)




def read_json(json_path):
    """ Reads json file """
    with open(json_path) as f:
        json_file = json.loads(f.read())

    return (json_file)






def checkUser_list(pipeline_version, cmd_line_start_path, privilages, title, pipeline_version_path):
    """ load user list, and save out information such as the pipeline version they set to use and the path, 
    this is to help keep things dynamic with pipeline
    versions and production vs development versions """

    user_data_base = f"{os.path.dirname(os.path.dirname(__file__))}/admin/data/user_data_base/{userName}.json"

    if os.path.exists(user_data_base) != True:
        data = {}
        write_to_json(user_data_base, data)

    userData = read_json(user_data_base)

    userData[userName] = {  
                        "lastSeen" : time.time(),
                        "privilages" : privilages,
                        "title" : title,
                        "pipeline_version" : pipeline_version,
                        "pipeline_start_type" : cmd_line_start_path,
                        "pipeline_version_path" : pipeline_version_path
                        }


    write_to_json(user_data_base, userData)






if __name__ == "__main__":

    run()
    #checkUser_list(pipeline_version="", cmd_line_start_path="", privilages="", title="")






