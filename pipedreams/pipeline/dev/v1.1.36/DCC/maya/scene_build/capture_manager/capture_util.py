import os
import json
import sys
import maya.cmds as cmds

PipeDreams_root_path = os.getenv('PIPELINE_ROOT')
sys.path.append(PipeDreams_root_path)

import toolUtils.ffmpeg as ffmpeg_convert
import toolUtils.pillow as pillow




def get_resolution():
    """ returns the resolution and aspect ratio of the maya scene file. """

    width = cmds.getAttr("defaultResolution.width")
    height = cmds.getAttr("defaultResolution.height")

    res = str(width) + "x" + str(height)

    if res == "1920x820":
        aspect_ratio = "2.35"
    elif res == "1920x817":
        aspect_ratio = "2.35:1"
    elif res == "1920x1080":
        aspect_ratio = "16:9"
    elif res == "1080x1080":
        aspect_ratio = "1:1"
    elif res == "1000x1000":
        aspect_ratio = "1:1"
    else:
        aspect_ratio = "/"

    return(aspect_ratio, width, height, res)




def get_FPS():
    """ returns the FPS in numbers and not text """

    FPS = cmds.currentUnit(query=True, time=True)

    if str(FPS) == "film":
        FPS_value = "24"
    elif str(FPS) == "pal":
        FPS_value = "25"
    elif str(FPS) == "ntsc":
        FPS_value = "30"
    elif str(FPS) == "palf":
        FPS_value = "50"
    else:
        FPS_value = str(FPS)

    return(FPS_value)




def cleanup_png_sequence(path_to_pngs):
    """ runs a cleanup process of deleting the png sequences if condition = True. 
        this is to help save space as png sequences cost a fair amount of mb. 
    """
    png_seq_raw = os.listdir(path_to_pngs + "/raw")
    png_seq_comp = os.listdir(path_to_pngs + "/comp")

    for png in png_seq_raw:
        os.remove(path_to_pngs + "/raw/" + png)

    for png in png_seq_comp:
        os.remove(path_to_pngs + "/comp/" + png)




def write_to_json(json_path, data):
    """ Create and write to json file. """

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
                        focal_length
                       ):
    """  writes out the json data """

    userName = os.environ['COMPUTERNAME']
    project_name = os.getenv("PROJECT_NAME")
    project = os.getenv("PROJECT")

    TOP_DATA = os.path.dirname(os.getenv("TOP_ASSETS")) + "/data"
    CAPTURES_DATA_DIR = TOP_DATA + "/captures"
    JSON_CAPTURE = CAPTURES_DATA_DIR + "/capture_data.json"

    if os.path.exists(CAPTURES_DATA_DIR) != True:
        os.mkdir(CAPTURES_DATA_DIR)

    if os.path.exists(JSON_CAPTURE) != True:
        data = {}
        write_to_json(JSON_CAPTURE, data)

    get_res = get_resolution()
    #data = read_json(JSON_CAPTURE)
    project_name = os.getenv("PROJECT_NAME")
    data = {}
    data["capture_data"] = {UI_version_eval: {
                                        "RESOLUTION": [get_res[0], int(get_res[1]), int(get_res[2])],
                                        "FPS": get_FPS(),
                                        "FOCAL_LENS": int(focal_length),
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



def collect_scene_data(camera, min, max, json_manifest_path):
    """ runs through every frame and collects data from the scene and records it into a json file,
    example, records the cameras world transforms and focal length on every frame.
    """

    data = read_json(json_manifest_path)

    camera_xform = []
    for i in range(int(min), int(max + 1)):

        cmds.currentTime(i, update=True, edit=True)
        camera_world_transforms = cmds.xform(camera,query=True,worldSpace=True,rotatePivot=True)

        camera_xform.append(camera_world_transforms)
        print("Collecting scene data: " + str(i))


    # polyEval
    cmds.select(all=True)
    query_poly = cmds.polyEvaluate()
    cmds.select(clear=True)

    # append to capture_manifest
    data["query_poly"] = query_poly
    data["camera_xform"] = camera_xform

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
                config_data
                ):

    # Get camera
    panel = cmds.getPanel(wf=1)
    camera = cmds.modelPanel(panel, query=True, camera=True)


    # evaluate selected cameras attributes.
    camera_shape = camera + 'Shape'
    camGate_eval = cmds.camera(camera_shape, edit=True, displayFilmGate=False)
    camRes_eval = cmds.camera(camera_shape, edit=True, displayResolution=False)

    focal_length = cmds.getAttr(camera_shape + ".focalLength")

    Scene_FPS = get_FPS()
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
    PNG_Dir = export_path_eval + "/" + task_name_eval + "/" + capture_name_eval + "/" + UI_version_eval + "/png_seq"
    PNG_file_saveName_path = PNG_Dir + "/raw/" + file_name


    # playblast
    cmds.playblast(format='image',
                    filename= PNG_file_saveName_path,
                    sequenceTime=False,
                    clearCache=1,
                    viewer=0,
                    showOrnaments=0,
                    fp=4,
                    percent=100,
                    compression="png",
                    quality=100,
                    widthHeight=[get_width,get_height],
                    indexFromZero=True
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
                        focal_length
                       )

    # collects scene data for every frame.
    collect_scene_data(
                       camera,
                       start_number_eval,
                       end_number_eval,
                       json_manifest_path
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
                              video_output_path,
                              Scene_FPS
                              )
             

    try:    
        # runs a cleanup process of deleting the png sequences if condition = True. this is to help save space as png sequences cost a fair amount of mb.      )
        if config_data["clean_captures_pngs"] == True:
            cleanup_png_sequence(PNG_Dir)
            print("Cleaning up pngs")
        else:
            pass
        
    except KeyError:
        print("Cleaning up - no conditions in config")
        pass




if __name__ == "__main__":

    # capture_name_eval = "dv_010"
    # start_number_eval = 1
    # end_number_eval = 120
    # task_name_eval = "anim"
    # export_path_eval = "D:/work/projects/3D/projects/test/testdev/shots/dv_010/captures"
    # selected_output = "mp4"
    # UI_version_eval = "v001"
    # UI_publish_eval = True
    # UI_guides_eval = True
    # UI_GS_eval = False
    # UI_comment_eval = "This is a comment"
    #
    #
    # capture_run(
    #             capture_name_eval,
    #             start_number_eval,
    #             end_number_eval,
    #             task_name_eval,
    #             export_path_eval,
    #             selected_output,
    #             UI_version_eval,
    #             UI_publish_eval,
    #             UI_guides_eval,
    #             UI_GS_eval,
    #             UI_comment_eval,
    #             )


    # get_resolution()


 
    path_to_pngs = "D:\\work\\projects\\3D\\projects\\boxx\\dev\\shots\\bxx_010\\captures\\anim\\bxx_010\\v020\\png_seq"
    cleanup_png_sequence(path_to_pngs)

