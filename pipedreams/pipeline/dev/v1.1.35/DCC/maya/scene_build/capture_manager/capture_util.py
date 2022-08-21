import os
import json
import sys
import maya.cmds as cmds

PipeDreams_root_path = os.getenv('PIPELINE_ROOT')
sys.path.append(PipeDreams_root_path)

import toolUtils.ffmpeg as ffmpeg_convert
import toolUtils.pillow as pillow








def write_to_json(json_path, data):
    """ Create and write to json file """

    with open(json_path, 'w') as f:
        json.dump(data, f, indent=6)



def read_json(json_path):
    """ Reads json file """
    with open(json_path) as f:
        json_file = json.loads(f.read())

    return (json_file)




def write_capture_data(
                        json_manifest_path,
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
                       ):
    """  writes out the json data """

    userName = os.environ['COMPUTERNAME']
    project_name = os.getenv("PROJECT_NAME")
    project = os.getenv("PROJECT")

    TOP_DATA = os.path.dirname(os.getenv("TOP_ASSETS")) + "/data"
    CAPTURES_DATA_DIR = TOP_DATA + "/captures"

    if os.path.exists(CAPTURES_DATA_DIR) != True:
        os.mkdir(CAPTURES_DATA_DIR)

    JSON_CAPTURE = CAPTURES_DATA_DIR + "/capture_data.json"

    if os.path.exists(JSON_CAPTURE) != True:

        data = {}
        data["capture_data"] = {UI_version_eval: {
                                            "RESOLUTION": ["2.35:1", cmds.getAttr("defaultResolution.width"), cmds.getAttr("defaultResolution.height")],
                                            "FPS": cmds.currentUnit(query=True, time=True),
                                            "FOCAL_LENS": 135,
                                            "VERSION": UI_version_eval,
                                            "PROJECT": project,
                                            "PROJECT_NAME": project_name,
                                            "TASK": task_name_eval,
                                            "START": start_number_eval,
                                            "END": end_number_eval,
                                            "RANGE": [start_number_eval, end_number_eval],
                                            "COMMENT": UI_comment_eval,
                                            "USER": userName,
                                            "PATH": export_path_eval + "/" + task_name_eval + "/" + capture_name_eval + "/" + UI_version_eval,

                                            "POSTED_TO_DISCORD": False,
                                            "GUIDES": UI_guides_eval,
                                            "PUBLISH": UI_publish_eval,
                                            "GREENSCREEN": UI_GS_eval
                                            }}

        write_to_json(JSON_CAPTURE, data)

    else:

        data = read_json(JSON_CAPTURE)
        project_name = os.getenv("PROJECT_NAME")
        data["capture_data"] = {UI_version_eval: {
                                            "RESOLUTION": ["2.35:1", cmds.getAttr("defaultResolution.width"), cmds.getAttr("defaultResolution.width")],
                                            "FPS": cmds.currentUnit(query=True, time=True),
                                            "FOCAL_LENS": 135,
                                            "VERSION": UI_version_eval,
                                            "PROJECT": project,
                                            "PROJECT_NAME": project_name,
                                            "TASK": task_name_eval,
                                            "START": start_number_eval,
                                            "END": end_number_eval,
                                            "RANGE": [start_number_eval, end_number_eval],
                                            "COMMENT": UI_comment_eval,
                                            "USER": userName,
                                            "PATH": export_path_eval + "/" + task_name_eval + "/" + capture_name_eval + "/" + UI_version_eval,

                                            "POSTED_TO_DISCORD": False,
                                            "GUIDES": UI_guides_eval,
                                            "PUBLISH": UI_publish_eval,
                                            "GREENSCREEN": UI_GS_eval
                                            }}

    write_to_json(JSON_CAPTURE, data)
    write_to_json(json_manifest_path, data)





def create_dirs(export_path_eval, task_name_eval,
                capture_name_eval, UI_version_eval):
    """ creates directories if it does not exist """

    anim_dir = export_path_eval + "/" + task_name_eval
    capture_name_dir = anim_dir + "/" + capture_name_eval
    version_dir = capture_name_dir + "/" + UI_version_eval
    png_seq_dir = version_dir + "/png_seq"
    video_dir = version_dir + "/video"
    data_dir = version_dir + "/data"
    raw_dir = png_seq_dir + "/raw"
    comp_dir = png_seq_dir + "/comp"

    directories_list = [
                        anim_dir,
                        capture_name_dir,
                        version_dir,
                        png_seq_dir,
                        video_dir,
                        data_dir,
                        raw_dir,
                        comp_dir
                        ]

    for dir in directories_list:
        print(dir)
        if os.path.exists(dir) != True:
            os.mkdir(dir)



def capture_run(
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
                ):


    panel = cmds.getPanel(wf=1)
    camera = cmds.modelPanel(panel, query=True, camera=True)

    # evaluate res mask and switch it off before playblast :
    camera_shape = camera + 'Shape'
    camGate_eval = cmds.camera(camera_shape, edit=True, displayFilmGate=False)
    camRes_eval = cmds.camera(camera_shape, edit=True, displayResolution=False)

# resets disables panzoom before capture.
    cmds.setAttr(camera_shape + ".panZoomEnabled", 0)




# get current resolution :
    get_width = cmds.getAttr("defaultResolution.width")
    get_height = cmds.getAttr("defaultResolution.height")

    # Sets frame range as per capture_UI settings
    cmds.playbackOptions(minTime=start_number_eval, maxTime=end_number_eval)

    res = (str(get_width) + ':' + str(get_height))

# create directories if it does not exist.
    create_dirs(export_path_eval, task_name_eval,
                capture_name_eval, UI_version_eval)

# Png sequence

    file_name = capture_name_eval + "_" + task_name_eval + "_" + UI_version_eval
    PNG_file_saveName_path = export_path_eval + "/" + task_name_eval + "/" + capture_name_eval + "/" + UI_version_eval + "/png_seq/raw/" + file_name


# playblast
    cmds.playblast(format='image',
                    filename= PNG_file_saveName_path,
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

    # file_saveName_path = path_to_new_dir + '/' + export_version_name + '/'
    # os.system("start " + file_saveName_path)

    json_manifest_path = export_path_eval + "/" + task_name_eval + "/" + capture_name_eval + "/" + UI_version_eval + "/data/capture_manifest.json"
    write_capture_data(
                        json_manifest_path,
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
                       )

# composit overlays
    if UI_publish_eval == True:
        pillow.composit_sequence(
                                 os.path.dirname(PNG_file_saveName_path),
                                 json_manifest_path,
                                 UI_version_eval
                                )
        COMP_file_saveName_path = export_path_eval + "/" + task_name_eval + "/" + capture_name_eval + "/" + UI_version_eval + "/png_seq/comp/" + file_name
    else:
        COMP_file_saveName_path = export_path_eval + "/" + task_name_eval + "/" + capture_name_eval + "/" + UI_version_eval + "/png_seq/raw/" + file_name

# convert to mp4
    video_output_path = os.path.dirname(os.path.dirname(os.path.dirname(COMP_file_saveName_path))) + "/video/" + file_name

    print("****", COMP_file_saveName_path)
    print("*** ***", video_output_path)

    ffmpeg_convert.png_to_vid(
                              COMP_file_saveName_path,
                              video_output_path
                              )





if __name__ == "__main__":

    capture_name_eval = "dv_010"
    start_number_eval = 1
    end_number_eval = 120
    task_name_eval = "anim"
    export_path_eval = "D:/work/projects/3D/projects/test/testdev/shots/dv_010/captures"
    selected_output = "mp4"
    UI_version_eval = "v001"
    UI_publish_eval = True
    UI_guides_eval = True
    UI_GS_eval = False
    UI_comment_eval = "This is a comment"


    capture_run(
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
                )

