import os
import sys
import yaml

main_path = os.path.dirname(os.path.dirname((__file__)))
sys.path.append(main_path) # /PIPEDREAMS/PipeDreams





def yaml_config(config_path):
    """ Open yaml configs """
    config = yaml.safe_load(open(config_path))
    return(config)




def getUsers():
    """ Returns users records """
    userName = os.environ['COMPUTERNAME']

    admin_config = yaml_config(f"{main_path}/admin/admin_config.yaml")
    artist_config = yaml_config(f"{main_path}/admin/artist_config.yaml")

    return(userName, admin_config, artist_config)




def check_admin():
    """ Checks the users in the data list """

    data = getUsers()
    userNames = data[0]
    admin_config = data[1]

    privilages = []

    for admin in admin_config["Admin"]:
        admin_list = admin_config["Admin"][admin]

        for usr in admin_list:
            if userNames == usr:
                privilages.append(admin)

    return(privilages)




def check_title():
    """ gets the users title """

    data = getUsers()
    userNames = data[0]
    artist_config = data[2]

    title = []

    for role in artist_config["Team"]:
        team_list = artist_config["Team"][role]

        for usr in team_list:
            if userNames == usr:
                title.append(role)

    return(title)




if __name__ == "__main__":
    print(check_title())
