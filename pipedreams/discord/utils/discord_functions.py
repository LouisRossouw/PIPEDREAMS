import os
import yaml
import json



##### FUNCTIONS


def write_to_json(json_path, data):
    """ Create and write to json file """

    with open(json_path, 'w') as f:
        json.dump(data, f, indent=6)



def read_json(json_path):
    """ Reads json file """
    with open(json_path) as f:
        json_file = json.loads(f.read())

    return (json_file)


def readYaml(input_file):
    file_data = yaml.safe_load(open(input_file, 'r'))
    return(file_data)


def get_Projects():
    """ returns all projects on the hardrive / network created by Pipedreams """

    # returns all projects on the projects network path, created with Pipedreams
    pipeline_config = readYaml(f"{os.path.dirname(os.path.dirname(os.path.dirname(__file__)))}/admin/pipeline_config.yaml")
    pipeline_path = pipeline_config["Pipeline_Path"]

    projects_built_with_PipeDreams = []
    projects_lists = os.listdir(pipeline_path)

    for dir in projects_lists:
        dir_path = f"{pipeline_path}/{dir}"

        if os.path.isdir(dir_path):
            for subdir in os.listdir(dir_path):
                pipeline_data_dir = f"{dir_path}/{subdir}/data/pipeline"
                if os.path.exists(pipeline_data_dir):
                    
                    if readYaml(f"{pipeline_data_dir}/pipeline_data.yaml")["discord_sync"] == True:

                        # ensures we dont add double names into the list.
                        if dir not in projects_built_with_PipeDreams:
                            projects_built_with_PipeDreams.append(dir)

    return(pipeline_path, projects_built_with_PipeDreams)



def get_Discord_categories(BoxBloxx):
    """ Returns all CATAGORIES on server """

    DISCORD_CATEGORY_LIST = []
    for category in BoxBloxx.categories:
        DISCORD_CATEGORY_LIST.append(category) # object

    # category names
    category_list = []
    for category in DISCORD_CATEGORY_LIST:
        category_name = category.name
        category_list.append(category_name)

    return(category_list)



def get_Discord_channels(BoxBloxx):
    """Returns all CHANNELS on server"""

    DISCORD_CHANNEL_LIST = []
    for channel in BoxBloxx.channels:
        if str(channel.type) == 'text':
            DISCORD_CHANNEL_LIST.append(channel)

    # channel names
    channel_list = []
    for channel in DISCORD_CHANNEL_LIST:
        channel_name = channel.name
        channel_list.append(channel_name)

    return(channel_list)



if __name__ == "__main__":
    print(get_Projects())
    