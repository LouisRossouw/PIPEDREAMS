import os
import sys

import maya.cmds as cmds





def capture_UI():


    if cmds.window('Capture_Manager', exists=True):
        cmds.deleteUI('Capture_Manager')

    window = cmds.window("Capture_Manager", widthHeight=(100, 100))


# Save path
    capture_setup = cmds.columnLayout( adjustableColumn=True )
    cmds.frameLayout(label='capture_setup', cll=True, mh=10,bgc=(0.22,0.22,0.22))
    cmds.gridLayout( numberOfColumns=2, cellWidthHeight=(150, 20) )


    cmds.text(label="Save_path:")
    cmds.textField(text=os.getenv("CAPTURES"))

    cmds.text(label="Task:")
    cmds.optionMenu()
    cmds.menuItem("anim")
    cmds.menuItem("previz")

    cmds.setParent( '..' )
    cmds.separator(height=10, style='in')


# Capture naming
    cmds.gridLayout( numberOfColumns=2, cellWidthHeight=(150, 20) )

    cmds.text(label="Existing:")

    cmds.optionMenu()
    cmds.menuItem("bxx_010")
    cmds.text(label="Capture Name:")
    cmds.textField(text=os.getenv("SHOT"))
    cmds.text(label="Capture Name:")
    cmds.optionMenu()
    cmds.menuItem("v001")

    cmds.setParent( '..' )
    cmds.separator(height=10, style='in')

# frame ranges
    cmds.gridLayout(numberOfColumns=2, cellWidthHeight=(150, 20))

    cmds.text(label="Start:")
    cmds.textField(text=int(cmds.playbackOptions(q=True, min=True)))
    cmds.text(label="End:")
    cmds.textField(text=int(cmds.playbackOptions(q=True, max=True)))

    cmds.setParent('..')
    cmds.separator(height=10, style='in')


# Options
    cmds.gridLayout(numberOfColumns=5, cellWidthHeight=(70, 20))

    cmds.checkBox("Publish")
    cmds.checkBox("Guides")
    cmds.checkBox("GS")

    output = cmds.radioCollection()
    mp4 = cmds.radioButton(label='mp4', select=True)
    png = cmds.radioButton(label='png')

    cmds.setParent('..')
    cmds.separator(height=10, style='in')


# comments
    cmds.text(label='comment:')
    comment = cmds.textField()

    # Creates Capture
    cmds.button(label='Capture',bgc=(0.65, 1, 0))



    cmds.showWindow(window)


if __name__ == '__main__':

    root = "C:\\custom_program_files\\pipeline\\PipeDreams\\"
    sys.path.append(root)
    capture_UI()