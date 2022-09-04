""" This script starts up the UI trayicon either with the systems local default python in /appdata/local/programms/python
    or the portable python iterpreter that is located /pipedreams/pipeline/tools/Python
"""

import os
import yaml
import set_paths as set_paths


def open_PipeLine_Config():
    """ opens the pipeline_config """

    # Open config
    config_path = os.path.abspath(__file__)
    config_path_dir = (f"{os.path.dirname(os.path.dirname(config_path))}")
    config = yaml.safe_load(open(f'{os.path.dirname(config_path_dir)}/PipeDreams/admin/pipeline_config.yaml', 'r'))

    return(config)


this_directory = os.path.dirname(__file__)

launch_trayIcon = f"{this_directory}/UI_trayIcon.pyw"
pipeline_path = os.path.dirname(os.path.dirname(__file__))
print(pipeline_path)
## Run ##

# Set paths
set_paths.path_set()

# Start dream environment
print("Virtual env active: ", bool(os.getenv("VIRTUAL_ENV")))

# start UI icon (UI_trayIcon.pyw)
Python_interpreter_type = open_PipeLine_Config()["Python_interpreter_type"]

if Python_interpreter_type == "portable":
    python_int = f"{pipeline_path}/pipeline/tools/Python/Python310/python.exe "
    os.system("START /B " + python_int + " " + launch_trayIcon)
elif Python_interpreter_type == "system":
    os.startfile(launch_trayIcon)
