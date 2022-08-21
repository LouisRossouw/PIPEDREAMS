import os
import sys
import yaml
import PySimpleGUI as sg
import threading

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# from toolUtils.setshot import setShot
import utils.setShot_utils as ssUtils


# Fixes blurry issues on UI for win10 high DPI displays
from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)


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



def get_tasks():
    """ Returns a list of tasks for user """

    task_list = ["samsung_brandday_sh010", "roblox_anim_rbx010", "roblox_anim_rbx020", "cultura_anim_rigging"]

    return(task_list)


def get_all_projects_list(path):
    """ This returns a list of all the projects """

    projects_lists = os.listdir(path)
    
    return(projects_lists)



def PipeDreams_UI(config):
    """ The Main PipeDreams UI """

    # sg.theme('DarkGrey14') 
    sg.theme('Default1') 

    # Config
    Pipeline_name = config["Pipeline_name"]
    main_projects_path = config["Pipeline_Path"]


    # Top UI layout
    top_menu = [
                    ['File', ['dev','Properties', 'Exit']],      
                    ['Edit', ['Paste', ['Special', 'Normal', ], 'Undo'], ],      
                    ['Help', 'About'], 
                ]   



    # TABS
    Pipedreams_TAB_01 = [
                            [sg.Text("Main: " + main_projects_path)],
                            [sg.Text('_'  * 80)],

                            [sg.Text("Task")],
                            [sg.Listbox(values=get_tasks(), 
                            size =(20, 12),)],

                            [sg.Text("SetShot: "), sg.InputCombo((get_all_projects_list(main_projects_path)), enable_events=True, key="MAIN_PROJECT", size=(20,15)), 
                            sg.InputCombo(("None"), enable_events=True,  key="SUB_PROJECT", size=(20,15)),
                            sg.InputCombo(('None'), enable_events=True,  key="SHOT", size=(20,15)),
                            sg.Button("Maya", enable_events=True), sg.Button("Houdini", enable_events=True)],

                            [sg.Multiline(size=(10,5), font='Courier 8', expand_x=True, expand_y=True, write_only=True,
                                        reroute_stdout=True, reroute_stderr=True, echo_stdout_stderr=True, autoscroll=True, auto_refresh=True)],
                        ]
       

    CreateProject_TAB_02 = [
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

                                [sg.Multiline(size=(10,5), font='Courier 8', expand_x=True, expand_y=True, write_only=True,
                                            reroute_stdout=True, reroute_stderr=True, echo_stdout_stderr=True, autoscroll=True, auto_refresh=True)],
                
                                [sg.Push(), sg.Button('Build')]
                            ]

    tools_TAB = [[sg.Text('This is inside ofhjhj tab')]]
    UTILS_tab_group = sg.TabGroup([[sg.Tab('Create Project', CreateProject_TAB_02), sg.Tab('Tools', tools_TAB)]])

    Utils_TAB_03 = [
                        [sg.Text('Tab 3')],
                        [UTILS_tab_group]
                   ]



    # The TabgGroup layout - it must contain only Tabs
    tab_group_layout = [
                            [sg.Tab('PipeDreams', Pipedreams_TAB_01, font='Courier 15', key='-TAB1-'),
                            sg.Tab('Utils', Utils_TAB_03, visible=True, key='-TAB3-'),]
                        ]



    # The window layout - defines the entire window
    layout = [
                [sg.Menu(top_menu, tearoff=False)],
                [sg.Text("tmp")],
                [sg.TabGroup(tab_group_layout, enable_events=True, key='-TABGROUP-')],
                [sg.Text('_'  * 80)],
                [sg.Button("dev")]
             ]



    window = sg.Window(
                        'PipeDreams', 
                        layout, 
                        no_titlebar=False, 
                        resizable=True, 
                        use_custom_titlebar=True, 
                        finalize=False, 
                        keep_on_top=False,
                        titlebar_background_color="darkGrey"
                        )

    tab_keys = ('-TAB1-','-TAB2-','-TAB3-', '-TAB4-')

    while True:
        
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break

        if event == 'Select':
            window[tab_keys[int(values['-IN-'])-1]].select()

        # SetShot
        if event == 'MAIN_PROJECT':
            selected_MAIN_project = values["MAIN_PROJECT"]
            window['SUB_PROJECT'].update(value='', values=get_all_projects_list(f'{main_projects_path}/{selected_MAIN_project}'))

        # SetShot
        if event == 'SUB_PROJECT':
            selected_SUB_project = values["SUB_PROJECT"]
            window['SHOT'].update(value='', values=get_all_projects_list(f'{main_projects_path}/{selected_MAIN_project}/{selected_SUB_project}/shots'))

        # SetShot
        if event == 'SHOT':
            selected_SHOT = values["SHOT"]
            print(f'SetShot to: {main_projects_path}/{selected_MAIN_project}/{selected_SUB_project}/shots/{selected_SHOT}')

        if event == "Maya":

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

            # This launches a new process
            threading.Thread(target=ssUtils.open_application, args=(                                                                            usr_input, 
                                                                            working_dir, 
                                                                            ss, 
                                                                            project_name,
                                                                            MAIN_PROJECT,
                                                                            SUB_PROJECT,
                                                                            SHOT,
                                                                            config,
                                                                            Documents_pipeline_dir), 

                                                                            daemon=True).start()






    window.close()





if __name__ == "__main__":

    # Open config
    config = yaml.safe_load(open(f'{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}\\config.yaml', 'r'))
    PipeDreams_UI(config)
