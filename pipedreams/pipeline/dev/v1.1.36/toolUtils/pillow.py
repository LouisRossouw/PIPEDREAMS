import os
import json
from pathlib import Path
from zlib import Z_BEST_SPEED

from PIL import Image, ImageFont, ImageDraw, ImageEnhance


def png_to_vid(path_to_png_sequence_input,
               path_to_video_output
               ):
    """ This converts a png sequence to video / mp4, mov etc """

    path = path_to_png_sequence_input + '_.%04d.png'
    path_out = path_to_video_output + '.mp4'

    # uses ffmpeg to convert png seq to mp4
    os.system('ffmpeg -i ' + str(path) + ' -vcodec libx264 -crf 1  -pix_fmt yuv420p ' + str(path_out))


def write_to_json(json_path, data):
    """ Create and write to json file """

    with open(json_path, 'w') as f:
        json.dump(data, f, indent=6)



def read_json(json_path):
    """ Reads json file """
    with open(json_path) as f:
        json_file = json.loads(f.read())

    return (json_file)




def logo_position():
    pass
    # (int("img_size_width" / 2) - int(("logo_size_width" / 2)



def get_resolution(capture_data_manifest, version):
    """ Based on the original resolution of the capture from the DCC package, we adjust the output 
        output resolution to accomodate the overlay crops + data.
    """

    aspect_ratio = capture_data_manifest["capture_data"][version]["RESOLUTION"][0]

    if aspect_ratio == "2.35:1":
        base_resolution = 1920, 817
        scaled = 1920, 1080
    elif aspect_ratio == "2.35":
        base_resolution = 1920, 820
        scaled = 1920, 1080
    elif aspect_ratio == "16:9":
        base_resolution = 1920, 1080
        scaled = 1920, 1340
    elif aspect_ratio == "16:10":
        base_resolution = 1920, 1200
        scaled = 1920, 1460
    elif aspect_ratio == "4:3":
        base_resolution = 1440, 1080
        scaled = 1920, 1340
    elif aspect_ratio == "1:1":
        base_resolution = 1000, 1000
        scaled = 1920, 1260
    else:
        scaled = 1920, 1080

    return scaled





def composit_sequence(image_sequence_dir, json_manifest_path, version):

    FONT_SIZE = 15
    LOGO_SIZE = 50

    # Cordinates
    TXT_USER = 50, 125
    TXT_COMMENT = 50, 110

    TXT_FPS = 200, 125
    TXT_FRAME_NUM = 200, 110
    TXT_LENS = 200, 95
    TXT_RANGE = 200, 80
    TXT_RESOLUTION = 200, 65

    # Overlay Color
    OVERLAY_COLOR = 0,0,0
    OVERLAY_TRANSPARENCY = 50

    logo_path = str(Path(os.path.dirname(__file__)).parents[2]) + "/resources/captures/logo/pixl_400_400.jpg"


    image_sequence = os.listdir(image_sequence_dir)

    img_logo_file = Image.open(logo_path)
    img_logo = img_logo_file.resize((LOGO_SIZE, LOGO_SIZE))
    logo_size_width, logo_size_height = img_logo.size

    # Read the Captures data manifest file
    capture_data_manifest = read_json(json_manifest_path)

    # json data - General
    FPS = capture_data_manifest["capture_data"][version]["FPS"]
    PROJECT = capture_data_manifest["capture_data"][version]["PROJECT"]
    USER = capture_data_manifest["capture_data"][version]["USER"]
    COMMENT = capture_data_manifest["capture_data"][version]["COMMENT"]
    FOCAL_LENS = capture_data_manifest["capture_data"][version]["FOCAL_LENS"]
    VERSION = capture_data_manifest["capture_data"][version]["VERSION"]
    RANGE = capture_data_manifest["capture_data"][version]["RANGE"]
    RESOLUTION = capture_data_manifest["capture_data"][version]["RESOLUTION"]

    # json data - poly
    VERTEX = capture_data_manifest["query_poly"]["vertex"]
    EDGE = capture_data_manifest["query_poly"]["edge"]
    FACE = capture_data_manifest["query_poly"]["face"]
    UVCOORD = capture_data_manifest["query_poly"]["uvcoord"]
    TRIANGLE = capture_data_manifest["query_poly"]["triangle"]

    # json data - camera xform / world transforms (list of lists)
    CAMERA_XFORM = capture_data_manifest["camera_xform"]


    count = 0
    frame_count = int(RANGE[0]) - 1

    for image in image_sequence:

        format = image[-3:]
        if format == "png":

            count += 1
            frame_count += 1

            print("adding overlays: frame -- " + str(frame_count), " | count -- " + str(count))

            # Open image frame that was captured
            image_path = f"{image_sequence_dir}/{image}"
            img = Image.open(image_path).convert("RGBA")
            img_size_width, img_size_height = img.size


# Blank 1080P resolution, this is the base
            scaled_resolution = get_resolution(capture_data_manifest, version)
            blank_img = Image.new("RGB", (scaled_resolution[0], scaled_resolution[1]), (0,0,0))


# Add capture image
            position_height = (scaled_resolution[1] - img_size_height) / 2
            blank_img.paste(img, (0,int(position_height)))
            # Add logo | (image size / 2) - (logo size / 2) =  center point for logo
            blank_img.paste(img_logo, (int(img_size_width / 2) - int((logo_size_width / 2)), 970))

            draw = ImageDraw.Draw(blank_img, "RGBA")
            font = ImageFont.truetype("arial.ttf", FONT_SIZE)


# Left Bottom Corner
            # User
            draw.text((TXT_USER[0], scaled_resolution[1] - TXT_USER[1]),"User: " + str(USER),(255,255,255), font=font)
            # Comment
            draw.text((TXT_COMMENT[0], scaled_resolution[1] - TXT_COMMENT[1]),"Comment: " + str(COMMENT),(255,255,255), font=font)

# Right Bottom Corner
            # FPS
            draw.text((img_size_width - TXT_FPS[0], scaled_resolution[1] - TXT_FPS[1]),"FPS: " + str(FPS),(255,255,255), font=font)
            # Frame Number
            draw.text((img_size_width - TXT_FRAME_NUM[0], scaled_resolution[1] - TXT_FRAME_NUM[1]),"Frame: " + str(frame_count),(255,255,255), font=font)
            # Lens
            draw.text((img_size_width - TXT_LENS[0], scaled_resolution[1] - TXT_LENS[1]),"Focal: " + str(FOCAL_LENS),(255,255,255), font=font)
            # Range
            draw.text((img_size_width - TXT_RANGE[0], scaled_resolution[1] - TXT_RANGE[1]),"Range: " + str(RANGE[0]) + " - " + str(RANGE[1]),(255,255,255), font=font)
            # Resolution
            draw.text((img_size_width - TXT_RESOLUTION[0], scaled_resolution[1] - TXT_RESOLUTION[1]),"Res: " + str(RESOLUTION[0] + " | "+str(RESOLUTION[1])+"x"+str(RESOLUTION[2])),(255,255,255), font=font)

# Top Left Corner
            # SHOT NAME
            draw.text((50, 100),PROJECT + "_" + VERSION,(255,255,255), font=font)


# Overlay
            if capture_data_manifest["capture_data"][version]["GUIDES"] == True:
                draw.line((0, 250, 1920, 250), fill=(OVERLAY_COLOR[0],OVERLAY_COLOR[1],OVERLAY_COLOR[2], OVERLAY_TRANSPARENCY))
                draw.line((0, 830, 1920, 830), fill=(OVERLAY_COLOR[0],OVERLAY_COLOR[1],OVERLAY_COLOR[2], OVERLAY_TRANSPARENCY))
                draw.line((480, 0, 480, 1080), fill=(OVERLAY_COLOR[0],OVERLAY_COLOR[1],OVERLAY_COLOR[2], OVERLAY_TRANSPARENCY))
                draw.line((960+480, 0, 960+480, 1080), fill=(OVERLAY_COLOR[0],OVERLAY_COLOR[1],OVERLAY_COLOR[2], OVERLAY_TRANSPARENCY))



            save_path = f"{os.path.dirname(image_sequence_dir)}/comp/{image}"
            blank_img.save(save_path, "PNG")






def camera_plot(data_path):
    """ This function will draw the cameras xform as a visual representation """

    capture_data_manifest = read_json(data_path)

    CAMERA_XFORM_DATA = capture_data_manifest["camera_xform"]

    IMG_SIZE_X = 1000
    IMG_SIZE_Z = 1000

    IMG_CENTRE = IMG_SIZE_X / 2

    DRAW_SCALE = 10

    # Blank starting image - need to be dynamic to the cameras travel distance.
    blank_canvas = Image.new("RGB", (IMG_SIZE_X, IMG_SIZE_Z), (0,0,0))
    draw = ImageDraw.Draw(blank_canvas, "RGBA")

    frame = 0

    for cord in CAMERA_XFORM_DATA:
        frame += 1

        X = (cord[0] * DRAW_SCALE) + IMG_CENTRE
        Z = (cord[2] * DRAW_SCALE) + IMG_CENTRE

        print(frame, "-", X, Z)

        draw.line((X, Z, X, Z))

    blank_canvas.show()





if __name__ == "__main__":


    logo_path = "D:/work/projects/dev/projects/PIPEDREAMS/pipedreams/pipeline/resources/logo/pixl.jpg"
    image_sequence_dir = "D:/work/projects/3D/projects/test/testdev/shots/dv_010/captures/anim/dv_010/v017/png_seq/raw"
    output = "D:/work/projects/3D/projects/test/testdev/shots/dv_010/captures/anim/dv_010/v017/dev"
    data = "D:/work/projects/3D/projects/test/testdev/shots/dv_010/captures/anim/dv_010/v017/data/capture_manifest.json"

    version = "v017"
    #composit_sequence(image_sequence_dir, data, version)
    
    camera_plot(data)