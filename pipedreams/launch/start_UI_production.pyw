""" 
- this script launches a command line style program when the users input is ""a"" into windows cmd
- before the user can set shot this script must first determine who the user is and his/her privilages, based on the users
- privilages, they will or will not get access to certain commands and features.
"""

import os
import loggers

import utils as utils








def run():
    """ main function of this script """

    userName = os.environ['COMPUTERNAME']
    logger = loggers.create_logger("UI_production")

    logger.info(f"**** start ****")

    # check if part of admin team
    privilages = utils.check_admin()[0]

    # check Title
    title = utils.check_title()

    # check user that is accessing the pipeline via cmd tool
    if privilages == "Tivoli":

        print(userName, privilages, title[0])

        # get path to dev directory to launch the latest dev pipeline
        production_path = utils.getProductionPath()
        pipeline_version = utils.getLatestVersion(production_path)
        pipeline_version_path = f"{production_path}/{pipeline_version}"
        cmd_line_start_path = f"{production_path}/{pipeline_version}/Main/UI/UI_start_compact.pyw"


        # check and update user list details
        utils.checkUser_list(pipeline_version, cmd_line_start_path, privilages, title, pipeline_version_path, userName)

        # start cmd line interface
        utils.cmd_line_start(cmd_line_start_path)



    else:

        # launch cmd line for artist with basic privilages
        print(userName, privilages, title)

        # get path to dev directory to launch the latest dev pipeline
        production_path = utils.getProductionPath()
        pipeline_version = utils.getLatestVersion(production_path)
        pipeline_version_path = f"{production_path}/{pipeline_version}"
        cmd_line_start_path = f"{production_path}/{pipeline_version}/Main/UI/UI_start_compact.pyw"


        # check and update user list details
        utils.checkUser_list(pipeline_version, cmd_line_start_path, privilages, title, pipeline_version_path, userName)

        # start cmd line interface
        utils.cmd_line_start(cmd_line_start_path)

        logger.warning(f"{userName} accessing production build {str(pipeline_version)}")





if __name__ == "__main__":

    run()







