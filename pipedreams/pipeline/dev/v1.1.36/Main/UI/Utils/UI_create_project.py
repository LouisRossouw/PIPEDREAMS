import os
import yaml
import time
from pathlib import Path

import PySimpleGUI as sg
from PIL import ImageGrab


# Fixes blurry issues on UI for win10 high DPI displays
from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)


def screen_size():
    img = ImageGrab.grab()
    return (img.size)


def create_config(pipeline_path, 
                    pipeline_type,
                    resolution,
                    aspect_ration,
                    FPS,
                    discord_sync,
                    Publisher,
                    Guides
                    ):
    """ This creates a yaml config file for pipeline_type """

    pipeline_config_path = f'{pipeline_path}/pipeline_data.yaml'


    if resolution == "1080p":
        res_w = 1920
        res_h = 1080
    if resolution == "720p":
        res_w = 1280
        res_h = 720
    if resolution == "480p":
        res_w = 852
        res_h = 480 

    if aspect_ration == "16x9":
        res = str(res_w) + 'x' + str(res_h)
    if aspect_ration == "16x9":
        res = str(res_h) + 'x' + str(res_w)


    data = {"pipeline_type" : pipeline_type,
            "Resolution" : res,
            "ASPR" : aspect_ration,
            "FPS" : FPS,
            "discord_sync": discord_sync,
            "Publisher": Publisher,
            "Guides": Guides
            }


    with open(pipeline_config_path, 'w') as file:
        yaml.dump(data, file, default_flow_style=False)



def create_dir(directory_list):
    """ simply creates the dir if it does not exist """


    for dir in directory_list:

        # Create dirs
        if os.path.exists(dir) != True:
            os.mkdir(dir)
            print("Creating dir: ", dir.split('/')[-1])




def build_project(
                    main_projects_path,
                    input_project_name,
                    input_sub_project_name,

                    pipeline_type,
                    shot_acronym,
                    shot_count,

                    resolution,
                    aspect_ration,
                    FPS,

                    discord_sync,
                    Publisher,
                    Guides

                  ):
    """ Builds the file structure for a project based on either pipeline_A structure or pipeline_B structure"""


    if pipeline_type == "pipe_a":

        # PipeLine_A
        # Paths to project dirs

        project_name = f'{main_projects_path}/{input_project_name}'
        sub_project_name = f'{project_name}/{input_sub_project_name}'

        top_asset = f'{sub_project_name}/assets'
        client_io = f'{sub_project_name}/client_io'
        data = f'{sub_project_name}/data'
        refrence = f'{sub_project_name}/refrence'
        shots = f'{sub_project_name}/shots'

        pipeline = f'{data}/pipeline'
        edit = f'{shots}/edit'


        directory_list = [
                            project_name,
                            sub_project_name,
                            top_asset,
                            client_io,
                            data,
                            refrence,
                            shots,

                            pipeline,
                            edit,


                          ]

        # Create dirs
        create_dir(directory_list)
        create_config(pipeline, 
                    pipeline_type, 
                    resolution,
                    aspect_ration,
                    FPS,
                    discord_sync,
                    Publisher,
                    Guides
                    )



        # Create Shots
        for i in range(1, (int(shot_count)) + 1):
            shot_name = f'{shot_acronym}_{str(i * 10).zfill(3)}'

            shot_dir = f'{shots}/{shot_name}'

            shot_assets = f'{shot_dir}/assets'
            shot_captures = f'{shot_dir}/captures'
            shot_data = f'{shot_dir}/data'
            shot_image = f'{shot_dir}/image'
            shot_refrence = f'{shot_dir}/refrence'
            shot_users = f'{shot_dir}/users'

            shot_directories_list = [

                                        shot_dir,
                                        shot_assets,
                                        shot_captures,
                                        shot_data,
                                        shot_image,
                                        shot_refrence,
                                        shot_users,

                                    ]

            # Create dirs
            create_dir(shot_directories_list)









    elif pipeline_type == "pipe_b":

        pass




def get_UI_config():
    """ returns the UI specific config """

    main_path = Path(__file__).parents[6]
    config_path = (f"{main_path}/admin/UI_toolBar.yaml")
    file_data = yaml.safe_load(open(config_path, 'r'))

    return file_data




def UI(config, icon_1):
    """ builds a UI for the project creator """


    UI_config = get_UI_config()


    THEME = UI_config['CREATE_THEME']
    CREATE_WINDOW_NUDGE = UI_config["CREATE_WINDOW_NUDGE"]
    CREATE_WINDOW_SIZE = UI_config["CREATE_WINDOW_SIZE"]
    CREATE_FONT_HEADING = UI_config["FONT_HEADING"]

    CREATE_TEXT_COLOR_MULTILINE = UI_config["TEXT_COLOR_MULTILINE"]
    CREATE_FONT_MULTILINE = UI_config["FONT_MULTILINE"]
    CREATE_BG_MULTILINE = UI_config["BG_MULTILINE"]

    CREATE_WINDOW_TEXT_COLOR = UI_config["WINDOW_TEXT_COLOR"]
    CREATE_WINDOW_BG_COLOR = UI_config["WINDOW_BG_COLOR"]





    print("Launching project creator")

    # Config
    main_projects_path = config["Pipeline_Path"]

    # Theme
    sg.theme(THEME) 


    # # Top UI layout
    # top_menu = [['Rockettotheskies', ['dev', 'test', 'Exit', 'Properties']],      
    #             ['Edit', ['Paste', ['Special', 'Normal', ], 'Undo'], ],      
    #             ['Help', 'About'], ]   



    # Build UI layout
    layout = [  
                # [sg.Menu(top_menu, tearoff=True)],
                [sg.Text("Main: " + str(main_projects_path))],
                [sg.Text('_'  * 80)],
                [sg.Text("Create Project", )],
                [sg.Push(), sg.Text("Project Name: "), sg.Input(key='PROJECT_NAME'),],
                [sg.Push(), sg.Text("Sub Project Name: "), sg.Input(key='SUB_PROJECT_NAME')],
                
                [sg.Text('_'  * 80)],
                [sg.Push(), sg.Text("shot Acronym: "), sg.Input(key='SHOT_ACRONYM')],
                [sg.Push(), sg.Text("Shot Count: "), sg.Input(key='SHOT_COUNT')], 
                [sg.Push(),sg.Text("Resolution: "), sg.InputCombo(('1080p','720p','480p'), key="-RES-",)],
                [sg.Push(),sg.Text("ASPR: "), sg.InputCombo(('16x9','9x16'), key="-ASPR-",)],  
                [sg.Push(),sg.Text("FPS: "), sg.InputCombo(('24','25','30','60'), key="FPS",)], 
                [sg.Push(), sg.Text("Pipleline Type: "), sg.InputCombo(('pipe_a', 'pipe_b'), key="PIPELINE_TYPE")],
                [sg.Text('_'  * 80)],
                [sg.Push(), sg.Checkbox("Discord Sync: ", key="-DISCORD_SYNC-"),
                sg.Push(), sg.Checkbox("Publisher: ", key="-AUTO_PUBLISH-"),
                sg.Push(), sg.Checkbox("Guides: ", key="-GUIDES-")],

                [sg.Multiline(size=(60,15), font='Courier 8', expand_x=True, expand_y=True, write_only=True,
                            reroute_stdout=True, reroute_stderr=True, echo_stdout_stderr=True, autoscroll=True, auto_refresh=True, background_color="black",text_color="magenta", key="MULTI_TEXTBOX")],
 
                [sg.Push(), sg.Button('Build')] ]

    # Build UI
    window = sg.Window('PipeDreams Project Build', 
                        layout,
                        no_titlebar=False, 
                        resizable=False, 
                        use_custom_titlebar=True, 
                        finalize=False, 
                        keep_on_top=True,
                        titlebar_background_color=CREATE_WINDOW_BG_COLOR,
                        location=(screen_size()[0]-CREATE_WINDOW_NUDGE[0], screen_size()[1]-CREATE_WINDOW_NUDGE[1]),
                    
                        size=(CREATE_WINDOW_SIZE[0],CREATE_WINDOW_SIZE[1]),
                        alpha_channel=1,
                        titlebar_text_color=CREATE_WINDOW_TEXT_COLOR,
                        icon=icon_1,
                        titlebar_icon=icon_1,

                        )




    # Read UI
    event, values = window.read()



    # Do something with the information gathered
    if event == "Build":

        # main_projects_path = "D:/Dropbox/Dev/projects_dev"

        input_project_name = values["PROJECT_NAME"]
        input_sub_project_name = values["SUB_PROJECT_NAME"]

        shot_acronym = values["SHOT_ACRONYM"]
        shot_count = values["SHOT_COUNT"]
        pipeline_type = values["PIPELINE_TYPE"]

        resolution = values["-RES-"]
        aspect_ration = values["-ASPR-"]
        FPS = values["FPS"]

        discord_sync = values["-DISCORD_SYNC-"]
        Publisher = values["-AUTO_PUBLISH-"]
        Guides = values["-GUIDES-"]


        if input_project_name != '':

            build_project(
                            main_projects_path,
                            input_project_name,
                            input_sub_project_name,
            
                            pipeline_type,
                            shot_acronym,
                            shot_count,

                            resolution,
                            aspect_ration,
                            FPS,

                            discord_sync,
                            Publisher,
                            Guides
                        )

            # Pop up when done with window
            # sg.popup(f'Created Project: \n{input_project_name}\n{input_sub_project_name}\n{shot_acronym}\n{shot_count}\n\n{pipeline_type}')
            window["MULTI_TEXTBOX"].update("")

            # dots = '🔺'
            for i in range(50):
                time.sleep(0.01)
                # dots += "🔺"
                print("🔺" * 33)

            window["MULTI_TEXTBOX"].update("")

            print("-Created Project:")

            print("\n✔️Main_Name: " + input_project_name)
            print("✔️Sub_Name: " + input_sub_project_name)

            print("\n✔️ Acr: " + shot_acronym)
            print("✔️ Shot_Count: " + shot_count)

            print("\n✔️ Res: " + resolution)
            print("✔️ AspectR: " + aspect_ration)
            print("✔️ FPS: " + FPS)
            print("✔️ PipeType: " + pipeline_type)

            if discord_sync == True:
                print("✔️ Discord Sync: " + str(discord_sync))
            else:
                print("❌ Discord Sync: " + str(discord_sync))

            if Publisher == True:
                print("✔️ Publisher: " + str(Publisher))
            else:
                print("❌ Publisher: " + str(Publisher))

            if Guides == True:
                print("✔️ Guides: " + str(Guides))
            else:
                print("❌ Guides: " + str(Guides))

            print(f"\n✔️{main_projects_path}/{input_project_name}/{input_sub_project_name}")
            

    # window.close()





if __name__ == "__main__":

    icon_1 = ""

    # Open config
    config = get_UI_config()
    UI(config, icon_1)
