import os
import sys
import yaml
import maya.cmds as cmds
from pathlib import Path

PipeDreams_root_path = os.getenv('PIPELINE_ROOT')
sys.path.append(PipeDreams_root_path)

import scene_build.savesave as SV
import toolutils.other as other
import toolutils.ChopChop as ChopChop
import toolutils.QuickAnimSkin as QuickAnimSkin
import toolutils.RandomHide as RandomHide

import toolutils.StudioLib as StudioLib
import scene_build.capture_manager.capture_UI as cap_UI
import scene_build.export_manager.export_Manager_UI as export_UI
import scene_build.scene_manager.scene_manager_UI as scn_manager_UI



class ToolBar():
    """ Builds a toolbar for Maya. """


    def __init__(self):
        """ Initialize the PipeDream Toolbar. """

        self.config = self.return_config()
        menu_label = self.config["Pipeline_name"]

        self.window_title = "Quick Save"
        self.size = (500, 25)
        self.bg_MENUBAR = (0.14, 0.14, 0.14)
        self.TB_LOGO = self.return_logo_path()

        core_tools_items = [menu_label, "---" * 6, "Scene Manager", "Export Manager", "Capture Manager", "---" * 6, "Studio Library"]
        community_tools_items = ["Community Tools", "---" * 6, "Camera Rig", "RandomHide", "QuickAnimSkin", "ChopChop"]


        # Create window
        self.window = cmds.window(title=self.window_title, widthHeight=self.size, menuBar=True)
        self.buttonForm = cmds.rowColumnLayout(numberOfRows=1, parent=self.window)
        cmds.separator(hr=True)
        cmds.columnLayout(adjustableColumn=True)
        cmds.rowColumnLayout(numberOfRows=1)


        # Window contents
        cmds.image(image=self.TB_LOGO)
        # cmds.text(" " * 5 + menu_label, align='center' , highlightColor=(0.65, 1, 0), font="boldLabelFont")
        cmds.text(" " * 2)
        cmds.separator(hr=False, width=16)
        cmds.text(" " * 2)

        self.CORE_TOOLS = cmds.optionMenu(bgc=self.bg_MENUBAR, changeCommand=self.core_tool_select)
        self.fill_optionMenu(core_tools_items)

        self.COMMUNITY_TOOLS = cmds.optionMenu(bgc=self.bg_MENUBAR, changeCommand=self.community_tool_select)
        self.fill_optionMenu(community_tools_items)


        # add quicksave to the toolbar
        SV.SaveSave()

        cmds.separator(hr=False, width=100)
        cmds.text(os.getenv('PROJECT_NAME'))
        cmds.separator(hr=False, width=100)

        self.allowedAreas = ['top', 'bottom', 'left', 'right']
        self.bar = cmds.toolBar(area='top',
                                content=self.window,
                                allowedArea=self.allowedAreas,
                                bgc=self.bg_MENUBAR, numberOfPopupMenus=1, annotation="hello"
                                )




    def return_logo_path(self):
        """ returns the logo to be used for the ToolBar. """

        pipedreams = Path(os.getenv('PIPELINE_ROOT')).parents[2]
        logo_dir = str(pipedreams) + "/pipeline/resources/logo/pxl_3.png"

        return logo_dir




    def core_tool_select(self, *args):
        """ Launches the selected item from the core tool optionMneu. """

        clicked_button = args[0]

        if clicked_button == "Scene Manager":
            scn_manager_UI.Scene_Manager_UI()

        if clicked_button == "Export Manager":
            export_UI.Export_Manager()

        if clicked_button == "Capture Manager":
            cap_UI.capture_UI()

        if clicked_button == "Studio Library":
            StudioLib.launchStudioLib()

        cmds.optionMenu(self.CORE_TOOLS, edit=True, select=1, )




    def community_tool_select(self, *args):
        """ Launches the selected item from the community tool optionMneu. """

        clicked_button = args[0]

        if clicked_button == "Camera Rig":
            other.camera_build()

        if clicked_button == "RandomHide":
            RandomHide.build_ui()

        if clicked_button == "QuickAnimSkin":
            QuickAnimSkin.QuickAnim_Skin_UI()

        if clicked_button == "ChopChop":
            ChopChop.ChopChop_UI()

        cmds.optionMenu(self.COMMUNITY_TOOLS, edit=True, select=1,)




    def fill_optionMenu(self, items):
        """ adds items to optionMenu. """

        for i in items:
            cmds.menuItem(i)
        cmds.separator(hr=False)




    def return_config(self):
        """ Return the Pipeline config. """

        main_path = Path(os.getenv('PIPELINE_ROOT')).parents[2]
        config_path = (f"{main_path}/admin/pipeline_config.yaml")
        file_data = yaml.safe_load(open(config_path, 'r'))

        return file_data




if __name__ == "__main__":

    ToolBar()