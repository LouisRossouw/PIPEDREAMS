""" This script starts up the UI trayicon either with the systems local default python in /appdata/local/programms/python
    or the portable python iterpreter that is located /pipedreams/pipeline/tools/Python
"""

import os
import sys



def get_the_PY(PIPEDREAMS_DIR):
    """ returns the python version nam being used in the /pipedreams/pipeline/tools/Python directory -
        incase there is a unique python version.
    """
    python_dir = f"{PIPEDREAMS_DIR}/pipedreams/pipeline/tools/Python"
    pyname = os.listdir(python_dir)[0]

    return(pyname)


def path_set(
            launch_dir, 
            ffmpeg_dir, 
            python_interpreter, 
            python_scripts
            ):
    """ sets system paths to env and other tools like ffmpeg """

    # set sys env paths
    sys.path.append(launch_dir)
    os.environ['PATH'] += os.pathsep + ffmpeg_dir
    os.environ['PATH'] += os.pathsep + python_interpreter
    os.environ['PATH'] += os.pathsep + python_scripts


def run():
    """ Startsup the Pipeline tools. """

    this_directory = os.path.dirname(__file__)
    PIPEDREAMS_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

    launch_dir = f"{PIPEDREAMS_DIR}/pipedreams/launch"
    launch_trayIcon = f"{launch_dir}/UI_trayIcon.pyw"

    # paths to tools.
    ffmpeg_dir = f"{PIPEDREAMS_DIR}/pipedreams/pipeline/tools/ffmpeg"

    # Portable Python if exists.
    python_interpreter = f"{PIPEDREAMS_DIR}/pipedreams/pipeline/tools/Python/{get_the_PY(PIPEDREAMS_DIR)}"
    python_scripts = f"{python_interpreter}/Scripts"

    launch_trayIcon = f"{this_directory}/UI_trayIcon.pyw"

    # Set paths
    path_set(
            launch_dir, 
            ffmpeg_dir, 
            python_interpreter, 
            python_scripts
            )

    # Check if Virtual env
    print("Virtual env active: ", bool(os.getenv("VIRTUAL_ENV")))

    # start UI icon (UI_trayIcon.pyw)
    os.startfile(launch_trayIcon)










if __name__ == "__main__":

    run()
