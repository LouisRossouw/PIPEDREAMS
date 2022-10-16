import os

import random

import art
import yaml
from pathlib import Path

import maya.mel as mel
import maya.cmds as cmds
import pymel.core as pm

import scene_build.toolBar_UI as toolBar_UI
import scene_build.simple_UI as Simple_UI



def startup_build():
    """ this function sets Maya up the way i like it on startup """

    art.tprint("Pipeline_v_" + pipeline_version())
    print("\n\n* * * Pipeline version: ", pipeline_version())
    print("\n\n **** www.LouisRossouw.com")


    PIPELINE_DATA = get_pipeline_data()
    PIPELINE_CONFIG = return_pipeline_config()

    # Set unique scene ID
    unique_ID = str(random.randint(1, 1000000))
    cmds.fileInfo('sceneID', unique_ID)

    # display info
    project_name = os.getenv("PROJECT_NAME")
    print('Shot set to : ' + str(project_name))
    pm.inViewMessage( amg='Shot set to : ' + str(project_name), pos='midCenter', fade=True )
    # pm.headsUpDisplay( project_name, section=1, block=0, blockSize='medium', label=project_name, labelFontSize='large')


    try:
        save_file = os.getenv('MAYA_USR')
        maya_dir = save_file
        mel.eval('setProject \"' + maya_dir + '\"')

    except Exception:
        pass


    # set to animation
    pm.setMenuMode('animationMenuSet')

    # Set FPS
    set_MAYA_time(PIPELINE_DATA)

    # Resolution
    set_MAYA_Resolution(PIPELINE_DATA)

    # Set Range
    cmds.playbackOptions(animationStartTime=1, minTime=1)
    cmds.playbackOptions(animationEndTime=100, maxTime=100)


    # Load Pipeline UI
    if PIPELINE_CONFIG["maya_UI_type"] == "toolBar":
        toolBar_UI.ToolBar()

    if PIPELINE_CONFIG["maya_UI_type"] == "simple":
        Simple_UI.start_UI()


    # Start ScrictJobs
    start_ScriptJob()




def return_pipeline_config():
    """ Return the Pipeline config. """

    main_path = Path(os.getenv('PIPELINE_ROOT')).parents[2]
    config_path = (f"{main_path}/admin/pipeline_config.yaml")
    file_data = yaml.safe_load(open(config_path, 'r'))
    return file_data




def pipeline_version():
    """ returns the current version of the pipline based on top directory """
    pipeline_version = os.path.basename((os.getenv('PIPELINE_ROOT')))
    return(pipeline_version)




def yaml_config(config_path):
    """ Open yaml configs """
    config = yaml.safe_load(open(config_path))
    return(config)




def get_pipeline_data():
    """ returns the pipeline data for the project and opens it as a yaml file """
    project_data = os.path.dirname(os.getenv("TOP_ASSETS")) + "/data"
    pipeline_data = (project_data) + "/pipeline/pipeline_data.yaml"
    return(yaml_config(pipeline_data))




def set_MAYA_Resolution(PIPEDATA):
    """ Sets Mayas aspect resolution to the projects set resolution """

    apsect_ratio = PIPEDATA["ASPR"]
    resolution = PIPEDATA["Resolution"].split("x")

    if apsect_ratio == "16x9":
        width_X = resolution[0]
        width_Y = resolution[1]
    elif apsect_ratio == "9x16":
        width_X = resolution[1]
        width_Y = resolution[0]

    cmds.setAttr("defaultResolution.width", int(width_X))
    cmds.setAttr("defaultResolution.height", int(width_Y))




def set_MAYA_time(PIPEDATA):
    """ Sets Mayas FPS to the current project """

    FPS = PIPEDATA["FPS"]

    if FPS == 30:
        time_name = "ntsc"
    elif FPS == 25:
        time_name = "pal"
    elif FPS == 24:
        time_name = "film"
    else:
        time_name = "ntsc"

    cmds.currentUnit(time=time_name)




def start_ScriptJob():
    """ Starts scriptJobs. """
    pass






if __name__ == "__main__":

    startup_build()