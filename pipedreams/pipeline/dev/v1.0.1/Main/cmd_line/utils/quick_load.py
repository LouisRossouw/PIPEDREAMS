import os
import json

def quick_load(Documents_pipeline_dir):
    """ This function runs after a shortcut is entered into the cmd line to open certain files quicker based on last-save """

    maya_quickload_path = f'{Documents_pipeline_dir}\\data\\maya_quickload.json'

    with open(maya_quickload_path, 'r') as f:
        maya_quickload_json = json.load(f)

    return(maya_quickload_json)




















if __name__ == '__main__':
    quick_load()
