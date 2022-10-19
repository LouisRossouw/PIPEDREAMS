import os
import maya.cmds as cmds



class SaveSave():
    """ an effecient way to save scene files using pipedreams file structure. """


    def __init__(self):


        self.window_title = "Quick Save"
        self.size = (500, 25)

        # Colors
        self.bg_TXTFIELD = (0.13, 0.13, 0.13)
        self.bg_SIMPLE_BUTTONS = (0.1, 0.1, 0.1)
        self.bg_GREEN = (0, 1, 0.7)
        self.bg_MENUBAR = (0.14, 0.14, 0.14)

        core_tool_items = ["anim", "previs", "rigging", "modelling", "lighting", "rendering"]


        self.save_name_field = cmds.textField(width=200, bgc=self.bg_TXTFIELD)

        self.optionMenu_task = cmds.optionMenu(changeCommand=self.updateTask, width=80)
        self.populate_optionMenu(core_tool_items)

        self.version_up = cmds.button(label="^", bgc=self.bg_SIMPLE_BUTTONS, command=self.button_version_up, width=40)
        self.verion_down = cmds.button("v", bgc=self.bg_SIMPLE_BUTTONS,command=self.button_version_down, width=40)
        cmds.separator(hr=False, width=16)
        self.incremental_up = cmds.button(label="^", bgc=self.bg_SIMPLE_BUTTONS, command=self.button_incremental_up, width=40)
        self.incremental_down = cmds.button(label="v", bgc=self.bg_SIMPLE_BUTTONS, command=self.button_incremental_down, width=40)
        cmds.button(label="ma", bgc=self.bg_GREEN, width=35, command=self.save_button_MA)
        cmds.button(label="mb", bgc=self.bg_GREEN, width=35, command=self.save_button_MB)
        cmds.button(label="^^", bgc=self.bg_GREEN, width=35, command=self.save_increment)
        cmds.separator(hr=True)

        self.startup_update_save_field(self)
        self.add_scriptJob()




    def save_increment(self, *args):
        """ quick version up and save file. """

        try:
            # If the scene is "Untitled" and has not been saved, then we can not get index 2, so pass
            file_name = os.path.basename(self.scene_name).split('.')[1]
            self.button_incremental_up()

            if file_name == "mb":
                self.save_button_MB(self)
            elif file_name == "ma":
                self.save_button_MA(self)

        except IndexError:
            pass




    def save_button_MA(self, *args):
        """ Executes when button is pushed. """

        scene_name = os.path.dirname(cmds.file(q=True, sn=True))
        save_name = cmds.textField(self.save_name_field, query=True, text=True)
        cmds.file(rename=scene_name + "/" + save_name + '.ma')
        cmds.file(save=True, type='mayaAscii')




    def save_button_MB(self, *args):
        """ Executes when button is pushed. """

        scene_name = os.path.dirname(cmds.file(q=True, sn=True))
        save_name = cmds.textField(self.save_name_field, query=True, text=True)
        cmds.file(rename=scene_name + "/" + save_name + '.mb')
        cmds.file(save=True, type='mayaBinary')




    def scriptJob_update_save(self, *args):
        """ executes the from the script job. """
        cmds.textField(self.save_name_field, edit=True, text=self.get_scene_name(self))



    def add_scriptJob(self, *args):
        """ adds a scriptJob to update the save text field when maya scene file changed. """
        # create a job that deletes things when they are seleted
        jobNum = cmds.scriptJob(event=["SceneOpened", self.scriptJob_update_save], protected=True)




    def updateTask(self, *args):
        """ update task on optionMenu change. """

        split_text = self.query_split_field(self)
        task_name = cmds.optionMenu(self.optionMenu_task, query=True, value=True)

        self.update_save_field(split_text[2], task_name)




    def populate_optionMenu(self, items):
        """ Simply populates the optionMenu. """

        for item in items:
            cmds.menuItem(item)




    def get_name_for_untitled(self, *args):
        """ generates a scene file name for an unsaved scene. project/shot default name. """

        name = os.environ["SHOT"]
        format_name = name + "_task_" + "v01_001"

        return format_name




    def get_scene_name(self, *args):
        """ Returns the name of the scene. """

        self.scene_name = cmds.file(q=True, sn=True)

        # check if this is a existing scene or an new untitle scene.
        if bool(self.scene_name) == False:
            file_name = self.get_name_for_untitled(self)

        elif bool(self.scene_name) == True:
            file_name = os.path.basename(self.scene_name).split('.')[0]

        return file_name




    def startup_update_save_field(self, *args):
        """ adds the existing scene file name to the UI text field. """

        cmds.textField(self.save_name_field, edit=True, text=self.get_scene_name(self))




    def query_split_field(self, *args):
        """ splits the text up into pieces to make it changeable. """

        text = cmds.textField(self.save_name_field, query=True, text=True)
        split_text = text.split('_')
        split_text.reverse()

        return split_text




    def update_save_field(self, replace_text, with_new_text):
        """ Replaces the old text with the new text in the save fieild. """

        replace_text = str(cmds.textField(self.save_name_field, query=True, text=True)).replace(replace_text, with_new_text)
        cmds.textField(self.save_name_field, edit=True, text=replace_text)




    def button_incremental_down(self, *args):
        """ version down. """

        split_text = self.query_split_field(self, *args)
        new_incremental_number = str((int(split_text[0]) - 1)).zfill(3)

        self.update_save_field(split_text[0], new_incremental_number)




    def button_incremental_up(self, *args):
        """ version up. """

        split_text = self.query_split_field(self, *args)
        new_incremental_number = str((int(split_text[0]) + 1)).zfill(3)

        self.update_save_field(split_text[0], new_incremental_number)




    def button_version_up(self, *args):
        """ version up. """

        split_text = self.query_split_field(self)
        new_version_number = "v" + str((int(split_text[1][1:]) + 1)).zfill(2) # + Update number

        self.update_save_field(split_text[1], new_version_number)




    def button_version_down(self, *args):
        """ version down. """

        split_text = self.query_split_field(self)
        new_version_number = "v" + str((int(split_text[1][1:]) - 1)).zfill(2) # - Update number

        self.update_save_field(split_text[1], new_version_number)
