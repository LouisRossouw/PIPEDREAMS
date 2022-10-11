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

        cmds.optionMenu()
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




    def populate_optionMenu(self, *args):
        """ Simply populates the optionMenu. """
        items = ["anim", "previs", "rigging", "modelling", "lighting", "rendering"]
        for i in items:
            cmds.menuItem(i)




    def get_name_for_untitled(self, *args):
        """ generates a scene file name for an unsaved scene. project/shot default name. """
        name = os.environ["SHOT"]
        format_name = name + "_anim_" + "v01_001"
        return format_name




    def get_name_for_existing(self, *args):
        """ If scene is already saved, return its name. """
        file_name = os.path.basename(self.scene_name).split('.')[0]
        return file_name




    def get_scene_name(self, *args):
        """ Returns the name of the scene. """

        self.scene_name = cmds.file(q=True, sn=True)

        # check if this is a existing scene or an new untitle scene.
        if bool(self.scene_name) == False:
            file_name = self.get_name_for_untitled(self)

        elif bool(self.scene_name) == True:
            file_name = self.get_name_for_existing(self)

        return file_name




    def startup_update_save_field(self, *args):
        """ adds the existing scene file name to the UI text field. """
        cmds.textField(self.save_name_field, edit=True, text=self.get_scene_name(self))




    def query_save_field(self, *args):
        """ evaluates the save field. """
        save_field = cmds.textField(self.save_name_field, query=True, text=True)
        return save_field



    def query_split_field(self, *args):
        """ splits the text up into pieces to make it changeable. """
        text = self.query_save_field(self)
        split_text = text.split('_')
        split_text.reverse()
        return split_text



    def button_incremental_down(self, *args):
        """ version up. """
        split_text = self.query_split_field(self, *args)
        version_number = split_text[1]
        incremental_number = split_text[0]
        new_incremental_number = str((int(incremental_number) - 1)).zfill(3)

        self.updated_text = version_number + "_" + new_incremental_number

        self.rebuild_save(self)




    def button_incremental_up(self, *args):
        """ version up. """
        split_text = self.query_split_field(self, *args)
        version_number = split_text[1]
        incremental_number = split_text[0]
        new_incremental_number = str((int(incremental_number) + 1)).zfill(3)

        self.updated_text = version_number + "_" + new_incremental_number

        self.rebuild_save(self)




    def button_version_up(self, *args):
        """ version up. """
        split_text = self.query_split_field(self, *args)
        version_number = split_text[1][1:] # Remove the V from the number
        new_version_number = str((int(version_number) + 1)).zfill(2)
        self.updated_text = "v" + new_version_number + "_" + split_text[0]

        self.rebuild_save(self)




    def button_version_down(self, *args):
        """ version up. """
        split_text = self.query_split_field(self, *args)
        version_number = split_text[1][1:] # Remove the V from the number
        new_version_number = str((int(version_number) - 1)).zfill(2)
        self.updated_text = "v" + new_version_number + "_" + split_text[0]

        self.rebuild_save(self)




    def rebuild_save(self, split_text):
        """ Rebuilds the new save name """

        text = cmds.textField(self.save_name_field, query=True, text=True)
        updated_text = self.updated_text
        updated_save_name = text[:-len(updated_text)] + updated_text

        cmds.textField(self.save_name_field, edit=True, text=updated_save_name)






if __name__ == "__main__":
    
    run = Save_as()