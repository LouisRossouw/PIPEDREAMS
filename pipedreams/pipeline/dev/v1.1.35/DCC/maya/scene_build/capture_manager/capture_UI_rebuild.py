import os
import sys

import maya.cmds as cmds





def capture_UI():



    def clearOptionMenu(optionMneu_path):
        """ pass the optionmenu and it will clear all the items """

        # loop through existing menus in the optionMenu and destroy them
        for item in cmds.optionMenu(optionMneu_path, q=True, ill=True) or []:
            cmds.deleteUI(item)


    def versioning(path_to_dir):
        """ This function returns the current version and the next version number """

        try:
            list_contents = os.listdir(path_to_dir)

            if bool(list_contents) == False:
                latest_version = "v001"

                new_version = "v001"
                current_version = "v001"
                list_contents = ["v001"]

            elif bool(list_contents) == True:
                sort = sorted(list_contents, reverse=True)
                latest_version = sort[0]

                chop_name_end = latest_version[-3:]

                latest_version = int(chop_name_end)
                new_version_num = latest_version + 1

                new_version = ('v{0:03d}'.format(new_version_num))
                current_version = ('{0:03d}'.format(latest_version))

                list_contents.append(new_version)
            version_list = sorted(list_contents, reverse=True)

        except FileNotFoundError:
            new_version = ["v001"]
            version_list = ["v001"]

        return (new_version, version_list)




    def update_version(*args):
        """ Updates version on capture name field change update """

        input_name = args[0]
        captures_path = os.getenv("CAPTURES")
        UI_optionMenu_path = data["UI_version_menu"]
        UI_task_path = data["UI_task"]

        Task_name = cmds.optionMenu(UI_task_path, query=True, value=True)

        clearOptionMenu(UI_optionMenu_path)

        path_to_capture_dir = captures_path + "/" + Task_name + "/" + input_name

        for v in versioning(path_to_capture_dir)[1]:
            cmds.menuItem(label=v, parent=UI_optionMenu_path)

        # # changes the version option menu to whatever
        # cmds.optionMenu(data["UI_version_menu"], edit=True, value="latet_version")

# Build UI

    data = {}

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
    UI_task_path = cmds.optionMenu()
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
    cmds.textField(text=os.getenv("SHOT"), changeCommand=update_version)
    cmds.text(label="Version:")
    UI_version_menu = cmds.optionMenu()
    # cmds.menuItem("v001")




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


# Add menu path to dictionary
    data["UI_version_menu"] = UI_version_menu
    data["UI_task"] = UI_task_path


    cmds.showWindow(window)


if __name__ == '__main__':

    root = "C:\\custom_program_files\\pipeline\\PipeDreams\\"
    sys.path.append(root)
    capture_UI()