import os
from functools import partial
from PySide2 import (QtGui,
                    QtCore,
                    QtWidgets)

import scene_build.scene_manager.maya_SceneManager_utils as Maya_SM_utils



class Scene_Manager_UI(QtWidgets.QWidget):
    """ Builds the Scene Manager UI for the importing of assets. """

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Scene Manager")
        self.project_name = os.getenv('PROJECT_NAME')

        self.ignore_formats = ["mtl"]

    # Top Layout:

        topLayout = QtWidgets.QVBoxLayout()
        label = QtWidgets.QLabel()
        font = QtGui.QFont()
        # Refresh_button = QtWidgets.QPushButton(text="Refresh")

        font.setBold(True)
        label.setFont(font)
        label.setText(self.project_name)
        label.setAlignment(QtCore.Qt.AlignHCenter)
        topLayout.addWidget(label)
        # topLayout.addWidget(Refresh_button)

        self.line = QtWidgets.QFrame()
        self.line.setGeometry(QtCore.QRect(0, 0, 0, 0))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        topLayout.addWidget(self.line)


    # Tabs Layout:

        Tab_group = QtWidgets.QTabWidget()
        Tab_group.tabBarClicked.connect(self.tab_resize)

        self.layout_Global_Assets = QtWidgets.QVBoxLayout()
        self.layout_Top_Assets = QtWidgets.QVBoxLayout()
        self.layout_Shot_Assets = QtWidgets.QVBoxLayout()

        tab_1 = QtWidgets.QWidget()
        tab_1.setLayout(self.layout_Global_Assets)

        tab_2 = QtWidgets.QWidget()
        tab_2.setLayout(self.layout_Top_Assets)

        tab_3 = QtWidgets.QWidget()
        tab_3.setLayout(self.layout_Shot_Assets)

        Tab_group.addTab(tab_1, "Global_Assets")
        Tab_group.addTab(tab_2, "Top_Assets")
        Tab_group.addTab(tab_3, "Shot_Assets")

        # Center Tabs.
        self.setStyleSheet("""QTabWidget::tab-bar {alignment: center;}""")


    # Populate Tabs:

        TABS = ["TOP", "SHOT"]

        self.asset_dict = {}
        self.total_asset_count = {}

        for tab in TABS:

            total_asset_count = 0
            category = self.return_existing_categories(tab)

            for cat in category[0]:

                self.groupBox = QtWidgets.QGroupBox(cat)
                self.groupBox.setCheckable(True)

                self.v_layout = QtWidgets.QVBoxLayout()
                self.groupBox.setLayout(self.v_layout)

                # Populate specific category with all existing assets.
                row_count = self.populate_assets(cat, category[1], tab)

                # add total count of assets for the Tab.
                total_asset_count += row_count
                self.total_asset_count[tab] = total_asset_count

                if tab == "GLOBAL":
                    self.layout_Global_Assets.addWidget(self.groupBox)
                if tab == "TOP":
                    self.layout_Top_Assets.addWidget(self.groupBox)
                if tab == "SHOT":
                    self.layout_Shot_Assets.addWidget(self.groupBox)


    # Master Layout:

        master_layout = QtWidgets.QVBoxLayout()
        master_layout.addLayout(topLayout)
        master_layout.addWidget(Tab_group)
        self.setLayout(master_layout)




    def populate_assets(self, category, path, tab):
        """ Populates all assets for specific category. """

        category_path = path + '/' + category
        category_dir = os.listdir(category_path)

        # Build buttons for single Asset
        row_index = 0

        for i in category_dir:

            row_index += 1
            unique_name = tab + "_" + category + "_" + str(i) + "_" + str(row_index)

            self.asset_layout = QtWidgets.QHBoxLayout()

            self.asset_Label = QtWidgets.QLabel(i)
            self.asset_Label.setAlignment(QtCore.Qt.AlignHCenter)
            self.asset_type = QtWidgets.QComboBox()
            self.asset_version = QtWidgets.QComboBox()
            self.asset_format = QtWidgets.QComboBox()
            # self.name_space = QtWidgets.QCheckBox("NS", )

            self.Import_button = QtWidgets.QPushButton("Import", clicked=partial(self.button_import, unique_name))
            self.Refrence_button = QtWidgets.QPushButton("Refrence", clicked=partial(self.button_refrence, unique_name))
            self.Update_button = QtWidgets.QPushButton("Reload", clicked=partial(self.button_reload, unique_name))

            asset_user = QtWidgets.QLabel("Louis")
            asset_user.setAlignment(QtCore.Qt.AlignHCenter)

            self.asset_layout.addWidget(self.asset_Label)
            self.asset_layout.addWidget(self.asset_type)
            self.asset_layout.addWidget(self.asset_version)
            self.asset_layout.addWidget(self.asset_format)
            # self.asset_layout.addWidget(self.name_space)

            self.asset_layout.addWidget(self.Import_button)
            self.asset_layout.addWidget(self.Refrence_button)
            self.asset_layout.addWidget(self.Update_button)

            self.asset_layout.addWidget(asset_user)

            self.asset_dict[unique_name] = {"asset_name": i,
                                            "asset_label": self.asset_Label,
                                            "asset_type": self.asset_type,
                                            "asset_version": self.asset_version,
                                            "asset_format": self.asset_format,
                                            "asset_path": category_path,
                                            "category": category,
                                           }

            # Connect QcomboBoxs
            self.asset_type.activated.connect(partial(self.TYPE_comboBox_change, unique_name))
            self.asset_version.activated.connect(partial(self.FORMAT_comboBox_change, unique_name))

            # add data to the comboBox / optionMenus
            asset_data = self.return_assets(path, category_path + "/" + i)

            self.asset_type.addItems(asset_data[0])
            self.asset_version.addItems(asset_data[1])
            self.asset_format.addItems(asset_data[2])

            # Set Button StyleSheet.
            self.Import_button.setStyleSheet("""color: rgb(0,0,0);background-color: rgb(0, 255, 180);""")
            self.Refrence_button.setStyleSheet("""color: rgb(0,0,0);background-color: rgb(0, 255, 180);""")
            self.Update_button.setStyleSheet("""color: rgb(0,0,0);background-color: rgb(0, 255, 180);""")

            # add to layout.
            self.v_layout.addLayout(self.asset_layout)

        return row_index


    def tab_resize(self, tab_index):

        if tab_index == 0: # Globbal_Assets
            pass
        if tab_index == 1: # Top_Assets
            amount = self.total_asset_count["TOP"]
            y_Size = 150
            self.setFixedSize(QtCore.QSize(900, y_Size + (80 * amount)))

        if tab_index == 2:  # Shot_Assets
            amount = self.total_asset_count["SHOT"]
            y_Size = 150
            self.setMinimumSize(QtCore.QSize(900, y_Size + (50 * amount)))




    def check_file_exists(self, asset_path):
        """ Check if file exists. """

        print(asset_path)
        exists = os.path.exists(asset_path)

        if exists == False:
            self.popUp_message("File Not Found.", "Could not find the path to: \n\n" + str(asset_path))
            status = False

        elif exists == True:
            print(asset_path)
            status = True

        return status




    def execute_import(self, action, row_index):
        """ Executes the import function across DCCs. """

        selected_asset_data = self.return_selected_asset_path(row_index)

        asset_path = selected_asset_data[0]
        asset_type = selected_asset_data[2]
        catagory = selected_asset_data[5]
        asset_name = selected_asset_data[1]
        current_version = selected_asset_data[3]
        NameSpace = selected_asset_data[6]

        exists = self.check_file_exists(asset_path)

        if exists != False:

            DCC = os.getenv("DCC")

            if DCC == "Maya":
                Maya_SM_utils.SCM_import(action, asset_path,
                                           asset_type, catagory,
                                           asset_name, current_version, NameSpace)

            if DCC == "Houdini":
                pass

            if DCC == "Blender":
                pass




    def button_reload(self, row_index):
        """ Function for Reload button when clicked. """
        self.execute_import("Reload", row_index)




    def button_refrence(self, row_index):
        """ Function for refrence button when clicked. """
        self.execute_import("Reference", row_index)




    def button_import(self, row_index):
        """ Function for import button when clicked. """
        self.execute_import("Import", row_index)




    def popUp_message(self, title, message):
        """ PopUp message to use for errors etc. """

        dlg = QtWidgets.QMessageBox(self)
        dlg.setWindowTitle(title)
        dlg.setText(message)
        button = dlg.exec_()

        if button == QtWidgets.QMessageBox.Ok:
            pass




    def return_selected_asset_path(self, row_index):
        """ Function for import button when clicked. """

        dict = self.return_dict(row_index)

        asset_path = dict["asset_path"]
        asset_name = dict["asset_name"]
        asset_type = dict["asset_type"].currentText()
        asset_version = dict["asset_version"].currentText()
        asset_format = dict["asset_format"].currentText()
        category = dict["category"]
        NameSpace = dict["NameSpace"]

        file_name = asset_name + "_" + asset_type + "_" + asset_version + "." + asset_format
        path = asset_path + "/" + asset_name + "/" + asset_type + "/" + asset_version + "/" + file_name

        data = [path, asset_name, asset_type, asset_version, asset_format, category, NameSpace]

        return data




    def return_dict(self, row_index):
        """ Return an object from specific row in the UI. """

        # Returns asset info from row.
        asset_name = self.asset_dict[row_index]["asset_name"]
        asset_type = self.asset_dict[row_index]["asset_type"]
        asset_version = self.asset_dict[row_index]["asset_version"]
        asset_format = self.asset_dict[row_index]["asset_format"]
        asset_path = self.asset_dict[row_index]["asset_path"]
        category = self.asset_dict[row_index]["category"]
        NameSpace = False

        return {
                "asset_name":asset_name,
                "asset_type":asset_type,
                "asset_version":asset_version,
                "asset_format":asset_format,
                "asset_path":asset_path,
                "category": category,
                "NameSpace": NameSpace
                }




    def strip_extensions(self, return_formats):
        """ Strips the extension from the names. """

        ext_list = []

        for f in return_formats:
            ext = f.split(".")[1]

            if ext not in self.ignore_formats:
                ext_list.append(ext)

        return ext_list




    def return_asset(self, row_index, comboBox):
        """ Returns QcomboBox object from specific row, to query it. """

        return self.return_dict(row_index)[comboBox]




    def FORMAT_comboBox_change(self, row_index, type):
        """ ComboBox change function to update the versions and formats comboBox
            based on what is in the directories. """

        T_comboBox_obj = self.return_asset(row_index, "asset_type").currentText()
        V_comboBox_obj = self.return_asset(row_index, "asset_version").currentText()
        F_comboBox_obj = self.return_asset(row_index, "asset_format")

        asset_name = self.return_asset(row_index, "asset_name")
        asset_path = self.return_asset(row_index, "asset_path")

        path = asset_path + "/" + asset_name + "/" + T_comboBox_obj + "/" + V_comboBox_obj
        return_formats = os.listdir(path)
        ext_list = self.strip_extensions(return_formats)

        # Update versions comboBox
        F_comboBox_obj.clear()
        F_comboBox_obj.addItems(ext_list)




    def TYPE_comboBox_change(self, row_index, type):
        """ ComboBox change function to update the versions and formats comboBox
            based on what is in the directories. """

        T_comboBox_obj = self.return_asset(row_index, "asset_type").currentText()
        V_comboBox_obj = self.return_asset(row_index, "asset_version")

        asset_name = self.return_asset(row_index, "asset_name")
        asset_path = self.return_asset(row_index, "asset_path")

        path = asset_path + "/" + asset_name + "/" + T_comboBox_obj
        return_versions = os.listdir(path)

        # Update versions comboBox
        V_comboBox_obj.clear()
        V_comboBox_obj.addItems(reversed(return_versions))

        self.FORMAT_comboBox_change(row_index, type)




    def return_existing_categories(self, tab):
        """ Returns the existing ca """

        asset_tab = tab + "_ASSETS"

        existing_ASSETS_path = os.getenv(asset_tab)
        existing_categories = os.listdir(existing_ASSETS_path)

        return existing_categories, existing_ASSETS_path




    def return_assets(self, path, asset_path):
        """ Returns the list of assets for the specific category. """

        asset_types = os.listdir(asset_path)
        versions = os.listdir(asset_path + "/" + asset_types[0])

        files_formats = os.listdir(asset_path + "/" + asset_types[0] + "/" + versions[-1])
        formats = self.strip_extensions(files_formats)

        print(asset_path, files_formats)

        return asset_types, reversed(versions), formats




if __name__ == "__main__":

    #app = QtWidgets.QApplication()
    Scene_Manager_UI = Scene_Manager_UI()
    Scene_Manager_UI.show()
    #app.exec_()