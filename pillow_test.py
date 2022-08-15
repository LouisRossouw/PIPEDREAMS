import os
from tkinter import Scale
from PIL import Image, ImageFont, ImageDraw, ImageEnhance




logo_path = "D:/work/projects/dev/projects/PIPEDREAMS/pipedreams/pipeline/resources/logo/pixl.jpg"
image_sequence_dir = "D:/work/projects/3D/projects/boxx/dev/shots/bxx_010/captures/anim/bxx_010/v006"
output = "D:/work/projects/3D/projects/boxx/dev/shots/bxx_010/captures/anim/bxx_010/v007"


image_sequence = os.listdir(image_sequence_dir)

FONT_SIZE = 20
LOGO_SIZE = 50
MAIN_RESOLUTION = 1920, 1080



def img_check(img_size_width, img_size_height, main_resolution):
    position_height = (main_resolution[1] - img_size_height) / 2
    return(position_height)





def png_to_vid(path_to_png_sequence_input,
               path_to_video_output
               ):
    """ This converts a png sequence to video / mp4, mov etc """

    path = path_to_png_sequence_input + '_.%04d.png'
    path_out = path_to_video_output + '.mp4'

    # uses ffmpeg to convert png seq to mp4
    os.system('ffmpeg -i ' + str(path) + ' -vcodec libx264 -crf 1  -pix_fmt yuv420p ' + str(path_out))






count = 0
for image in image_sequence:

    count += 1

    image_path = f"{image_sequence_dir}/{image}"
    img = Image.open(image_path).convert("RGBA")
    img_size_width, img_size_height = img.size

    img_logo_file = Image.open(logo_path)
    img_logo = img_logo_file.resize((LOGO_SIZE, LOGO_SIZE))
    logo_size_width, logo_size_height = img_logo.size

    position_height = img_check(img_size_width, img_size_height, MAIN_RESOLUTION)

    blank_img = Image.new("RGB", (MAIN_RESOLUTION[0], MAIN_RESOLUTION[1]), (0,0,0))
    # Add capture image
    blank_img.paste(img, (0,int(position_height)))
    # Add logo | (image size / 2) - (logo size / 2) =  center point for logo
    blank_img.paste(img_logo, (int(img_size_width / 2) - int((logo_size_width / 2)), 970))


    draw = ImageDraw.Draw(blank_img)
    font = ImageFont.truetype("arial.ttf", FONT_SIZE)

# Right Bottom Corner
    # FPS
    draw.text((img_size_width - 200, MAIN_RESOLUTION[1] - 125),"FPS: 30",(255,255,255), font=font)
    # Frame Number
    draw.text((img_size_width - 200, MAIN_RESOLUTION[1] - 100),"Frame_" + str(count).zfill(4),(255,255,255), font=font)
    # Version
    draw.text((img_size_width - 200, MAIN_RESOLUTION[1] - 75),"V007",(255,255,255), font=font)

# Top Left Corner
    # SHOT NAME
    draw.text((50, 50),"Boxx_dev_sh010",(255,255,255), font=font)


    blank_img.save(f"{output}/{image}", "PNG")


tt = output + "/anim_bxx_010_v006"
out = output + "/text.mp4"
png_to_vid(tt, tt)