
""" This file needs to be converted to a .exe and shared as a shortcut to other users machines,
    - it checks the pipeline_config and chooses to launch the pipeline with the local default Python interpreter
    or the portable Python interpreter that lives in the /pipedreams/pipeline/tools/Python directory.
"""

import os
import sys
import shutil
import pipedreams.launch.utils as utils

import ctypes  # An included library with Python install.   







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

    try:
        py_version = get_the_PY(Python_dir)
    except FileNotFoundError:
        py_version = None

    if py_version != None:

        python_interpreter = f"{Python_dir}/{py_version}"
        python_scripts = f"{python_interpreter}/Scripts"

        # set sys env paths
        sys.path.append(launch_dir)
        os.environ['PATH'] += os.pathsep + ffmpeg_dir
        os.environ['PATH'] += os.pathsep + python_interpreter
        os.environ['PATH'] += os.pathsep + python_scripts

        print("*** Set paths:")
        print(ffmpeg_dir)
        print(python_interpreter)
        print(python_scripts)





def install_Python(appdata_Python_dir):
    """ Install / coppies over a version of Python, it first tries to copy over python if it exists in pipedream /pipeline/tools/Python directory
        If not, it will then attempt to install it from the internet.
    """
    print("Installing Python.")

    text = f"No Python found, installing Python \n-{appdata_Python_dir}"
    ctypes.windll.user32.MessageBoxW(0, text, "PipeDreams", 0)

    this_dir = os.path.dirname(sys.argv[0])
    Internal_Python_path = f"{this_dir}/pipedreams/pipeline/tools/python"
    Internal_Python_path_dir = os.listdir(Internal_Python_path)

    # checks if Python exists in pipedreams file structure, if True then simply copy and paste to user AppData and set paths.
    for dir in Internal_Python_path_dir:
        if dir != ".gitignore":
            if "Python" in dir:
                shutil.copytree(Internal_Python_path, appdata_Python_dir)

                text = f"Done"
                ctypes.windll.user32.MessageBoxW(0, text, "PipeDreams", 0)




def check_Python(Python_dir):
    """ Check if default Python is installed, if not, install it """

    PY_version = os.system("py --version")

    if os.path.exists(Python_dir) != True:
        print("** Python does not exist")
        install_Python(Python_dir)




def check_Python_packages(PIPEDREAMS_DIR, pipeline_config):
    """ checks and makes sure system python has all the packages needed to run Pipedreams. """

    maya_version = pipeline_config["maya_version"]


    # System default Python
    os.system(f"pip install -r {PIPEDREAMS_DIR}/pipedreams/admin/requirements/system_requirements.txt")

    # Maya Python
    ProgramFiles_path = os.environ["ProgramFiles"]
    path = f"{ProgramFiles_path}/Autodesk/Maya{str(maya_version)}/bin/mayapy.exe -m pip install -r {PIPEDREAMS_DIR}/pipedreams/admin/requirements/maya_requirements.txt"
    os.system(path)




def launch_pipedreams(launch_dir):
    """ launches pipedreams tools. """

    print("pipedreams launching.")
    os.startfile(f"{launch_dir}/UI_trayIcon.pyw")




def startup():
    """ Fist startup for Pipedreams """

    userName = os.environ['COMPUTERNAME']

    PIPEDREAMS_DIR = os.path.dirname(sys.argv[0])
    launch_dir = f"{PIPEDREAMS_DIR}/pipedreams/launch"

    # # paths to tools.
    ffmpeg_dir = f"{PIPEDREAMS_DIR}/pipedreams/pipeline/tools/ffmpeg"

    usr_data_dir = f"{PIPEDREAMS_DIR}/pipedreams/admin/data/user_data_base"
    pipeline_config = utils.yaml_config(f"{PIPEDREAMS_DIR}/pipedreams/admin/pipeline_config.yaml")


    appdata_path = os.path.dirname(os.getenv('APPDATA'))
    Python_dir = f"{appdata_path}/Local/Programs/Python"


    # check if user exists in database directory, if not, check if default Python is installed.
    if os.path.exists(f"{usr_data_dir}/{userName}.json") != True:
        check_Python(Python_dir)
        path_set(launch_dir, ffmpeg_dir, Python_dir,)
        check_Python_packages(PIPEDREAMS_DIR, pipeline_config)
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


