import os
import sys
import json
import yaml
import imp
import utils.env as env

imp.reload(env)





def read_json(json_path):
    """ Reads json file """
    with open(json_path) as f:
        json_file = json.loads(f.read())

    return (json_file)

def getPipelineRoot():

    ThisFile = os.path.dirname(__file__)
    PipeLine_Root = os.path.dirname(os.path.dirname(os.path.dirname(ThisFile)))

    return(PipeLine_Root)


def getUserDataBase():
    """ gets and returns the current pipeline version to be used for the user based on privilages etc """

    user_data_base = f"{os.path.dirname(os.path.dirname(os.path.dirname(getPipelineRoot())))}/admin/data/user_data_base/{os.getenv('COMPUTERNAME')}.json"
    data = read_json(user_data_base)

    pipeline_version = data[os.getenv('COMPUTERNAME')]["pipeline_version"]
    pipeline_path_to_version = data[os.getenv('COMPUTERNAME')]["pipeline_version_path"]

    return(pipeline_version, pipeline_path_to_version)



def updateModule():
    """ updates mayas modules to point to the latest production build version of pipedreams """

    Documents_path = os.path.expanduser('~')
    if "Documents" not in Documents_path:
        Documents_path += "/Documents"

    pipedreams_mod_path = f"{Documents_path}/maya/modules/PipeDreams.mod"
    modules_dir_path = f"{Documents_path}/maya/modules"

    if os.path.exists(modules_dir_path) != True:
        os.mkdir(modules_dir_path)

    with open(pipedreams_mod_path, "w") as f:

        version = getUserDataBase()[0]
        pipeline_path_to_version = getUserDataBase()[1]
        text = f"+ PipeDreams {str(version)} {pipeline_path_to_version}\DCC\maya \nscripts: {pipeline_path_to_version}\DCC\maya"
        f.write(text)




def create_dir(working_dir):

    users = os.path.dirname(working_dir)
    shot = os.path.dirname(os.path.dirname(working_dir))
    captures = f'{os.path.dirname(os.path.dirname(working_dir))}\\captures'
    assets = f'{os.path.dirname(os.path.dirname(working_dir))}\\assets'


    print(assets)


    return(users, shot, captures, assets)





def open_application(usr_input, 
                    working_dir, 
                    ss, 
                    project_name,
                    usr_input_project,
                    usr_input_sub_project,
                    usr_input_shot,
                    config,
                    Documents_pipeline_dir,
                    ):
    """ """

    maya_version = str(config['maya_version'])
    houdini_version = str(config['houdini_version'])
    # home_dir = str(config['home_dir'])
    home_dir = f"{os.path.join(os.path.join(os.path.expanduser('~')), 'Documents')}/projects"

    user_name = os.environ['COMPUTERNAME'].lower()

    updateModule()

    if ss == 'home':

        user_path = working_dir
        maya_dir_path = f'{user_path}\\scenes'
        houdini_dir_path = f'{user_path}\\scenes'


        if os.path.exists(user_path) != True:
            os.mkdir(user_path)

        users = os.path.dirname(working_dir)
        shot = working_dir
        captures = f'{working_dir}\\movies'
        shot_assets = f'{working_dir}\\assets'
        top_assets = f'{working_dir}'
        shot_data = f'{working_dir}\\data'



    elif ss == 'project':

        # read pipeline data here - this is to know what kind of file structure maya needs to use to set paths in the .env
        proj = f'{os.path.dirname(os.path.dirname(working_dir))}'
        pipeline_data_path = f'{proj}\\data\\pipeline\\pipeline_data.yaml'
        pipeline_data_file = yaml.safe_load(open(pipeline_data_path, 'r'))

        pipeline_type = pipeline_data_file['pipeline_type']

        # default structure
        if pipeline_type == 'pipe_a':

            user_path = f'{working_dir}\\users\\{user_name}'
            maya_dir_path = user_path + '\\maya'
            houdini_dir_path = user_path + '\\houdini'

            users = os.path.dirname(working_dir)
            shot = os.path.dirname(os.path.dirname(working_dir))
            captures = f'{working_dir}\\captures'
            shot_assets = working_dir + '\\assets'
            top_assets = f'{os.path.dirname(os.path.dirname(working_dir))}\\assets'
            shot_data = f'{working_dir}\\data'

        # Zambon structure - for online rendering for maya
        elif pipeline_type == 'pipe_b':

            user_path = f'{working_dir}\\users\\{user_name}'
            maya_dir_path = user_path + '\\maya'
            houdini_dir_path = user_path + '\\houdini'

            users = os.path.dirname(working_dir)
            shot = os.path.dirname(os.path.dirname(working_dir))
            captures = f'{working_dir}\\captures'
            shot_assets = working_dir + '\\assets'
            top_assets = f'{os.path.dirname(os.path.dirname(working_dir))}\\assets'
            shot_data = f'{working_dir}\\data'



        # Check if username exists within shot path
        if os.path.exists(user_path) != True:
            os.mkdir(user_path)
        else:
            pass

    
    # execute programs and check paths

    # Maya
    if usr_input == 'ma':

        if ss != 'home':

            data = {}
            data['usr_input'] = usr_input
            data['maya_last_working_dir'] = os.path.dirname(working_dir)
            data['ss'] = ss
            data['project_name'] = project_name
            data['usr_input_project'] = usr_input_project
            data['usr_input_sub_project'] = usr_input_sub_project
            data['usr_input_shot'] = usr_input_shot

            # write to documents/pipeline_name/data as a last open info data
            maya_last_save = Documents_pipeline_dir + '\\data\\maya_quickload.json'
            with open(maya_last_save, 'w') as f:
                json.dump(data, f, indent=4)


        if os.path.exists(working_dir + '\\users') != True:
            os.mkdir(working_dir + '\\users')

        if os.path.exists(user_path) != True:
            os.mkdir(user_path)
        
        if os.path.exists(maya_dir_path) != True:
            os.mkdir(maya_dir_path)

        sys.path.append("C:/custom_program_files/pipeline/PipeDreams/maya/scripts")


        env.maya_env(working_dir,
                    shot,
                    shot_assets,
                    captures,
                    maya_dir_path,
                    shot_data,
                    project_name,
                    usr_input_project,
                    usr_input_sub_project,
                    usr_input_shot,
                    config,
                    top_assets,
                    )

        program_path = f'"C:\\Program Files\\Autodesk\\Maya{maya_version}\\bin\\maya.exe"'
        os.startfile(f'"{program_path}"')


    # Houdini
    elif usr_input == 'he':

        if os.path.exists(working_dir + '\\users') != True:
            os.mkdir(working_dir + '\\users')

        if os.path.exists(user_path) != True:
            os.mkdir(user_path)

        if os.path.exists(houdini_dir_path) != True:
            os.mkdir(houdini_dir_path)


        program_path = f'"C:\\Program Files\\Side Effects Software\\Houdini {houdini_version}\\bin\\houdinifx.exe"'
        os.startfile(f'"{program_path}"')

        










if __name__ == '__main__':
    working_dir = "C:\\Users\\Louis\\Dropbox\\Arcade\\structure_idea\\Projects\\samsung\\socials\\shots\\soc010\\users\\Louis"
    usr_input = ''

    #open_application(usr_input, working_dir)

    getUserDataBase()