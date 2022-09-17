""" 
- this script launches a command line style program when the users input is ""a"" into windows cmd
- before the user can set shot this script must first determine who the user is and his/her privilages, based on the users
- privilages, they will or will not get access to certain commands and features.
"""

import os
import ctypes
import loggers

import utils as utils







def run():
    """ Starts the Dev UI version """


    userName = os.environ['COMPUTERNAME']
    logger = loggers.create_logger("UI_dev")

    logger.info(f"**** start ****")

    # check if part of admin team
    try:
        privilages = utils.check_admin()[0]
    except IndexError:
        privilages = None
        pass

    # check Title
    title = utils.check_title()

    print(userName, title, privilages)

    # check user that is accessing the pipeline via cmd tool
    if privilages == "Tivoli":

        print(userName, privilages, title)

        # get path to dev directory to launch the latest dev pipeline
        dev_path = utils.getDevPath()
        pipeline_version = utils.getLatestVersion(dev_path)
        pipeline_version_path = f"{dev_path}\{pipeline_version}"
        cmd_line_start_path = f"{dev_path}/{pipeline_version}/Main/UI/UI_start_compact.pyw"

        # check and update user list details
        utils.checkUser_list(pipeline_version, cmd_line_start_path, privilages, title, pipeline_version_path, userName)

        # start cmd line interface
        print(pipeline_version)
        utils.cmd_line_start(cmd_line_start_path)


    else:
        
        # Denied access
        dev_path = utils.getDevPath()
        pipeline_version = utils.getLatestVersion(dev_path)
        text = f"{userName} | you need Admin rights to access dev build {str(pipeline_version)}."
        ctypes.windll.user32.MessageBoxW(0, text, "PipeDreams", 0)
        logger.warning(f"{userName} attempting to access Dev build {str(pipeline_version)} - access denied.")






if __name__ == "__main__":

    run()






