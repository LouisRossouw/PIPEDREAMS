import os
import json
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



def get_resolution(capture_data_manifest):
    """ Based on the original resolution of the capture from the DCC package, we adjust the output 
        output resolution to accomodate the overlay crops + data.
    """

    aspect_ratio = capture_data_manifest["capture_data"]["RESOLUTION"][0]

    if aspect_ratio == "2.35:1":
        base_resolution = 1920, 818
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

    return scaled





def composit_sequence(image_sequence_dir):

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

    logo_path = "D:/work/projects/dev/projects/PIPEDREAMS/pipedreams/pipeline/resources/logo/pixl.jpg"

    image_sequence = os.listdir(image_sequence_dir)

    img_logo_file = Image.open(logo_path)
    img_logo = img_logo_file.resize((LOGO_SIZE, LOGO_SIZE))
    logo_size_width, logo_size_height = img_logo.size

    # Read the Captures data manifest file
    capture_data_manifest = read_json(image_sequence_dir + "/capture_data_manifest.json")


    FPS = capture_data_manifest["capture_data"]["FPS"]
    PROJECT = capture_data_manifest["capture_data"]["PROJECT"]
    USER = capture_data_manifest["capture_data"]["USER"]
    COMMENT = capture_data_manifest["capture_data"]["COMMENT"]
    FOCAL_LENS = capture_data_manifest["capture_data"]["FOCAL_LENS"]
    VERSION = capture_data_manifest["capture_data"]["VERSION"]
    RANGE = capture_data_manifest["capture_data"]["RANGE"]
    RESOLUTION = capture_data_manifest["capture_data"]["RESOLUTION"]

    count = 0
    for image in image_sequence:

        print("adding overlays: " + str(count))

        format = image[-3:]
        if format == "png":

            count += 1

            # Open image frame that was captured
            image_path = f"{image_sequence_dir}/{image}"
            img = Image.open(image_path).convert("RGBA")
            img_size_width, img_size_height = img.size



# Blank 1080P resolution, this is the base
            scaled_resolution = get_resolution(capture_data_manifest)
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
            draw.text((img_size_width - TXT_FRAME_NUM[0], scaled_resolution[1] - TXT_FRAME_NUM[1]),"Frame: " + str(count),(255,255,255), font=font)
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
            if capture_data_manifest["capture_data"]["OVERLAY"] == True:
                draw.line((0, 250, 1920, 250), fill=(OVERLAY_COLOR[0],OVERLAY_COLOR[1],OVERLAY_COLOR[2], OVERLAY_TRANSPARENCY))
                draw.line((0, 830, 1920, 830), fill=(OVERLAY_COLOR[0],OVERLAY_COLOR[1],OVERLAY_COLOR[2], OVERLAY_TRANSPARENCY))
                draw.line((480, 0, 480, 1080), fill=(OVERLAY_COLOR[0],OVERLAY_COLOR[1],OVERLAY_COLOR[2], OVERLAY_TRANSPARENCY))
                draw.line((960+480, 0, 960+480, 1080), fill=(OVERLAY_COLOR[0],OVERLAY_COLOR[1],OVERLAY_COLOR[2], OVERLAY_TRANSPARENCY))



            blank_img.save(f"{output}/{image}", "PNG")





if __name__ == "__main__":

    logo_path = "D:/work/projects/dev/projects/PIPEDREAMS/pipedreams/pipeline/resources/logo/pixl.jpg"
    image_sequence_dir = "D:/work/projects/3D/projects/boxx/dev/shots/bxx_010/captures/anim/bxx_010/v014"
    output = "D:/work/projects/3D/projects/boxx/dev/shots/bxx_010/captures/anim/bxx_010/v014"

    data = {}
    data["capture_data"] = {
                            "RESOLUTION": ["2.35:1", 1920, 818],
                            "RANGE": [1, 100],
                            "FPS": 25,
                            "PROJECT": "boxx_dev_bxx_010",
                            "USER": "LOURO",
                            "COMMENT": "this is still a WIP!",
                            "FOCAL_LENS": 135,
                            "VERSION": "v007",

                            "OVERLAY": True,
                            "PUBLISH": True,
                            }

    write_to_json(image_sequence_dir + "/capture_data_manifest.json", data)

    test = read_json(image_sequence_dir + "/capture_data_manifest.json")
    composit_sequence(image_sequence_dir)



    png_to_vid(output + "/anim_bxx_010_v014", output + "/test.mp4")