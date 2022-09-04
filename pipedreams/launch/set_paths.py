import os
import sys

this_directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

launch_dir = f"{this_directory}/pipedreams/launch"
launch_trayIcon = f"{launch_dir}/UI_trayIcon.pyw"
ffmpeg_dir = f"{this_directory}/pipedreams/pipeline/tools/ffmpeg"

python_interpreter = f"{this_directory}/Python/Python310"
python_scripts = f"{this_directory}/Python/Scripts"

def path_set():
    """ sets system paths to env and other tools like ffmpeg """

    # set sys env paths
    sys.path.append(launch_dir)
    os.environ['PATH'] += os.pathsep + ffmpeg_dir
    os.environ['PATH'] += os.pathsep + python_interpreter
    os.environ['PATH'] += os.pathsep + python_scripts

if __name__ == "__main__":

    print("Virtual env active: ", bool(os.getenv("VIRTUAL_ENV")))
