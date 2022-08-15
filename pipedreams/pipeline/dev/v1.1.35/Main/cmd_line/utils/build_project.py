import os
import yaml
import PySimpleGUI as sg

# Fixes blurry issues on UI for win10 high DPI displays
from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)



def create_config(pipeline_path, pipeline_type):
    """ This creates a yaml config file for pipeline_type """

    pipeline_config_path = f'{pipeline_path}/pipeline_data.yaml'

    data = {"pipeline_type" : pipeline_type}

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
        create_config(pipeline, pipeline_type)



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





def UI(config):
    """ builds a UI for the project creator """

    print("Launching project creator")

    # Config
    main_projects_path = config["Pipeline_Path"]

    # Theme
    sg.theme('DarkGrey14') 
    # sg.theme('DarkGrey15') 
    # sg.theme('SystemDefaultForReal') 
    # sg.theme('Black') 
    # sg.theme('LightGreen4') 
    # sg.theme('Topanga') 
    # sg.theme('DarkTeal3') 

    # Top UI layout
    top_menu = [['Rockettotheskies', ['dev', 'test', 'Exit', 'Properties']],      
                ['Edit', ['Paste', ['Special', 'Normal', ], 'Undo'], ],      
                ['Help', 'About'], ]   



    # Build UI layout
    layout = [  
                [sg.Menu(top_menu, tearoff=True)],
                [sg.Text("Main: " + str(main_projects_path))],
                [sg.Text('_'  * 80)],
                [sg.Text("Create Project")],
                [sg.Push(), sg.Text("Project Name: "), sg.Input(key='PROJECT_NAME'),],
                [sg.Push(), sg.Text("Sub Project Name: "), sg.Input(key='SUB_PROJECT_NAME')],
                
                [sg.Text('_'  * 80)],
                [sg.Push(), sg.Text("shot Acronym: "), sg.Input(key='SHOT_ACRONYM')],
                [sg.Push(), sg.Text("Shot Count: "), sg.Input(key='SHOT_COUNT')], 
                [sg.Text("Pipleline Type: "), sg.InputCombo(('pipe_a', 'pipe_b'), key="PIPELINE_TYPE")],
                [sg.Text('_'  * 80)],

                [sg.Multiline(size=(60,15), font='Courier 8', expand_x=True, expand_y=True, write_only=True,
                            reroute_stdout=True, reroute_stderr=True, echo_stdout_stderr=True, autoscroll=True, auto_refresh=True)],
 
                [sg.Push(), sg.Button('Build')] ]

    # Build UI
    window = sg.Window('PipeDreams Project Build', layout)      # Part 3 - Window Defintion

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

        if input_project_name != '':

            build_project(
                            main_projects_path,
                            input_project_name,
                            input_sub_project_name,
            
                            pipeline_type,
                            shot_acronym,
                            shot_count,
                        )

            # Pop up when done with window
            sg.popup(f'Created Project: \n{input_project_name}\n{input_sub_project_name}\n{shot_acronym}\n{shot_count}\n\n{pipeline_type}')   


    window.close()





if __name__ == "__main__":

    # Open config
    config = yaml.safe_load(open(f'{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}\\config.yaml', 'r'))
    UI(config)



    # main_projects_path = "D:/Dropbox/Dev/projects_dev"
    # input_project_name = "project_name"
    # input_sub_project_name = "sub_project_name"   
    #
    #
    # pipeline_type = "pipe_a"
    # shot_acronym = "bob"
    # shot_count = 5
    #
    #
    # build_project(
    #                 main_projects_path,
    #                 input_project_name,
    #                 input_sub_project_name,
    #
    #                 pipeline_type,
    #                 shot_acronym,
    #                 shot_count,
    #               )