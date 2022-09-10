
""" This file needs to be converted to a .exe and shared as a shortcut to other users machines,
    - it checks the pipeline_config and chooses to launch the pipeline with the local default Python interpreter
    or the portable Python interpreter that lives in the /pipedreams/pipeline/tools/Python directory.
"""

import os
import sys
import shutil
import pipedreams.launch.utils as utils



this_dir = os.path.dirname(sys.argv[0])




def install_Python(appdata_Python_dir):
    """ Install / coppies over a version of Python, it first tries to copy over python if it exists in pipedream /pipeline/tools/Python directory
        If not, it will then attempt to install it from the internet.
    """

    Internal_Python_path = f"{this_dir}/pipedreams/pipeline/tools/python"
    Internal_Python_path_dir = os.listdir(Internal_Python_path)

    for dir in Internal_Python_path_dir:
        if dir != ".gitignore":
            if "Python" in dir:
                shutil.copytree(Internal_Python_path, appdata_Python_dir)



def check_Python():
    """ Check if default Python is installed, if not, install it """

    PY_version = os.system("py --version")
    appdata_path = os.path.dirname(os.getenv('APPDATA'))
    Python_dir = f"{appdata_path}/Local/Programs/Python"

    if os.path.exists(Python_dir) != True:
        print("Python does not exist")
        install_Python(Python_dir)


def startup():
    """ Fist startup for Pipedreams """

    userName = os.environ['COMPUTERNAME']


    usr_data_dir = f"{this_dir}/pipedreams/admin/data/user_data_base"

    pipeline_config = utils.yaml_config(f"{this_dir}/pipedreams/admin/pipeline_config.yaml")


    # check if user exists in database directory, if not, check if default Python is installed.
    if os.path.exists(f"{usr_data_dir}/{userName}.json") != True:

        check_Python()

    else:
        pass





if __name__ == "__main__":

    startup()