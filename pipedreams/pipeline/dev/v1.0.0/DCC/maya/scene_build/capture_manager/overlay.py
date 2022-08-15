import os
import yaml


def add_overlay(original_file,
                output_capture,
                comment,
                output_saved_path,
                filename_for_overlay,
                ):
    """ This function first checks the config, and then adds an overlay if True """

    # Open config
    This_py_file = os.path.abspath(__file__)
    backUp = os.path.dirname(os.path.dirname(os.path.dirname(This_py_file)))
    path_to_config = os.path.dirname(os.path.dirname((backUp))) + '\\cmd_line'

    # Open config
    config = yaml.safe_load(open(f'{path_to_config}\\config.yaml', 'r'))

    # Evaluate overlay data in the config
    create_overlay = config["create_overlay"]
    overlay_position = config["overlay_position"]
    overlay_size = config["overlay_size"]
    overlay_image_dir = config["overlay_image_dir"]
    image_to_overlay = config["image_to_overlay"]



    path_to_image = overlay_image_dir + '\\' + image_to_overlay

    image_type = image_to_overlay.split('.')[1]

    # xy pixel coordinates all stat top left, 1:1 is the very top left pixel,
    # and (main_w-overlay_w):(main_h-overlay_h) gets the videos w and h

    if overlay_position == 'top_left':
        position = '25:25"'

    elif overlay_position == 'top_center':
        position = '(main_w-overlay_w)/2:25"'

    elif overlay_position == 'top_right':
        position = '(main_w-overlay_w)-25:(main_h-overlay_h)-25"'

    elif overlay_position == 'bottom_left':
        position = '25:(main_h-overlay_h)-25"'

    elif overlay_position == 'bottom_center':
        position = '(main_w-overlay_w)/2:(main_h-overlay_h)-25"'

    elif overlay_position == 'bottom_right':
        position = '(main_w-overlay_w)-25:(main_h-overlay_h)-25"'


    # If config says True, an overlay will be added
    if create_overlay == True:

        comment_file_path = output_saved_path + 'comment.png'
        project_name = os.getenv("PROJECT_NAME")
        comment_reformatted = '"' + project_name + ' || ' + filename_for_overlay + ' || ' + comment + '"'

        # add comment overlay
        os.system('magick convert -background none -fill white  -font Georgia \
                  -size 1000x100 -gravity center label:' + str(comment_reformatted) + ' ' + str(comment_file_path))


        # For png
        if image_type == 'png':

            # overlay=25:25 - top right
            # overlay=(main_w-overlay_w)\2:25 - center top

            os.system('ffmpeg -i ' + str(original_file) + ' -i ' + str(comment_file_path) + ' -filter_complex \
            "[1]scale=' + str(overlay_size) + ':-1[b];[0][b] overlay=' + str(position) + ' ' + str(output_capture))


        # For gif
        elif image_type == 'gif':

            os.system('ffmpeg -i ' + str(original_file) + ' -ignore_loop 0 -i ' + str(path_to_image) + ' -filter_complex \
            "[1]scale=' + str(overlay_size) + ':-1[b];[0][b] overlay=' + str(position[0:-1]) + ':shortest=1" ' + str(output_capture))











    else:

        pass



if __name__ == "__main__":
    original_file = "D:\\work\\projects\\dev\\learn\\ffmpeg_tests\\overlay\\footage\\yes.mp4"
    output_capture = "D:\\work\\projects\\dev\\learn\\ffmpeg_tests\\overlay\\hello.mp4"

    add_overlay(original_file, output_capture)

