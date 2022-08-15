import os
import sys
import time
import yaml
import threading

import PySimpleGUI as sg

sys.path.append(f'{os.path.dirname(os.path.dirname(__file__))}/cmd_line')

import utils.setShot_utils as ssUtils
import Utils.UI_create_project as UI_create_project


# Fixes blurry issues on UI for win10 high DPI displays
from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)




def getPaths():
    """ dynamically returns common paths based on a predictable structure """

    version_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    build_path = os.path.dirname(version_path)
    resources_path = os.path.dirname(build_path)+"/resources"
    pipedreams_path = os.path.dirname(os.path.dirname(build_path))


    build_type = os.path.basename(build_path)
    version = os.path.basename(version_path)

    user_data_base = f"{pipedreams_path}/admin/data/user_data_base/user_data_base.json"
    
    return(build_type, version, user_data_base, resources_path)




def returnIconPath(paths):
    """ dynamically returns the paths to the icons """

    main_icon = f"{paths}/windows_tray_icons/tray_icon_animations/default_colors/px_1.png"
    maya_icon = f"{paths}/UI/maya_20.png"
    houdini_icon = f"{paths}/UI/houdini_20.png"

    icons={
        "main_icon" : main_icon,
        "maya_icon" : maya_icon,
        "houdini_icon" : houdini_icon,
        }

    return(icons)


def notification(DCC, Title, Message, icons_dict_input):
    """ Simple notification popup """
    
    if DCC == "Maya":
        icons = icons_dict_input["maya_icon"]
    elif DCC == "Houdini":
        icons = icons_dict_input["houdini_icon"]

    """ Simple notification """
    sg.SystemTray.notify(title=" "*10 + Title, 
                        message=" "*10 + Message,
                        icon=icons,
                        fade_in_duration=100,
                        display_duration_in_ms=2000,
                        alpha=1,
                        location=(2500,1),
                        )





def readYaml(input_file):
    file_data = yaml.safe_load(open(input_file, 'r'))
    return(file_data)

def getConfig():
    config = yaml.safe_load(open(f'{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}/cmd_line/config.yaml', 'r'))
    return(config)


def Documents_pipe(Pipeline_name):
    """ Checks if the pipeline user documents folder exists """

    # check if pipedreams exists and creates it if not
    Documents_path = os.path.join(os.path.join(os.path.expanduser('~')), 'Documents')
    Documents_pipeline_dir = f'{Documents_path}\\{Pipeline_name}'
    # make dirs if not exist
    if os.path.exists(Documents_pipeline_dir) != True:
        os.mkdir(Documents_pipeline_dir)
        os.mkdir(Documents_pipeline_dir + '\\data')

    return(Documents_pipeline_dir)



def project_data_print(type, pipeline_data):
    """ returns data about the selected projects """
    try:
        if type == "SUB_PROJECT":
            data = readYaml(pipeline_data)
            print("\n✔️ PipeType: " + data["pipeline_type"])
            print("✔️ Res: " + str(data["Resolution"]))
            print("✔️ AspectR: " + str(data["ASPR"]))
            print("✔️ FPS: " + str(data["FPS"]))
    except Exception:
        print("\n❌NO existing pipeline data")

def get_all_projects_list(path):
    """ This returns a list of all the projects """

    projects_lists = os.listdir(path)
    
    return(projects_lists)








def PipeDreams_UI(config):
    """ The Main PipeDreams UI """

    returnPathsNames = getPaths()
    icons_dict = returnIconPath(returnPathsNames[3])

    sg.theme('DarkGrey8') 
    # sg.theme('Default1') 

    # Config
    Pipeline_name = config["Pipeline_name"]
    main_projects_path = config["Pipeline_Path"]


    # TABS
    Pipedreams_TAB_01 = [
                            [sg.Text("Main: " + main_projects_path)],
                            [sg.Text('_'  * 80)],

                            [sg.Text("SetShot: "), sg.InputCombo((get_all_projects_list(main_projects_path)), enable_events=True, key="MAIN_PROJECT", size=(10,5)), 
                            sg.InputCombo(("None"), enable_events=True,  key="SUB_PROJECT", size=(10,5)),
                            sg.InputCombo(('None'), enable_events=True,  key="SHOT", size=(10,15)),
                            sg.Button("", enable_events=True, image_filename=icons_dict["maya_icon"], size=(1,10), tooltip="Launch Maya", key="Maya"), sg.Button("", enable_events=True, image_filename=icons_dict["houdini_icon"], size=(1,10),tooltip="Launch Houdini")],

                        ]
       



    Utils_TAB_02 = [
                        [sg.Button('Create Project', enable_events=True, key="-CreateProject-")],
                   ]



    # The TabgGroup layout - it must contain only Tabs
    tab_group_layout = [
                            [sg.Tab('Projects', Pipedreams_TAB_01, font='Courier 15', key='-TAB1-'),
                            sg.Tab('Utils', Utils_TAB_02, visible=True, key='-TAB2-'),]
                        ]



    # The window layout - defines the entire window
    layout = [

                [sg.TabGroup(tab_group_layout, enable_events=True, key='-TABGROUP-',background_color="black")],

				[sg.Multiline(size=(5,2), font='Courier 8', expand_x=True, expand_y=True, write_only=False,
							reroute_stdout=True, reroute_stderr=True, echo_stdout_stderr=True, autoscroll=True, auto_refresh=True, background_color="black",text_color="magenta", key="MULTI_TEXTBOX")],

             ]


    if returnPathsNames[0] != "production":
        Window_Name = 'PipeDreams_' + returnPathsNames[0] + ' ' + returnPathsNames[1]
    else:
        Window_Name = 'PipeDreams ' + returnPathsNames[1]

    window = sg.Window(
                        Window_Name, 
                        layout,
                        no_titlebar=False, 
                        resizable=False, 
                        use_custom_titlebar=True, 
                        finalize=False, 
                        keep_on_top=True,
                        titlebar_background_color="black",
                        location=(4520,1100),
                        size=(500,260),
                        alpha_channel=1,
                        titlebar_text_color="white",
                        icon=icons_dict["main_icon"],
                        titlebar_icon=icons_dict["main_icon"],
                        

                        )

    tab_keys = ('-TAB1-','-TAB2-','-TAB3-', '-TAB4-')

    while True:
        
        event, values = window.read()


        if event == sg.WIN_CLOSED:
            break



        if event == "-CreateProject-":
            UI_create_project.UI(config, icons_dict["main_icon"])


        if event == 'Select':
            window[tab_keys[int(values['-IN-'])-1]].select()


            
        # SetShot
        if event == 'MAIN_PROJECT':
            selected_MAIN_project = values["MAIN_PROJECT"]
            list_projects = get_all_projects_list(f'{main_projects_path}/{selected_MAIN_project}')
            window['SUB_PROJECT'].update(value='', values=list_projects)
            window["MULTI_TEXTBOX"].update(selected_MAIN_project)

            print(str(os.listdir(f'{main_projects_path}/{selected_MAIN_project}')))

        # SetShot
        if event == 'SUB_PROJECT':
            selected_SUB_project = values["SUB_PROJECT"]
            window['SHOT'].update(value='', values=get_all_projects_list(f'{main_projects_path}/{selected_MAIN_project}/{selected_SUB_project}/shots'))
            window["MULTI_TEXTBOX"].update(selected_MAIN_project + "/" +selected_SUB_project + ":")

            # prints info on the current selected project
            pipeline_data_path = (f'{main_projects_path}/{selected_MAIN_project}/{selected_SUB_project}\\data\\pipeline\\pipeline_data.yaml')
            project_data_print(
                                type="SUB_PROJECT", 
                                pipeline_data=pipeline_data_path, 
                                )
            


        # SetShot
        if event == 'SHOT':
            selected_SHOT = values["SHOT"]
            setshot_text = (f'{main_projects_path}/{selected_MAIN_project}/{selected_SUB_project}/shots/{selected_SHOT}')
            window["MULTI_TEXTBOX"].update("Shot Set to: \n\n" + setshot_text)

            

		# Launch Maya
        if event == "Maya":
            window["MULTI_TEXTBOX"].update("")
            dots = 'Launching Maya.'
            for i in range(30):
                time.sleep(0.01)
                dots += "🔺"
                print(dots)



            text = ("*** Maya PipeDreams toolSet: " + returnPathsNames[0] + "_" + returnPathsNames[1])
            window["MULTI_TEXTBOX"].update(text)

            MAIN_PROJECT = values["MAIN_PROJECT"]
            SUB_PROJECT = values["SUB_PROJECT"]
            SHOT = values["SHOT"]
            working_dir = f'{main_projects_path}/{MAIN_PROJECT}/{SUB_PROJECT}/shots/{SHOT}'
            usr_input = "ma"
            project_name = f'{MAIN_PROJECT}_{SUB_PROJECT}_{SHOT}'
            Documents_pipeline_dir = Documents_pipe(Pipeline_name)
            ss = "project"

            print(f'Launching Maya')
            print(working_dir)

            notification(DCC = "Maya",
                        Title = "Launching",
                        Message = project_name,
                        icons_dict_input = icons_dict
                        )
            

            # This launches a new process
            threading.Thread(target=ssUtils.open_application, args=(        usr_input, 
                                                                            working_dir, 
                                                                            ss, 
                                                                            project_name,
                                                                            MAIN_PROJECT,
                                                                            SUB_PROJECT,
                                                                            SHOT,
                                                                            config,
                                                                            Documents_pipeline_dir), 

                                                                            daemon=True).start()
            
            


        if event == "-TASK_LIST-":
            window['-OUTPUT-'].update(values="test")


    window.close()





if __name__ == "__main__":

    # Open config
    config = yaml.safe_load(open(f'{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}/cmd_line/config.yaml', 'r'))
    PipeDreams_UI(config)
