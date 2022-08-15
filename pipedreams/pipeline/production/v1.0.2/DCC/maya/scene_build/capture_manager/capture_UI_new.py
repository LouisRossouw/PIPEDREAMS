import os
import sys

import imp

import pymel.core as pm
import maya.cmds as cmds

import scene_build.capture_manager.capture as capture
import scene_build.export_manager.export_utils as utils

PipeDreams_root_path = os.getenv('PIPELINE_ROOT')
sys.path.append(PipeDreams_root_path)


import toolUtils.ffmpeg as ffmpeg_convert



# This is the UI that gets created
def capture_UI():


    # functions for the UI (buttons etc)
    def capture_button(*args):
        """ This button executes the capture with the required settings inputted on the UI """

        capture_name = pm.textField(capture_name_input, query=True, text=True)
        start_number = pm.intField(start_frame, query=True, value=True)
        end_number = pm.intField(end_frame, query=True, value=True)
        task_name = pm.optionMenu(task, query=True, value=True)
        export_path_eval = pm.textField(save_path, query=True, text=True)
        #radio buttons
        selected_output_group = pm.radioCollection(output, query=True, sl=True)
        selected_output = pm.radioButton(selected_output_group, query=True, label=True)
        ##
        version_eval = pm.textField(version, query=True, text=True)
        overlay_checkbox = pm.checkBox(overlay, query=True, value=True)
        greenScreen_checkbox = pm.checkBox(green_screen, query=True, value=True)
        comment_eval = pm.textField(comment, query=True, text=True)
        resolution_eval = pm.optionMenu(resolution, query=True, value=True)


        capture.capture_view(capture_name,
                             start_number,
                             end_number,
                             task_name,
                             export_path_eval,
                             selected_output,
                             version_eval,
                             overlay_checkbox,
                             comment_eval,
                             greenScreen_checkbox,
                             )

        if greenScreen_checkbox == True:
            name = task_name + '_' + capture_name + '_' + version_eval
            path_to_png_sequence_input = export_path_eval + '\\' + task_name + '\\' + capture_name + '\\' + version_eval

            ffmpeg_convert.maya_green_screen(path_to_png_sequence_input, name, selected_output)


        # Rechecks and updates the version number in UI
        check_version()



    main_dir_path = os.getenv('PROJECT_NAME')
    shot = os.getenv('SHOT')


    def get_capture_items(*args):
        """ This collects the captured names that already exist """

        try:
            export_path_eval = pm.textField(save_path, query=True, text=True)
            task_name = pm.optionMenu(task, query=True, value=True)

            ls_captures = os.listdir(export_path_eval + '\\' + task_name)
        except FileNotFoundError:
            ls_captures = ''

        return ls_captures


    def capture_menu(item):
        """ this sets the capture name text field """
        pm.textField( capture_name_input, edit=True, text=item )

        check_version()



    def task_menu(*args):
        """ this sets the capture name text field """

        # Clears existing menu items
        for i in pm.optionMenu(captures, q=True, ill=True):
            pm.deleteUI(i)

        ls = get_capture_items()

        # Adds new menuItems
        for x in ls:
            pm.menuItem(captures, label=x)

        comment_eval = pm.textField(comment, query=True, text=True)
        r = '"' + comment_eval + '"'
        print(r)


    def enter_textField(*args):
        """ after the capture_name is entered by user, this command runs """

        check_version()

        print('test')


    def check_version():
        """ Checks version """
        print('checking version')

        capture_name = pm.textField(capture_name_input, query=True, text=True)
        start_number = pm.intField(start_frame, query=True, value=True)
        end_number = pm.intField(end_frame, query=True, value=True)
        task_name = pm.optionMenu(task, query=True, value=True)
        export_path_eval = pm.textField(save_path, query=True, text=True)
        selected_output = pm.radioCollection(output, query=True, sl=True)

        path = export_path_eval + '\\' + task_name + '\\' + capture_name

        try:
            old_version = utils.versioning(path)[0]
            new_version = utils.versioning(path)[1]
        except FileNotFoundError:
            new_version = '001'

        pm.textField(version, edit=True, text='v' + new_version)









    # UI
    if pm.window('Capture', exists=True):
        pm.deleteUI('Capture')

    window = pm.window(title='Capture', widthHeight=(350, 380) )

    pm.columnLayout(adjustableColumn=True)
    pm.frameLayout(label='Capture_setup', borderStyle='etchedOut', cll=True, mh=10, )
    pm.rowColumnLayout(numberOfColumns=2, columnAttach=(1, 'right', 0), columnWidth=[(10, 100), (2, 250)])


    pm.text( label='Save_path :' )
    item = os.getenv('CAPTURES')
    save_path = pm.textField(text=item )




    pm.text( label='Task :' )
    task = pm.optionMenu(changeCommand=task_menu)
    pm.menuItem( label='anim' )
    pm.menuItem( label='previs' )
    pm.text( label='' )


    pm.setParent( '..' )
    pm.separator( height=10, style='in' )

    pm.columnLayout(adjustableColumn=True)
    pm.rowColumnLayout(numberOfColumns=3, columnAttach=(1, 'left', 1), columnWidth=[(10, 100), (30, 25)])
    pm.text(label='Capture_Name : ', )
    name = pm.textField(cc=enter_textField)
    capture_name_input = pm.textField(name, edit=True, font='tinyBoldLabelFont', text=shot)


    version = pm.textField(text='')

    pm.text(label='', )

    # # drop down menu, also sets the capture name text field
    captures = pm.optionMenu(changeCommand=capture_menu)

    for x in get_capture_items():
        pm.menuItem(captures, label=x )

    pm.setParent( '..' )

    # version = pm.optionMenu(label='version')
    # pm.menuItem(version, label='v001')

    pm.separator( height=10, style='in' )
    pm.setParent( '..' )

    pm.rowColumnLayout(numberOfColumns=2, columnWidth=[(100, 100), (20, 50)])

    pm.text( label='Resolution :' )
    resolution = pm.optionMenu()
    pm.menuItem( label='1080p' )
    pm.menuItem( label='720p' )
    pm.menuItem(label='480p')

    pm.text( label='Start_frame :' )
    start = cmds.playbackOptions(q=True, min=True)
    start_frame = pm.intField(v=start)

    pm.text( label='End_frame :' )
    end = cmds.playbackOptions(q=True, max=True)
    end_frame = pm.intField(v=end)

    pm.setParent( '..' )
    pm.separator( height=10, style='in' )



    pm.rowColumnLayout(numberOfColumns=4,)

    overlay = pm.checkBox(label='overlay', value=True)
    green_screen = pm.checkBox(label='green screen', value=False)

    output = pm.radioCollection()
    mp4 = pm.radioButton(label='mp4', select=True)
    png = pm.radioButton(label='png')

    pm.setParent( '..' )
    pm.separator( height=10, style='in' )



    pm.text(label='comment:')
    comment = pm.textField()


    pm.setParent( '..' )


    # Creates Capture
    pm.button(label='Capture',bgc=(0.65, 1, 0), command=capture_button)

    pm.setParent( '..' )

    get_capture_items()
    check_version()

    pm.showWindow(window)


if __name__ == '__main__':

    root = "C:\\custom_program_files\\pipeline\\PipeDreams\\"
    # this_file = os.path.abspath(__file__)
    # p = (os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(root)))))
    sys.path.append(root)

    capture_UI()