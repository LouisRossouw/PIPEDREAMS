import os
import maya.cmds as cmds

import scene_build.startup as startup



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


# Start the custom Maya tools.
cmds.evalDeferred(startup.startup_build)





if __name__ == "__main__":
    pass