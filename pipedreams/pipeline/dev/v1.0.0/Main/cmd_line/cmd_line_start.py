""" 
cmd_line_start.py launches the command line interface for the user, this is where he can performance
multiple commands, Set shots, launch DCCs etc

 """

import os
import yaml
import readline



def checkDirs(Documents_pipeline_dir):

    if os.path.exists(Documents_pipeline_dir) != True:
        os.mkdir(Documents_pipeline_dir)
        os.mkdir(Documents_pipeline_dir + '\\data')




def run():


    import utils.fancy as fancy
    from utils.quick_load import quick_load
    import utils.setShot_utils as ssUtils
    from utils.project_list import list_all
    from utils.setshot import setShot
    from utils.build_project import UI


    os.system('cls')
    fancy.cmd_title()
    fancy.cmd_shortcut_help()

    def autoComplete(text, state):
        for cmd in dirs:
            if cmd.startswith(text):
                if not state:
                    return cmd
                else:
                    state -= 1

    # Open config
    config_path = os.path.abspath(__file__)
    config = yaml.safe_load(open(f'{os.path.dirname(config_path)}\\config.yaml', 'r'))

    # Projetcs path from config
    Pipeline_Path_name = config['Pipeline_name']
    projects = config['Pipeline_Path']
    maya_version = config['maya_version']

    # check if pipedreams exists and creates it if not
    Documents_path = os.path.join(os.path.join(os.path.expanduser('~')), 'Documents')
    Documents_pipeline_dir = f'{Documents_path}\\{Pipeline_Path_name}'


    # make dirs if not exist
    checkDirs(Documents_pipeline_dir)

    home_dir = f"{Documents_path}/projects"



    usr_input = ''

    while usr_input != 'exit':

        usr_input = input('\n$ ')

        if usr_input == 'np':
            os.system('notepad.exe')

        elif usr_input == 'opl':

            maya_quick_load = quick_load(Documents_pipeline_dir)

            usr_input = maya_quick_load['usr_input']
            working_dir_shots = maya_quick_load['maya_last_working_dir']
            ss = maya_quick_load['ss']
            project_name = maya_quick_load['project_name']
            usr_input_project = maya_quick_load['usr_input_project']
            usr_input_sub_project = maya_quick_load['usr_input_sub_project']
            usr_input_shot = maya_quick_load['usr_input_shot']

            project_check = ''
            sub_project_check = ''
            shot_check = ''

            usr_input_value = ''

            while not (project_check == True or usr_input_value == 'exit'):

                # for autocomplete
                dirs = os.listdir(working_dir_shots)

                for i in range(len(dirs)):
                    dirs[i] = dirs[i].lower()

                readline.parse_and_bind("tab: complete")
                readline.set_completer(autoComplete)

                project_name_sliced = project_name[0:-3]

                usr_input_value = input(f'\n{project_name_sliced} : ')
                usr_input_shot = usr_input_shot[0:-3] + str(usr_input_value)

                working_dir = working_dir_shots + '\\' + usr_input_shot


                project_check = os.path.exists(working_dir)

                if project_check == True:

                    setShot(
                            usr_input_project,
                            usr_input_sub_project,
                            usr_input_shot,
                            config,
                            working_dir,
                            usr_input,
                            Documents_pipeline_dir
                            )
                else:
                    pass

        elif usr_input == 'ss home':

            Documents = os.path.expanduser('~\Documents')
            mayaENV_home_path = f'{Documents}\\maya\\'
            working_dir = f'{mayaENV_home_path}\\projects\\default\\'


            usr_input_project = ''
            usr_input_sub_project = ''
            usr_input_shot = 'home'
            working_dir = home_dir
            # usr_input = ''


            setShot(
                    usr_input_project,
                    usr_input_sub_project,
                    usr_input_shot,
                    config,
                    working_dir,
                    usr_input,
                    Documents_pipeline_dir
                    )

        # Set Shot
        elif usr_input == 'ss':

            project_check = ''
            sub_project_check = ''
            shot_check = ''

            usr_input_project = ''
            
            while not (project_check == True or usr_input_project == 'exit'):

                # for autocomplete
                dirs = os.listdir(projects)

                for i in range(len(dirs)):
                    dirs[i] = dirs[i].lower()

                readline.parse_and_bind("tab: complete")
                readline.set_completer(autoComplete)

                usr_input_project = input('\nSet Project : ')
                dir_check = f'{projects}\\{usr_input_project}'
                project_check = os.path.exists(dir_check)

            while not (sub_project_check == True or usr_input_project == 'exit'):

                # for autocomplete
                dirs = os.listdir(f'{projects}\\{usr_input_project}')

                for i in range(len(dirs)):
                    dirs[i] = dirs[i].lower()

                readline.parse_and_bind("tab: complete")
                readline.set_completer(autoComplete)

                usr_input_sub_project = input('\nSet Sub project : ')
                dir_check = f'{projects}\\{usr_input_project}\\{usr_input_sub_project}'
                sub_project_check = os.path.exists(dir_check)

            while not (shot_check == True or usr_input_project == 'exit'):

                # read pipeline data here - this is to point to the correct location to find the shots dir
                proj = (f'{projects}\\{usr_input_project}\\{usr_input_sub_project}')
                pipeline_data_path = f'{proj}\\data\\pipeline\\pipeline_data.yaml'
                pipeline_data_file = yaml.safe_load(open(pipeline_data_path, 'r'))

                pipeline_type = pipeline_data_file['pipeline_type']

                # default structure
                if pipeline_type == 'pipe_a':
                    shots_path = "shots"
                # default structure for online render farm
                if pipeline_type == 'pipe_b':
                    shots_path = "scenes"

                print(f'\npipeline_type : {pipeline_type}')


                # for autocomplete
                dirs = os.listdir(f'{projects}\\{usr_input_project}\\{usr_input_sub_project}\\{shots_path}')

                for i in range(len(dirs)):
                    dirs[i] = dirs[i].lower()

                readline.parse_and_bind("tab: complete")
                readline.set_completer(autoComplete)

                usr_input_shot = input('\nSet Shot : ')
                dir_check = f'{projects}\\{usr_input_project}\\{usr_input_sub_project}\\{shots_path}\\{usr_input_shot}'
                shot_check = os.path.exists(dir_check)
            
            working_dir = f'{projects}\\{usr_input_project}\\{usr_input_sub_project}\\{shots_path}\\{usr_input_shot}'

            os.system('cls')
            fancy.cmd_title()
            fancy.cmd_shortcut_help()

            setShot(
                    usr_input_project,
                    usr_input_sub_project,
                    usr_input_shot,
                    config,
                    working_dir,
                    usr_input,
                    Documents_pipeline_dir,
                    )

        # List directories in projects
        elif usr_input == 'ls':
            list_all(
                    projects, 
                    config
                    )

        elif usr_input == 'cp':
            UI(
                config
                )
            


    # clears cmd line
    os.system('cls')





if __name__ == "__main__":

    run()