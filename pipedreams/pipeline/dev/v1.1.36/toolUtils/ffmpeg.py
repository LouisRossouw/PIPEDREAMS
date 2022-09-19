import os
import shutil
from PIL import Image


# FFMPEG

def vid_to_png(path_to_video_input,
               path_to_png_sequence_output,
               ):
    """ This converts the mp4/mov etc to a png sequence """

    print('wip')


def png_to_vid(path_to_png_sequence_input,
               path_to_video_output,
               FPS
               ):
    """ This converts a png sequence to video / mp4, mov etc """

    path = path_to_png_sequence_input + '.%04d.png'
    path_out = path_to_video_output + '.mp4'

    # uses ffmpeg to convert png seq to mp4
    os.system('ffmpeg -i ' + str(path) + ' -vcodec libx264 -crf 1 -r ' + str(FPS) + ' -pix_fmt yuv420p ' + str(path_out))


def composite_img(png_name, png_save_name, bg_color):
    """ This loops through all pngs and adds a backround color """

    img = Image.open(png_name)
    img_size_width, img_size_height = img.size
    color_backround = Image.new('RGBA', (img_size_width, img_size_height), bg_color)

    comp = Image.alpha_composite(color_backround, img)

    comp.save(png_save_name)
    os.remove(png_name)



def maya_green_screen(path_to_png_sequence_input, name, selected_output):
    """ This tool turns maya capture to green screen mp4 or png """

    print('running maya_green_screen')

    # path goes to \movies\anim\test\v000\

    bg_color_green = (0, 177, 64)
    all_pngs = os.listdir(path_to_png_sequence_input)

    png_main_name = path_to_png_sequence_input + '\\' + name

    count = 0

    for png in all_pngs:

        split = png.split('.')[2]

        if split == 'png':

            count += 1
            png_save_name = png_main_name + '_' + str(count) + '.png'
            png_name = (path_to_png_sequence_input + '\\' + png)

            # Comp the green_screen to the png
            composite_img(png_name, png_save_name, bg_color_green)


    if selected_output != 'png':
        # Convert green_screen png seq back to .mp4

        png_to_vid(png_main_name, png_main_name)

        # remove png old green_screen seq
        all_pngs_new = os.listdir(path_to_png_sequence_input)
        for green_png in all_pngs_new:
            split = green_png.split('.')[1]

            if split == 'png':
                os.remove(path_to_png_sequence_input + '\\' + green_png)
    else:
        pass




















if __name__ == '__main__':
    name = 'anim_green_test_v001'
    path_to_png_sequence_input = "D:/work/projects/3D/projects/test/testdev/shots/dv_010/captures/anim/dv_010/v001/png_seq/comp/dv_010_anim_v001"
    out = "D:/work/projects/3D/projects/test/testdev/shots/dv_010/captures/anim/dv_010/v001/video/test.mp4"
    # maya_green_screen(path_to_png_sequence_input, name)

    png_to_vid(path_to_png_sequence_input, out)
