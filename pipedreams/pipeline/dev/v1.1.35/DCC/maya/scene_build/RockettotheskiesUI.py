import yaml
from pathlib import Path

import pymel.core as pm

import toolutils.other as other
import toolutils.ChopChop as ChopChop
import toolutils.QuickAnimSkin as QuickAnimSkin
import toolutils.RandomHide as RandomHide
import toolutils.StudioLib as StudioLib

import scene_build.capture_manager.capture_UI_new as cap_UI
import scene_build.export_manager.export_Manager_UI as export_UI
import scene_build.scene_manager.scene_manager_UI as scn_manager_UI







def rocketothesky():
    """" Launches the Pipeline toolbar for Maya """

    main_path = Path(__file__).parents[6]
    config_path = (f"{main_path}/admin/pipeline_config.yaml")
    file_data = yaml.safe_load(open(config_path, 'r'))

    TOOLNAME = file_data["Pipeline_name"]

    main_window = pm.language.melGlobals['gMainWindow']
    
    menu_obj = 'MyCustomToolsMenu'
    menu_label = " - "+ TOOLNAME + " - "

    if pm.menu(menu_obj, label=menu_label, exists=True, parent=main_window):
        exit()
        # pm.deleteUI(menu_obj, deleteALLItems=True)

    custom_tools_menu = pm.menu(menu_obj, 
                                label=menu_label, 
                                parent=main_window, 
                                tearOff=True
                                )

    # Scene  Manager
    pm.menuItem(label='Scene Manager',
                subMenu=False, 
                parent=custom_tools_menu, 
                tearOff=True, 
                command=lambda x:scn_manager_UI.Scene_Manager_UI(),                
                )


    # Export
    pm.menuItem(label='Export_Manager',
                command=lambda x:export_UI.Export_Manager(),
                )
                

    # Capture
    pm.menuItem(label='Capture', 
                subMenu=False, 
                parent=custom_tools_menu, 
                tearOff=True, 
                command=lambda x:cap_UI.capture_UI(),
                )


    # Studio Library
    pm.menuItem(label='Studio Library', 
                subMenu=False, 
                parent=custom_tools_menu, 
                tearOff=True, 
                command=lambda x:StudioLib.launchStudioLib(),
                )



    # Tools
    tools = pm.menuItem(label='Tools', 
                        subMenu=True, 
                        parent=custom_tools_menu, 
                        tearOff=False, 
                        )


    pm.menuItem(label='Camera_rig', 
                subMenu=False, 
                parent=tools, 
                tearOff=False, 
                command=lambda x:other.camera_build(),
                )

    pm.menuItem(label='ChopChop',
                subMenu=False,
                parent=tools,
                tearOff=False,
                command=lambda x:ChopChop.ChopChop_UI(),
                )

    pm.menuItem(label='QuickAnimSkin',
                subMenu=False,
                parent=tools,
                tearOff=False,
                command=lambda x:QuickAnimSkin.QuickAnim_Skin_UI(),
                )

    pm.menuItem(label='RandomHide',
                subMenu=False,
                parent=tools,
                tearOff=False,
                command=lambda x:RandomHide.build_ui(),
                )





if __name__ == '__main__':
    test()
    # rocketothesky()