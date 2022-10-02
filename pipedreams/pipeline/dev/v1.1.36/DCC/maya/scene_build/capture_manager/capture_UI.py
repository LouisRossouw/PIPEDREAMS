import os
import sys
import yaml

import maya.cmds as cmds

import scene_build.capture_manager.capture_util as capture_utils



def capture_UI():
    """ Starts up the capture UI """




    def config_check():
        """ checks project data config for info on the working project """

        config_path = os.path.dirname(os.getenv("TOP_ASSETS")) + "/data/pipeline/pipeline_data.yaml"
        config = yaml.safe_load(open(config_path))

        return(config)




    def clearOptionMenu(optionMneu_path):
        """ pass the optionMenu and it will clear all the items """

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

        captures_path = os.getenv("CAPTURES")
        UI_optionMenu_path = data["UI_version_menu"]
        UI_task_path = data["UI_task"]
        UI_captureName_path = data["UI_captureName_path"]


        try:
            input_name = args[0]

        except IndexError:
            input_name = cmds.textField(UI_captureName_path, query=True, text=True)

        Task_name = cmds.optionMenu(UI_task_path, query=True, value=True)

        clearOptionMenu(UI_optionMenu_path)

        path_to_capture_dir = captures_path + "/" + Task_name + "/" + input_name

        for v in versioning(path_to_capture_dir)[1]:
            cmds.menuItem(label=v, parent=UI_optionMenu_path)




    def UI_update_existing(*args):
        """ Updates / populates the UI Existing optionMenu"""

        UI_Existing_path = data["UI_Existing_path"]

        try:
            clearOptionMenu(UI_Existing_path)
            task_dir = capture_path + "/" + cmds.optionMenu(UI_task_path, query=True, value=True)

            for existing in os.listdir(task_dir):
                cmds.menuItem(existing, parent=UI_Existing_path)

        except Exception as e:
            clearOptionMenu(UI_Existing_path)

        update_version()




    def UI_update_captureName(*args):
        """ updates the Captures name text field on command change """

        cmds.textField(UI_captureName_path, edit=True, text=args[0])




    def capture_button(*args):
        """ This button executes the capture with the required settings inputted on the UI """

        capture_name_eval = cmds.textField(UI_captureName_path, query=True, text=True)
        start_number_eval = cmds.intField(UI_start, query=True, value=True)
        end_number_eval = cmds.intField(UI_end, query=True, value=True)
        task_name_eval = cmds.optionMenu(UI_task_path, query=True, value=True)
        export_path_eval = cmds.textField(UI_save_path, query=True, text=True)

        #radio buttons
        selected_output_group = cmds.radioCollection(output, query=True, sl=True)
        selected_output = cmds.radioButton(selected_output_group, query=True, label=True)

        UI_version_eval = cmds.optionMenu(UI_version_menu, query=True, value=True)

        UI_publish_eval = cmds.checkBox(UI_publish, query=True, value=True)
        UI_guides_eval = cmds.checkBox(UI_guides, query=True, value=True)
        UI_GS_eval = cmds.checkBox(UI_GS, query=True, value=True)
        UI_comment_eval = cmds.textField(UI_comment, query=True, text=True)

        # Run capture process
        capture_utils.capture_run(
                                  capture_name_eval,
                                  start_number_eval,
                                  end_number_eval,
                                  task_name_eval,
                                  export_path_eval,
                                  selected_output,
                                  UI_version_eval,
                                  UI_publish_eval,
                                  UI_guides_eval,
                                  UI_GS_eval,
                                  UI_comment_eval,
                                  config_data
                                  )




# Builds UI

    config_data = config_check()

    try:
        publisher_active = config_data["Publisher"]
        guides_active = config_data["Guides"]
    except KeyError:
        publisher_active = False
        guides_active = False

    data = {}

    if cmds.window('Capture_Manager', exists=True):
        cmds.deleteUI('Capture_Manager')

    window = cmds.window("Capture_Manager", widthHeight=(100, 100))


# Save path
    capture_setup = cmds.columnLayout( adjustableColumn=True )
    cmds.frameLayout(label='capture_setup', cll=True, mh=10,bgc=(0.22,0.22,0.22))
    cmds.gridLayout( numberOfColumns=2, cellWidthHeight=(150, 20) )


    cmds.text(label="Save_path:")
    UI_save_path = cmds.textField(text=os.getenv("CAPTURES"))

    cmds.text(label="Task:")
    UI_task_path = cmds.optionMenu(changeCommand=UI_update_existing)
    cmds.menuItem("anim")
    cmds.menuItem("previz")

    cmds.setParent( '..' )
    cmds.separator(height=10, style='in')


# Capture naming
    cmds.gridLayout( numberOfColumns=2, cellWidthHeight=(150, 20) )

    capture_path = os.getenv("CAPTURES")
    cmds.text(label="Existing:")

    UI_Existing_path = cmds.optionMenu(changeCommand=UI_update_captureName)
    # UI_update_existing(UI_Existing_path)

    cmds.text(label="Capture Name:")
    UI_captureName_path = cmds.textField(text=os.getenv("SHOT"), changeCommand=update_version)
    cmds.text(label="Version:")
    UI_version_menu = cmds.optionMenu()




    cmds.setParent( '..' )
    cmds.separator(height=10, style='in')


# frame ranges
    cmds.gridLayout(numberOfColumns=2, cellWidthHeight=(150, 20))

    cmds.text(label="Start:")
    UI_start = cmds.intField(value=int(cmds.playbackOptions(q=True, min=True)))
    cmds.text(label="End:")
    UI_end = cmds.intField(value=int(cmds.playbackOptions(q=True, max=True)))

    cmds.setParent('..')
    cmds.separator(height=10, style='in')


# Options
    cmds.gridLayout(numberOfColumns=5, cellWidthHeight=(70, 20))

    UI_publish = cmds.checkBox("Publish", value=publisher_active)
    UI_guides = cmds.checkBox("Guides", value=guides_active)
    UI_GS = cmds.checkBox("GS")

    output = cmds.radioCollection()
    mp4 = cmds.radioButton(label='mp4', select=True)
    png = cmds.radioButton(label='png')

    cmds.setParent('..')
    cmds.separator(height=10, style='in')


# comments
    cmds.text(label='comment:')
    UI_comment = cmds.textField()

    # Creates Capture
    cmds.button(label='Capture',bgc=(0.65, 1, 0), command=capture_button)


# Add menu path to dictionary
    data["UI_version_menu"] = UI_version_menu
    data["UI_task"] = UI_task_path
    data["UI_captureName_path"] = UI_captureName_path
    data["UI_Existing_path"] = UI_Existing_path
    data["UI_comment"] = UI_comment


    UI_update_existing()

    cmds.showWindow(window)





if __name__ == '__main__':

    root = "C:\\custom_program_files\\pipeline\\PipeDreams\\"
    sys.path.append(root)
    capture_UI()
    #