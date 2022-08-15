import os
import pymel.core as pm
import maya.cmds as cmds







def ChopChop_UI():
    """ ChopChop is a tool to chop the start and end frame of run/walk cycles """



    def ChopChop(*args):
        """ This function sets a key at start and end frame and deletes the rest """

        selected = cmds.ls(sl=True, long=True)

        start_frame = pm.intField(start_field, query=True, value=True)
        end_frame = pm.intField(end_field, query=True, value=True)

        cmds.currentTime(start_frame, edit=True)

        all_keys = sorted(cmds.keyframe(selected, q=True) or [])

        cmds.setKeyframe(selected, insert=4)

        cmds.copyKey(selected, time=(start_frame, start_frame))
        cmds.pasteKey(selected, time=(end_frame, end_frame))

        cmds.cutKey(selected, time=(start_frame - 1, -999), option="keys")
        cmds.cutKey(selected, time=(end_frame + 1, end_frame + 999), option="keys")




## UI

    project_name = os.getenv('PROJECT_NAME')
    window_title = 'ChopChop || ' + str(project_name)

    cmds.window(title=window_title, widthHeight=(400, 100), menuBar=True)

    # pm.frameLayout()
    pm.columnLayout(adjustableColumn=True)
    pm.rowColumnLayout(numberOfColumns=2, columnAttach=(1, 'right', 0), columnWidth=[(10, 100), (2, 250)])

    start_frame = cmds.playbackOptions(q=True, min=True)
    end_frame = cmds.playbackOptions(q=True, max=True)


    pm.text(label='start')
    start_field = pm.intField('start_int', v=start_frame)

    pm.text(label='end')
    end_field = pm.intField('end_int', v=end_frame)

    pm.setParent( '..' )

    pm.columnLayout(adjustableColumn=True)

    pm.button(label='ChopChop',bgc=(0.65, 1, 0), command=ChopChop)

    cmds.setParent('..', menu=True)




    cmds.showWindow()









if __name__ == '__main__':

    ChopChop_UI()