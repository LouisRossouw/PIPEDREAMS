import os
import imp
import maya.cmds as cmds

import scene_build.export_manager.export_utils as utils
import scene_build.capture_manager.overlay as overlay



imp.reload(utils)




def capture_view(dir_name,
                 start_number,
                 end_number,
                 task_name,
                 save_path_eval,
                 selected_output,
                 version_eval,
                 overlay_checkbox,
                 comment_eval,
                 greenScreen_checkbox,
                 ):
    """ 
    Creates a playblast with the settings i need and then compresses to .mp4.
    """

    if greenScreen_checkbox == True:
        selected_output = 'png'

    # check if scene saved before executing script, if not saved, it stops
    utils.check_if_saved()
    panel = cmds.getPanel(wf=1)

    # Check if camera is named correctly for the capture to work
    try:
        camera = cmds.modelPanel(panel, query=True, camera=True)
    except RuntimeError:
        cmds.confirmDialog(message='RuntimeError: int value found in camera name', title='RunTimeError : Camera naming', backgroundColor=(1, 1, 1))
        exit()

    try:
        # evaluate res mask and switch it off before playblast :
        camGate_eval = cmds.camera(camera + 'Shape', q=1, displayFilmGate=0)
        camRes_eval = cmds.camera(camera + 'Shape', q=1, displayResolution=0)

        cmds.camera(camera + 'Shape', e=1, displayFilmGate=0)
        cmds.camera(camera + 'Shape', e=1, displayResolution=0)
    except ValueError:
        cmds.confirmDialog(message='ValueError: int value found in camera name', title='ValueError : Camera naming', backgroundColor=(1, 1, 1))
        exit()


    # get file name as temp name for capture
    filepath = cmds.file(q=True, sn=True)
    filename = os.path.basename(filepath)
    # dir_name, extension = os.path.splitext(filename)

    # main_dir = cmds.workspace( lw=True)
    # main_dir_path = cmds.workspace( q=True, rd=True)
    shot = os.getenv('SHOT')

    filename = dir_name

    path_to_dir = save_path_eval + '\\' + task_name

    # creates main dir for specific asset
    if os.path.exists(path_to_dir) != True:
        os.mkdir(path_to_dir)

    path_to_new_dir = save_path_eval + '\\' + task_name + '\\' + filename

    if os.path.exists(path_to_new_dir) != True:
        os.mkdir(path_to_new_dir)

    # creates version 001 dir
    if os.path.exists(path_to_new_dir + '\\v001' ) != True:
        os.mkdir(path_to_new_dir + '\\v001' )
        save_path = (path_to_new_dir + '\\v001')
        export_version_name = 'v001'

    # creates version 002 + etc dir
    else:
        new_version = version_eval.split('v')[1]
        # new_version = utils.versioning(path_to_new_dir)[1]
        try:
            os.mkdir(path_to_new_dir + '\\v' +  new_version)
        except FileExistsError:
            pass
        save_path = (path_to_new_dir + '\\v' +  new_version)
        export_version_name = 'v' +  new_version


    # get current resolution :
    get_width = cmds.getAttr("defaultResolution.width")
    get_height = cmds.getAttr("defaultResolution.height")

    # Sets frame range as per capture_UI settings
    cmds.playbackOptions(minTime=start_number, maxTime=end_number)

    res = (str(get_width) + ':' + str(get_height))


    # mp4 video
    if selected_output == 'mp4':

        file_saveName = path_to_new_dir + '/' + export_version_name + '/' + task_name + '_' + filename + '_' + export_version_name + '.mov'

        print('writing to : ')
        print(file_saveName)

        # playblast
        cmds.playblast(format='qt',
                        filename= file_saveName,
                        sequenceTime=0,
                        clearCache=1,
                        viewer=0,
                        showOrnaments=0,
                        fp=4,
                        percent=100,
                        compression="MPEG-4 Video",
                        quality=100,
                        widthHeight=[get_width,get_height],
                        )

        # res mask and gate to back on if they were on before playblast :
        cmds.camera(camera + 'Shape', e=1, displayFilmGate=camGate_eval)
        cmds.camera(camera + 'Shape', e=1, displayResolution=camRes_eval)

        # compress and convert to .mp4
        capture_file = '"' + file_saveName + '"'
        compressed_capture = path_to_new_dir + '/' + export_version_name + '/' + shot + '_' + filename + '_' + task_name + '_' + export_version_name + '.mp4'

        # FFMPEG cmd line
        os.system('ffmpeg -i ' + str(capture_file) + ' -vf scale=' + res + ' -y ' + str(compressed_capture))

        # add overlay
        if overlay_checkbox != False:
            overlayed_capture_outout = '"' + path_to_new_dir + '/' + export_version_name + '/' + shot + '_' + filename + '_' + task_name + '_overlay_' + export_version_name + '.mp4' + '"'
            output_saved_path = path_to_new_dir + '/' + export_version_name + '/'

            filename_for_overlay = filename + '_' + task_name + '_' + export_version_name + '.mp4'

            overlay.add_overlay(compressed_capture,
                                overlayed_capture_outout,
                                comment_eval,
                                output_saved_path,
                                filename_for_overlay,
                                )

            os.remove(compressed_capture)

        else:
            pass

        os.remove(file_saveName)

        file_saveName_path = path_to_new_dir + '/' + export_version_name + '/'
        os.system("start " + file_saveName_path)

    # Png sequence
    elif selected_output == 'png':

        file_saveName = path_to_new_dir + '/' + export_version_name + '/' + task_name + '_' + filename + '_' + export_version_name + '_'

        print('writing to : ')
        print(file_saveName)

        # playblast
        cmds.playblast(format='image',
                        filename= file_saveName,
                        sequenceTime=0,
                        clearCache=1,
                        viewer=0,
                        showOrnaments=0,
                        fp=4,
                        percent=100,
                        compression="png",
                        quality=100,
                        widthHeight=[get_width,get_height],
                        )

        file_saveName_path = path_to_new_dir + '/' + export_version_name + '/'
        os.system("start " + file_saveName_path)

if __name__ == '__main__':
    capture_view('pew')