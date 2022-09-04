""" This file needs to be converted to a .exe and shared as a shortcut to other users machines,

    - it checks the pipeline_config and chooses to launch the pipeline with the local default Python interpreter
    or the portable Python interpreter that lives in the /pipedreams/pipeline/tools/Python directory.
"""

import os
import pipedreams.launch.utils as utils


this_dir = os.path.dirname(__file__)

pipeline_config = utils.yaml_config(f"{this_dir}/pipedreams/admin/pipeline_config.yaml")
Python_interpreter_type = pipeline_config["Python_interpreter_type"]

# based on pipeline_config settings - choose to either launch with default local Python version or
# the portable Python version found in /pipedreams/pipeline/tools/Python directory.

try:

    if Python_interpreter_type == "system":
        os.startfile(f"{this_dir}/pipedreams/launch/run.pyw")
    if Python_interpreter_type == "portable":
        os.startfile(f"{this_dir}/run.bat")

except Exception as error:
    
    print("*** PipeDreams encounted an error: ")
    print("\n\n")
    print(error)