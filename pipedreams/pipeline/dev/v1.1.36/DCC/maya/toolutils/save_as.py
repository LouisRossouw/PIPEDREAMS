import os
import maya.cmds as cmds


class Save_as(object):
    """ Main Class to run the save as function. """

    def __init__(self):
        """ Initialize save UI """


        self.window_title = "Quick Save"
        self.size = (500, 25)

        self.create_window()


    def create_window(self):
        """ initialize the window UI. """

        # Remove window if it exists.
        if cmds.window(self.window_title, exists=True):
            cmds.deleteUI(self.window_title, window=True)

        # Create window
        window = cmds.window(title=self.window_title, widthHeight=self.size)

        cmds.rowColumnLayout(numberOfRows=1)

        self.optionMenu_task = cmds.optionMenu(changeCommand=self.updateTask)
        self.populate_optionMenu(self)

        cmds.setParent('..')

        cmds.columnLayout(adjustableColumn=True)
        cmds.rowColumnLayout(numberOfRows=1)

        # Window contents
        self.save_name_field = cmds.textField(width=250)
        self.version_up = cmds.button(label="^", command=self.button_version_up)
        self.verion_down = cmds.button("v", command=self.button_version_down)
        cmds.text("||", width=20)
        self.incremental_up = cmds.button(label="^", command=self.button_incremental_up)
        self.incremental_down = cmds.button(label="v", command=self.button_incremental_down)
        self.save_button = cmds.button(label="Save As")

        cmds.setParent('..')

        self.startup_update_save_field(self)

        cmds.showWindow(window)




    def updateTask(self, *args):
        """ update task on optionMenu change. """

        split_text = self.query_split_field(self)
        task_name = cmds.optionMenu(self.optionMenu_task, query=True, value=True)

        self.update_save_field(split_text[2], task_name)




    def populate_optionMenu(self, *args):
        """ Simply populates the optionMenu. """

        items = ["anim", "previs", "rigging", "modelling", "lighting", "rendering"]
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








if __name__ == "__main__":
    
    run = Save_as()