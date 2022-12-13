import os
import json




def read_json(json_path):
    """ Reads json file """
    with open(json_path) as f:
        json_file = json.loads(f.read())

    return (json_file)



def getUserDataBase():
    """ gets and returns the current pipeline version to be used for the user based on privilages etc """

    user_data_base = f"{os.path.dirname(os.path.dirname(os.path.dirname(getPipelineRoot())))}/admin/data/user_data_base/{os.getenv('COMPUTERNAME')}.json"
    data = read_json(user_data_base)

    pipeline_version = data[os.getenv('COMPUTERNAME')]["pipeline_version"]
    modules_path = f"{(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))}/DCC/maya/modules"

    print("**************************", modules_path)


def getEnvPath():
    """ This gets the path to the extra enviroment paths """
    
    extra_env_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))))
    extra_env_text = f"{extra_env_path}/admin/data/environments/important_env.txt"

    return(extra_env_text)


def getPipelineRoot():

    ThisFile = os.path.dirname(__file__)
    PipeLine_Root = os.path.dirname(os.path.dirname(os.path.dirname(ThisFile)))

    return(PipeLine_Root)



def maya_env(working_dir, 
            shots, 
            shot_assets, 
            captures, 
            maya_dir_path, 
            shot_data, 
            project_name,
            usr_input_project,
            usr_input_sub_project,
            usr_input_shot,
            config,
            top_assets
            ):

    """ This function writes environment paths to mayas .env file so when maya runs, its set shot to a specific dir. """

    maya_version = str(config['maya_version'])

    Documents = os.path.expanduser('~\Documents')
    mayaENV_path = f'{Documents}\\maya\\{maya_version}'
    envFile = f'{mayaENV_path}\\Maya.env'

    try:
        os.remove(envFile)
    except FileNotFoundError as e:
        pass

    getUserDataBase()

    important_env_path = getEnvPath()

    # Pipeline_root = config['Pipeline_root']
    Pipeline_root = getPipelineRoot()

    set_environments = f'\nDCC = Maya\nPIPELINE_ROOT = {Pipeline_root}\nPROJECT_NAME = {project_name}\nPROJECT = {usr_input_project}\nSUB_PROJECT = {usr_input_sub_project}\nSHOT = {usr_input_shot}\nSHOT_ASSETS = {shot_assets}\nTOP_ASSETS = {top_assets}\nCAPTURES = {captures}\nMAYA_USR = {maya_dir_path}\nSHOT_DATA = {shot_data}'

    # opens the custom but permanent env paths that will merge with the set shot paths
    # opens permanent env paths
    with open(important_env_path, 'r') as f:
        important_env = f.readlines()
    

    # loops and appends to the maya.env
    for text in important_env:
        clean_text = text.rstrip('\n')
        print(clean_text)
        with open(envFile, 'a') as env:
            env.write(str('\n' + clean_text))

    # outside the loop it then appends the set_env variables
    with open(envFile, 'a') as env:
        env.write(set_environments)

    print(set_environments)



def houdini_env(working_dir,
                shots,
                shot_assets,
                captures,
                maya_dir_path,
                shot_data,
                project_name,
                usr_input_project,
                usr_input_sub_project,
                usr_input_shot,
                config,
                ):
    """ This function writes environment paths to Houdini .env file so when Houdini runs, its set shot to a specific dir. """

    print('houdini env works')










if __name__ == '__main__':
    #getPipelineRoot()
    getEnvPath()
