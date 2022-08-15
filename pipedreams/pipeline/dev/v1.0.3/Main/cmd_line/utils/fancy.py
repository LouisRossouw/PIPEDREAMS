import os

def cmd_title():
    """ Title for this cmd line program """

    print('\n-------------------------------------------------------')
    print('                     PIPEDREAMS                          ')
    # print('-------------------------------------------------------')

def cmd_shortcut_help():
    """ Shortcuts help """

    print('-------------------------------------------------------')
    print('ls = list all projects | ss = set shot | np = notepad | exit = exit')
    print('-------------------------------------------------------')

def cmd_setshot_help(usr_input_project, usr_input_sub_project, usr_input_shot):


    shot = f'{usr_input_project}_{usr_input_sub_project}_{usr_input_shot}'
    
    print(f'                    {shot}')
    print('-------------------------------------------------------')  
    print('ma = Maya | he = Houdini | exit = exit')
    print('-------------------------------------------------------')

def cmd_line():
    """ Simple line """
    print('-------------------------------------------------------') 
    