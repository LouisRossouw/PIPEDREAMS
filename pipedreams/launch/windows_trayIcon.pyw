from infi.systray import SysTrayIcon
import os
import time
# from subprocess import *

# Icons
# Main
path_to_icon = "D:\\work\\projects\\dev\\projects\\PIPEDREAMS\\pipedreams\\pipeline\\resources\\logo\\pixl.ico"

Pipedreams_UI_icon = "D:\\work\\projects\\dev\\projects\\PIPEDREAMS\\pipedreams\\pipeline\\resources\\windows_tray_icons\\rocket.ico"
Pipedreams_CMD_icon = "D:\\work\\projects\\dev\\projects\\PIPEDREAMS\\pipedreams\\pipeline\\resources\\windows_tray_icons\\kat.ico"
sub_icon = "D:\\work\\projects\\dev\\projects\\PIPEDREAMS\\pipedreams\\pipeline\\resources\\windows_tray_icons\\fox.ico"

hover_text = "PipeDreams"

def Pipedreams_UI(sysTrayIcon):
    os.system("aa")

def Pipedreams_cmd(sysTrayIcon):
    os.system("xx")

def about(sysTrayIcon):
    os.system("start \"\" https://louisrossouw.com")

def bye(sysTrayIcon):
    print ('Bye, then.')

def do_nothing(sysTrayIcon):
    sysTrayIcon.update(hover_text="item")
    frame_2 = "D:\\work\\projects\\dev\\projects\\PIPEDREAMS\\pipedreams\\pipeline\\resources\\windows_tray_icons\\rocket.ico"
    sysTrayIcon.update(icon=frame_2)


menu_options = (('UI', Pipedreams_UI_icon, Pipedreams_UI),
                ('cmd', Pipedreams_CMD_icon, Pipedreams_cmd),
                ('About', sub_icon, about),

                ('A sub-menu', "submenu.ico", (('Say Hello to Simon', sub_icon, do_nothing),
                                               ('Do nothing', None, do_nothing),
                                              ))
               )
sysTrayIcon = SysTrayIcon(path_to_icon, hover_text, menu_options, on_quit=bye, default_menu_index=0)

sysTrayIcon.start()


while True:
    time.sleep(0.5)
    frame_1 = "D:\\work\\projects\\dev\\projects\\PIPEDREAMS\\pipedreams\\pipeline\\resources\\windows_tray_icons\\main\\ico\\pixli_1.ico"
    sysTrayIcon.update(icon=frame_1)

    time.sleep(0.5)

    frame_2 = "D:\\work\\projects\\dev\\projects\\PIPEDREAMS\\pipedreams\\pipeline\\resources\\windows_tray_icons\\main\\ico\\pixli_2.ico"
    sysTrayIcon.update(icon=frame_2)
   





