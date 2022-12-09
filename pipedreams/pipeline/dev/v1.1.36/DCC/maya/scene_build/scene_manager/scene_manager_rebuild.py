from PySide2 import (QtGui,
                    QtCore,
                    QtWidgets)



class Scene_Manager_UI(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Scene Manager")
        self.setMinimumSize(QtCore.QSize(1000, 400))

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
        layout_Global_Assets = QtWidgets.QVBoxLayout()
        layout_Top_Assets = QtWidgets.QHBoxLayout()
        layout_Shot_Assets = QtWidgets.QHBoxLayout()

        tab_1 = QtWidgets.QWidget()
        tab_1.setLayout(layout_Global_Assets)

        tab_2 = QtWidgets.QWidget()
        tab_2.setLayout(layout_Top_Assets)

        tab_3 = QtWidgets.QWidget()
        tab_3.setLayout(layout_Shot_Assets)

        Tab_group.addTab(tab_1, "Global_Assets")
        Tab_group.addTab(tab_2, "Top_Assets")
        Tab_group.addTab(tab_3, "Shot_Assets")

        # Center Tabs.
        self.setStyleSheet('''QTabWidget::tab-bar {alignment: center;}''')


# Populate Tabs:

        for cat in ["Char", "Veh", "Env"]:

            groupBox = QtWidgets.QGroupBox(cat)
            cat_layout = QtWidgets.QVBoxLayout()
            groupBox.setLayout(cat_layout)
            # groupBox.setCheckable(True)
            # Build buttons for single Asset

            for i in range(3):
                asset_layout = QtWidgets.QHBoxLayout()
                # groupBox.setLayout(asset_layout)

                Import_button = QtWidgets.QPushButton("Import")
                Refrence_button = QtWidgets.QPushButton("Refrence")
                Update_button = QtWidgets.QPushButton("Update")

                asset_layout.addWidget(Import_button)
                asset_layout.addWidget(Refrence_button)
                asset_layout.addWidget(Update_button)

                #cat_layout.addWidget(asset_layout)
                
                # cat_layout.addWidget(asset_layout)
            # layout_Global_Assets.addWidget(groupBox)
        # layout_Global_Assets.addWidget(QtWidgets.QPushButton("Button"))
            # layout_Global_Assets.addWidget(groupBox)
            # for i in range(5):
            #   layout_Global_Assets.addWidget(QtWidgets.QPushButton("Button" + str(i)))


# Master Layout:

        master_layout = QtWidgets.QVBoxLayout()
        master_layout.addLayout(topLayout)
        master_layout.addWidget(Tab_group)
        self.setLayout(master_layout)

# StyleSheet:
        # self.setStyleSheet('background-color: grey;')
        # Refresh_button.setStyleSheet('background-color: grey;'
        #                           'border-style: outset;'
        #                           'border-width: 2px;'
        #                           'border-radius: 10px;'
        #                           'border-color: beige;'
        #                           'font: bold 14px;'
        #                           'min-width: 10em;'
        #                           'padding: 6px;'
        #                           )

app = QtWidgets.QApplication()
Scene_Manager_UI = Scene_Manager_UI()
Scene_Manager_UI.show()
app.exec_()