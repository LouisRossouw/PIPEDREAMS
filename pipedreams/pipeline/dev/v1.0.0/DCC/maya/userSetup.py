import os
import sys

import maya.cmds as cmds
from pymel import mayautils

PipeDreams_root_path = os.getenv('PIPELINE_ROOT')
sys.path.append(f"{PipeDreams_root_path}/DCC/maya")

import scene_build.RockettotheskiesUI as UI
import scene_build.startup as startup





def pipedreams_startup():
    """ simply a startup message printout """

    print("***  *    *    *   PipeDreams starting up pew")


pipedreams_startup()


# Open new ports to connect VS, # Nomachine uses port 7001, need to close that
try:
    if not cmds.commandPort(":4434", query=True):
        cmds.commandPort(name=":4434")
except RuntimeError:
    pass

try:
    cmds.commandPort(name=":7001", sourceType="mel", echoOutput=True)
    cmds.commandPort(name=":7002", sourceType="python", echoOutput=True)
    #commandPort -name "localhost:7001" -sourceType "mel" -echoOutput;
except RuntimeError:
    pass



# setsup Maya the way i want it
cmds.evalDeferred(startup.startup_build)

# # starts menu
cmds.evalDeferred(UI.rocketothesky)

cmds.evalDeferred(pipedreams_startup)

mayautils.executeDeferred(pipedreams_startup)



if __name__ == "__main__":

    pipedreams_startup()