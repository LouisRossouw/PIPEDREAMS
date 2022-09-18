
""" This file needs to be converted to a .exe and shared as a shortcut to other users machines,
    - before startup it runs a check to see if Python and its packags are installed for this program.
    - to convert to .exe with pyinstaller installed, in cmd run: pyinstaller --onefile --windowed --icon=app.ico app.py
"""

import os
import time
import sys
import yaml
import shutil

import ctypes  # An included library with Python install.   

import logging


userName = os.environ['COMPUTERNAME']

# create logger
logger = logging.getLogger("PipeDreams_startup")
logger.setLevel(logging.DEBUG)

# create file handler which logs even debug messages
fh = logging.FileHandler(f'pipedreams/admin/logs/{userName}_DreamLOG.log')
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
            pipeline_config
            ):
    """ sets system paths to env and other tools like ffmpeg """

    maya_version = pipeline_config["maya_version"]

    try:
        py_version = get_the_PY(Python_dir)
    except FileNotFoundError:
        py_version = None

    if py_version != None:

        logger.info(f"Python Versin: {py_version}")

        # set path to /autodesk/maya/bin our function can find mayapy to pip install packages.
        ProgramFiles_path = os.environ["ProgramFiles"]
        mayapy_path = f"{ProgramFiles_path}/Autodesk/Maya{str(maya_version)}/bin"

        # set paths to default python.
        python_interpreter = f"{Python_dir}/{py_version}"
        python_scripts = f"{python_interpreter}/Scripts"

        # set sys env paths
        sys.path.append(launch_dir)
        os.environ['PATH'] += os.pathsep + ffmpeg_dir
        os.environ['PATH'] += os.pathsep + python_interpreter
        os.environ['PATH'] += os.pathsep + python_scripts
        os.environ['PATH'] += os.pathsep + mayapy_path        

        logger.info("*** Set paths:")
        logger.info(ffmpeg_dir)
        logger.info(python_interpreter)
        logger.info(python_scripts)
        logger.info(mayapy_path)





def install_Python(appdata_Python_dir):
    """ Install / coppies over a version of Python, it first tries to copy over python if it exists in pipedream /pipeline/tools/Python directory
        If not, it will then attempt to install it from the internet.
    """

    text = f"No Python found, installing Python \n-{appdata_Python_dir}"
    ctypes.windll.user32.MessageBoxW(0, text, "PipeDreams", 0)

    logger.info("copying Python fils, This may take awhile.")

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
        logger.info("** Python does not exist")
        time.sleep(2)
        install_Python(Python_dir)

    else:
        logger.info("Python exists.")




def check_Python_packages(PIPEDREAMS_DIR, pipeline_config):
    """ checks and makes sure system python has all the packages needed to run Pipedreams. """

    maya_version = pipeline_config["maya_version"]

    # System default Python
    os.system(f"pip install -r {PIPEDREAMS_DIR}/pipedreams/admin/requirements/system_requirements.txt")
    time.sleep(2)

    # Maya Python
    path = f"mayapy -m pip install -r {PIPEDREAMS_DIR}/pipedreams/admin/requirements/maya_requirements.txt"
    os.system(path)
    time.sleep(2)




def get_UI_toolBar_config(PIPEDREAMS_DIR):
    """ returns either pipeline forced defaults or user preferences. """

    pipeline_config = yaml_config(f"{PIPEDREAMS_DIR}/pipedreams/admin/pipeline_config.yaml")
    allow_user_preferences = pipeline_config["allow_user_preferences"]


    if allow_user_preferences == False:
        UI_toolBar_config = f"{PIPEDREAMS_DIR}/pipedreams/admin/UI_toolBar.yaml"
    elif allow_user_preferences == True:
        UI_toolBar_config = get_user_preferences(PIPEDREAMS_DIR)

    config = yaml_config(UI_toolBar_config)

    return(config)




def get_user_preferences(PIPEDREAMS_DIR):
    """ returns user preferences, creates it if it does not exist. """

    userName = os.environ['COMPUTERNAME']
    user_prefs = f"{PIPEDREAMS_DIR}/pipedreams/admin/data/user_preferences/{userName}_preferences.yaml"

    if os.path.exists(user_prefs) != True:

        UI_toolBar_config = yaml_config(f"{PIPEDREAMS_DIR}/pipedreams/admin/UI_toolBar.yaml")
        with open(user_prefs, 'w') as file:
            yaml.dump(UI_toolBar_config, file)

    return(user_prefs)




def launch_pipedreams(launch_dir, PIPEDREAMS_DIR):
    """ launches pipedreams tools. """

    MINIMIZED_TRAYICON = get_UI_toolBar_config(PIPEDREAMS_DIR)["MINIMIZED_TRAYICON"]
    
    # Launches the icon either minimized or on the side of the monitor.
    try:
        if MINIMIZED_TRAYICON == False:
            logger.info("*** Launching PipeDreams Tool Bar.")
            os.startfile(f"{launch_dir}/UI_trayIcon.pyw")
        elif MINIMIZED_TRAYICON == True:
            logger.info("*** Launching PipeDreams Minimized Tray Icon.")
            os.startfile(f"{launch_dir}/UI_trayIcon_mini.pyw")
    except Exception as e:
        logger.info(str(e))




def yaml_config(config_path):
    """ Open yaml configs. """
    config = yaml.safe_load(open(config_path))
    return(config)




def startup():
    """ Fist startup for Pipedreams """

    userName = os.environ['COMPUTERNAME']

    PIPEDREAMS_DIR = os.path.dirname(sys.argv[0])
    launch_dir = f"{PIPEDREAMS_DIR}/pipedreams/launch"

    # # paths to tools.
    ffmpeg_dir = f"{PIPEDREAMS_DIR}/pipedreams/pipeline/tools/ffmpeg"

    usr_data_dir = f"{PIPEDREAMS_DIR}/pipedreams/admin/data/user_data_base"
    pipeline_config = yaml_config(f"{PIPEDREAMS_DIR}/pipedreams/admin/pipeline_config.yaml")

    
    appdata_path = os.path.dirname(os.getenv('APPDATA'))
    Python_dir = f"{appdata_path}/Local/Programs/Python"

    logger.info(f"{userName} : PipeDreams Startup .. ")
    # check if user exists in database directory, if not, check if default Python is installed.
    if os.path.exists(f"{usr_data_dir}/{userName}.json") != True:
        logger.info(f"\n*** User {userName} not in database, setting up:")
        time.sleep(5)
        check_Python(Python_dir)
        path_set(launch_dir, ffmpeg_dir, Python_dir, pipeline_config)
        check_Python_packages(PIPEDREAMS_DIR, pipeline_config)
    else:
        pass


    path_set(
            launch_dir, 
            ffmpeg_dir, 
            Python_dir, 
            pipeline_config
            )


    launch_pipedreams(launch_dir, PIPEDREAMS_DIR)



if __name__ == "__main__":

    startup()


