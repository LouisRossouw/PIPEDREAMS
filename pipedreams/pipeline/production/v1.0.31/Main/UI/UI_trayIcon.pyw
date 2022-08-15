
import PySimpleGUI as sg

import UI_start_compact as UI_Compact


icon_path_1 = "D:/work/projects/dev/projects/PIPEDREAMS/pipedreams/pipeline/resources/windows_tray_icons/tray_icon_animations/default_colors/px_1.png"
icon_path_2 = "D:/work/projects/dev/projects/PIPEDREAMS/pipedreams/pipeline/resources/windows_tray_icons/tray_icon_animations/default_colors/px_2.png"

sg.theme('DarkGrey9')




def notification():
    """ Simple notification """
    sg.SystemTray.notify(title="kkkkk", 
                        message="helllo",
                        icon=icon_path_1,
                        fade_in_duration=500,
                        display_duration_in_ms=2000,
                        alpha=1,
                        location=(2500,1))





def animCount(count, tray):

    if count == 1:
        tray.Update(filename=icon_path_1)
    if count == 2:
        tray.Update(filename=icon_path_2)

    if count == 2:
        count = 0

    return(count)



def main():

    menu_def = ['UNUSED', ['PipeDreams', '---', 'Dev',['test', 'test2'] ,'Exit']]
    
    tray = sg.SystemTray(menu=menu_def, filename=icon_path_1)
    window= ''

    count = 0
    while True:
        count += 1
        event = tray.read(timeout=500)

        print(event)

        if event == 'Exit':
            break


        if event == "PipeDreams":
            config = UI_Compact.getConfig()
            UI_Compact.PipeDreams_UI(config)


        elif event in('UI', sg.EVENT_SYSTEM_TRAY_ICON_DOUBLE_CLICKED) and not window:
            count = 1
            tray.Update(filename=icon_path_1)
            config = UI_Compact.getConfig()
            window = UI_Compact.PipeDreams_UI(config)


        elif event == 'Hide' and window:
            count = 1
            tray.Update(filename=icon_path_1)
            window.close()
            window = None







        if window:
            event, values = window.read(timeout=1000)
            print(event, values)
            
            if event in (sg.WIN_CLOSED, 'Minimize\nTo Tray'):
                count = 1
                window.close()
                window = None
                continue

            if event == "Start":
                count = 1
                notification()






        # animates tray Icon, only 2 frames currently allowed
        count = animCount(count, tray)








    tray.close()

    if window:
        window.close()


main()