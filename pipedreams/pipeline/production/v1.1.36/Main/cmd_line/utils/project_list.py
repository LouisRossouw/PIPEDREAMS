import os
import utils.fancy as fancy


def list_all(projects, config):
    """ for loop that returns all the directory names in projects folder """

    projects_list = os.listdir(projects)

    fancy.cmd_line()

    for proj in projects_list:
        
        sub = f'{projects}\\{proj}\\'
        sub_proj = os.listdir(sub)
    
        # print(f'{proj} - {sub_proj}')
        print(proj)

    fancy.cmd_line()




if __name__ == '__main__':
    list_all()

