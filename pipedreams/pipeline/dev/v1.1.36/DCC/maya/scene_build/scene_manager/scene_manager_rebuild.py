import os
from PySide2 import (QtGui,
                    QtCore,
                    QtWidgets)



class Scene_Manager_UI(QtWidgets.QWidget):


    def __init__(self):
        super().__init__()

        self.setWindowTitle("Scene Manager")
        self.setMinimumSize(QtCore.QSize(1500, 400))

    # Top Layout:

        topLayout = QtWidgets.QVBoxLayout()
        label = QtWidgets.QLabel()
        font = QtGui.QFont()
        Refresh_button = QtWidgets.QPushButton(text="Refresh")

        font.setBold(True)
        label.setFont(font)
        label.setText("Go_Testify_rigging_010")
        label.setAlignment(QtCore.Qt.AlignHCenter)
        topLayout.addWidget(label)
        topLayout.addWidget(Refresh_button)

        self.line = QtWidgets.QFrame()
        self.line.setGeometry(QtCore.QRect(0, 0, 0, 0))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        topLayout.addWidget(self.line)


    # Tabs Layout:

        Tab_group = QtWidgets.QTabWidget()
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
        self.setStyleSheet('''QTabWidget::tab-bar {alignment: center;}''')


    # Populate Tabs:

        # category = self.return_existing_categories()

        TABS = ["TOP", "SHOT"]

        for tab in TABS:

            category = self.return_existing_categories(tab)

            for cat in category[0]:

                self.groupBox = QtWidgets.QGroupBox(cat)

                self.groupBox.setCheckable(True)

                self.v_layout = QtWidgets.QVBoxLayout()
                self.groupBox.setLayout(self.v_layout)

                # Populate specific category with all existing assets.
                self.populate_assets(cat, category[1])

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

        # StyleSheet:

        self.setStyleSheet('background-color: grey;')
        Refresh_button.setStyleSheet('background-color: grey;'
                'border-style: outset;'
                'border-width: 2px;'
                'border-radius: 10px;'
                'border-color: black;'
                'font: bold 14px;'
                'min-width: 10em;'
                'padding: 6px;'
                )


    def populate_assets(self, category, path):
        """ Populates all assets for specific category. """

        category_path = path + '/' + category
        category_dir = os.listdir(category_path)

        # Build buttons for single Asset
        for i in category_dir:

            self.asset_layout = QtWidgets.QHBoxLayout()

            asset_Label = QtWidgets.QLabel(i)
            asset_Label.setAlignment(QtCore.Qt.AlignHCenter)
            asset_type = QtWidgets.QComboBox()
            asset_version = QtWidgets.QComboBox()
            asset_format = QtWidgets.QComboBox()

            Import_button = QtWidgets.QPushButton("Import")
            Refrence_button = QtWidgets.QPushButton("Refrence")
            Update_button = QtWidgets.QPushButton("Update")

            asset_user = QtWidgets.QLabel("Louis")
            asset_user.setAlignment(QtCore.Qt.AlignHCenter)

            self.asset_layout.addWidget(asset_Label)
            self.asset_layout.addWidget(asset_type)
            self.asset_layout.addWidget(asset_version)
            self.asset_layout.addWidget(asset_format)

            self.asset_layout.addWidget(Import_button)
            self.asset_layout.addWidget(Refrence_button)
            self.asset_layout.addWidget(Update_button)

            self.asset_layout.addWidget(asset_user)

            self.line = QtWidgets.QFrame()
            self.line.setFrameShape(QtWidgets.QFrame.HLine)
            self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
            self.v_layout.addWidget(self.line)

            # add data to the comboBox / optionMenus
            asset_data = self.return_assets(category_path + "/" + i)

            asset_type.addItems(asset_data[0])
            asset_version.addItems(asset_data[1])
            asset_format.addItems(asset_data[2])

            # add to layout.
            self.v_layout.addLayout(self.asset_layout)



    def return_existing_categories(self, tab):
        """ Returns the existing ca """

        asset_tab = tab + "_ASSETS"

        existing_ASSETS_path = os.getenv(asset_tab)
        existing_categories = os.listdir(existing_ASSETS_path)

        return existing_categories, existing_ASSETS_path


    def return_assets(path, asset_path):
        """ Returns the list of assets for the specific category. """

        asset_types = os.listdir(asset_path)
        versions = os.listdir(asset_path + "/" + asset_types[0])
        files_formats = os.listdir(asset_path + "/" + asset_types[0] + "/" + versions[0])

        formats = []
        for f in files_formats:
            format = f.split(".")[1]
            formats.append(format)

        return asset_types, reversed(versions), formats









#app = QtWidgets.QApplication()
Scene_Manager_UI = Scene_Manager_UI()
Scene_Manager_UI.show()
#app.exec_()