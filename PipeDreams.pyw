
""" This file needs to be converted to a .exe and shared as a shortcut to other users machines,
    - it checks the pipeline_config and chooses to launch the pipeline with the local default Python interpreter
    or the portable Python interpreter that lives in the /pipedreams/pipeline/tools/Python directory.
"""

import os
import sys
import shutil
import pipedreams.launch.utils as utils



this_dir = os.path.dirname(sys.argv[0])




def get_the_PY(PIPEDREAMS_DIR):
    """ returns the python version nam being used in the /pipedreams/pipeline/tools/Python directory -
        incase there is a unique python version.
    """
    dir_files = os.listdir(PIPEDREAMS_DIR)
    for f in dir_files:
        if f != ".gitignore":
            pyname = f

    return(pyname)




def path_set(
            launch_dir, 
            ffmpeg_dir, 
            Python_dir,
            ):
    """ sets system paths to env and other tools like ffmpeg """


    py_version = get_the_PY(Python_dir)
    python_interpreter = f"{Python_dir}/{py_version}"
    python_scripts = f"{python_interpreter}/Scripts"


    # set sys env paths
    sys.path.append(launch_dir)
    os.environ['PATH'] += os.pathsep + ffmpeg_dir
    os.environ['PATH'] += os.pathsep + python_interpreter
    os.environ['PATH'] += os.pathsep + python_scripts

    print("*** Set paths:")
    print(python_interpreter)
    print(python_scripts)




def install_Python(appdata_Python_dir):
    """ Install / coppies over a version of Python, it first tries to copy over python if it exists in pipedream /pipeline/tools/Python directory
        If not, it will then attempt to install it from the internet.
    """

    Internal_Python_path = f"{this_dir}/pipedreams/pipeline/tools/python"
    Internal_Python_path_dir = os.listdir(Internal_Python_path)

    # checks if Python exists in pipedreams file structure, if True then simply copy and paste to user AppData and set paths.
    for dir in Internal_Python_path_dir:
        if dir != ".gitignore":
            if "Python" in dir:
                shutil.copytree(Internal_Python_path, appdata_Python_dir)



def check_Python(Python_dir):
    """ Check if default Python is installed, if not, install it """

    PY_version = os.system("py --version")

    if os.path.exists(Python_dir) != True:
        print("Python does not exist")
        install_Python(Python_dir)




def launch_pipedreams(launch_dir):
    """ launches pipedreams tools. """

    print("pipedreams launching.")




def startup():
    """ Fist startup for Pipedreams """

    userName = os.environ['COMPUTERNAME']

    PIPEDREAMS_DIR = os.path.dirname(__file__)
    launch_dir = f"{PIPEDREAMS_DIR}/pipedreams/launch"

    # # paths to tools.
    ffmpeg_dir = f"{PIPEDREAMS_DIR}/pipedreams/pipeline/tools/ffmpeg"

    usr_data_dir = f"{this_dir}/pipedreams/admin/data/user_data_base"
    pipeline_config = utils.yaml_config(f"{this_dir}/pipedreams/admin/pipeline_config.yaml")

    appdata_path = os.path.dirname(os.getenv('APPDATA'))
    Python_dir = f"{appdata_path}/Local/Programs/Python"





    # check if user exists in database directory, if not, check if default Python is installed.
    if os.path.exists(f"{usr_data_dir}/{userName}.json") != True:
        check_Python(Python_dir)
    else:
        pass



    path_set(
            launch_dir, 
            ffmpeg_dir, 
            Python_dir, 
            )


    launch_pipedreams(launch_dir)




if __name__ == "__main__":

    startup()
