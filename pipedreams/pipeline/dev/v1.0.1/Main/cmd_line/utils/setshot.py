import os
import utils.fancy as fancy
import utils.setShot_utils as ssUtils




def setShot(
        usr_input_project,
        usr_input_sub_project,
        usr_input_shot,
        config,
        working_dir,
        usr_input,
        Documents_pipeline_dir,
        ):

        """ This sets shot to a specific dir and launches a program into the dir """
        
        os.system('cls')

        project_name = f'{usr_input_project}_{usr_input_sub_project}_{usr_input_shot}'

        if usr_input == 'ss home':

                ss = 'home'

                fancy.cmd_setshot_help(usr_input_project, usr_input_sub_project, usr_input_shot)

                print(f'Working directory : {working_dir}')

                while usr_input != 'exit':

                        usr_input = input(f'\n$:{usr_input_project}_{usr_input_sub_project}_{usr_input_shot} : ')

                        ssUtils.open_application(usr_input, 
                                                working_dir,
                                                ss, 
                                                project_name,
                                                usr_input_project,
                                                usr_input_sub_project,
                                                usr_input_shot,
                                                config,
                                                Documents_pipeline_dir,
                                                )






        else:

                ss = 'project'

                fancy.cmd_setshot_help(usr_input_project, usr_input_sub_project, usr_input_shot)

                print(f'Working directory : {working_dir}')

                while usr_input != 'exit':

                        usr_input = input(f'\n$:{usr_input_project}_{usr_input_sub_project}_{usr_input_shot} : ')

                        ssUtils.open_application(usr_input, 
                                                working_dir, 
                                                ss, 
                                                project_name,
                                                usr_input_project,
                                                usr_input_sub_project,
                                                usr_input_shot,
                                                config,
                                                Documents_pipeline_dir,
                                                )




        # Clear cmds
        os.system('cls')
        fancy.cmd_title()
        fancy.cmd_shortcut_help()



if __name__ == '__main__':
    setShot(
            'samsung',
            'socials'
            'shot010'
        )

