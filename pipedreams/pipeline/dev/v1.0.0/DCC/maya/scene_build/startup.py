import os

import random

import maya.mel as mel
import maya.cmds as cmds
import pymel.core as pm




def startup_build():
    """ this function sets Maya up the way i like it on startup """
 
    print("******** Running latest v1.0.0")

    # Set unique scene ID
    unique_ID = str(random.randint(1, 1000000))
    cmds.fileInfo('sceneID', unique_ID)



    # display info
    project_name = os.getenv("PROJECT_NAME")
    print('Shot set to : ' + str(project_name))
    pm.inViewMessage( amg='Shot set to : ' + str(project_name), pos='midCenter', fade=True )
    pm.headsUpDisplay( project_name, section=1, block=0, blockSize='medium', label=project_name, labelFontSize='large')


    # set to animation
    pm.setMenuMode('animationMenuSet')



    # Time
    cmds.currentUnit(time='ntsc')

    cmds.playbackOptions(animationStartTime=1)
    cmds.playbackOptions(animationEndTime=100)

    try:
        save_file = os.getenv('MAYA_USR')
        maya_dir = save_file
        mel.eval('setProject \"' + maya_dir + '\"')

    except Exception:
        pass

    # layout and camera

    # panel = cmds.getPanel(wf=1)
    # cmds.modelEditor(panel, e=1, allObjects=0)
    # cmds.modelEditor(panel, e=1, polymeshes=1)
    # cmds.modelEditor(panel, e=1, xray=0)
    # cmds.modelEditor(panel, e=1, displayTextures=1)
    # cmds.modelEditor(panel, e=1, displayLights='all')