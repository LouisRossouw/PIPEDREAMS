import os
import maya.cmds as cmds

from functools import partial


def Scene_Manager_UI():
    """ Launches the Scene Manager """


    def clearOptionMenu(optionMneu_path):
        """ pass the optionmenu and it will clear all the items """

        # loop through existing menus in the optionMenu and destroy them
        for item in cmds.optionMenu(optionMneu_path, q=True, ill=True) or []:
            cmds.deleteUI(item)



    def importAsset(*args):
        """ function to import an asset """

        button_pushed = cmds.button(args[0], query=True, label=True)

        # check version number
        asset_name = UI_data[args[0]]["asset_name"]
        asset_base_path = UI_data[args[0]]["asset_path"]
        catagory = UI_data[args[0]]["catagory"]
        extension = UI_data[args[0]]["extension"]

        versions_path = args[1]
        asset_type_path = args[2]

        asset_type = cmds.optionMenu(asset_type_path, query=True, value=True)
        current_version = cmds.optionMenu(versions_path, query=True, value=True)
        extension_type = cmds.optionMenu(extension, query=True, value=True)

        path_to_assets_dir = asset_base_path + "/" + asset_type + "/" + current_version
        asset_path = path_to_assets_dir + "/" + asset_name + "_" + asset_type + "_" + current_version
        full_asset_path = asset_path + "." + extension_type

        # check if file exists
        exists = cmds.file(full_asset_path, query=True, exists=True)

        if exists == False:
            cmds.confirmDialog(title="Cant find file", message=asset_name + " Does not exist")
        else:
            # import / reference action
            print("Importing: ", full_asset_path)
            if button_pushed == "Import":
                cmds.file(full_asset_path, i=True)
            elif button_pushed == "Reference":
                cmds.file(full_asset_path, r=True, namespace=catagory)



    def UpdateVersions(*args):
        """ updates the versions UI for rigs or geo """

        button_type = args[0]
        button_name = args[1]

        versions_button_path = UI_data[button_type]["version_button"]
        asset_button_path = UI_data[button_type]["asset_path"]
        extensions_button = UI_data[button_type]["extensions"]

        current_version = cmds.optionMenu(versions_button_path, query=True, value=True)
        selected_Asset_path = asset_button_path + "/" + button_name

        # Clear optiopn menu
        clearOptionMenu(versions_button_path)

        asset_version_count = os.listdir(selected_Asset_path)

        for i in asset_version_count:

            # changes the version option menu to whatever
            cmds.menuItem(label=i, parent=versions_button_path)

        latet_version = asset_version_count[-1]

        # changes the version option menu to whatever
        cmds.optionMenu(versions_button_path, edit=True, value=latet_version)

        # update extensions in optionMenu
# ###
        list_assets = os.listdir(selected_Asset_path + "/" + latet_version)
        clearOptionMenu(extensions_button)
        for asset in list_assets:
            extention = asset.split(".")[1]
            if extention != "mtl":
                cmds.menuItem(label=extention, parent=extensions_button)



    def updateExtensions(*args):
        """ updates the extensions option menu """

        asset_path = args[1]
        asset_type = args[2]
        version = args[4]
        extensions_button = args[3]

        type = cmds.optionMenu(asset_type, query=True, value=True)
        selected_version_path = asset_path + "/" + type + "/" + version

        list_assets = os.listdir(selected_version_path)

        clearOptionMenu(extensions_button)
        for asset in list_assets:
            extention = asset.split(".")[1]
            if extention != "mtl":
                cmds.menuItem(label=extention, parent=extensions_button)



    def buildUI_Catagories(UI_data, catagory, TAB):
        """ builds the UI catagories / char / env / prop / veh """

        cmds.columnLayout(adjustableColumn=True)
        cmds.frameLayout(label=catagory, cll=False, cl=True, mh=10)
        cmds.rowColumnLayout(numberOfColumns=10, columnAttach=(1, 'left', 0), columnWidth=[(10, 100), (2, 250)])

        if TAB == "TOP_ASSETS":
            # gets the list of items for this specific asset type
            populate_Asset_TABS(UI_data, catagory, TAB)
            cmds.setParent(top_assets_row)
        elif TAB == "SHOT_ASSETS":
            populate_Asset_TABS(UI_data, catagory, TAB)
            cmds.setParent(shot_assets_row)



    def populate_Asset_TABS(UI_data, catagory, TAB):
        """ Populates the TOP / SHOT tabs with existing assets from the current project """

        if TAB == "TOP_ASSETS":
            TOP_ASSETS = os.getenv("TOP_ASSETS")
            catagory_path = (TOP_ASSETS + "/" + catagory)
        elif TAB == "SHOT_ASSETS":
            SHOT_ASSETS = os.getenv("SHOT_ASSETS")
            catagory_path = (SHOT_ASSETS + "/" + catagory)

        try:
            for asset in os.listdir(catagory_path):

                asset_path = catagory_path + "/" + asset

                cmds.text(label="-")
                cmds.text(label=asset + "_" + catagory)

                type_button = cmds.optionMenu(label="type: ", changeCommand=UpdateVersions)
                cmds.optionMenu(type_button, e=True, changeCommand=partial(UpdateVersions, type_button))

                for type in os.listdir(asset_path):
                    cmds.menuItem(label=type)

                cmds.text(label="  ")

    # version numbers to the versions UI
                versions = cmds.optionMenu(label="Version: ", changeCommand=updateExtensions)
                cmds.separator(style='in', hr=False)

                asset_type_menu = cmds.optionMenu(type_button, query=True, value=True)

                asset_type = asset_path + "/" + asset_type_menu

                asset_version_count = os.listdir(asset_type)
                latest_asset_version = asset_version_count[-1]

                for i in asset_version_count:
                    cmds.menuItem(label=i)

                cmds.optionMenu(versions, edit=True, value=latest_asset_version)
                version = cmds.optionMenu(versions, query=True, value=True)

    # Extensions optionMenu
                full_asset_version_path = asset_type + "/" + version
                extensions_button = cmds.optionMenu(label=" |")
                for ext in os.listdir(full_asset_version_path):
                    cmds.menuItem(ext.split(".")[1])

                cmds.text(label=" | ")

    # Import Button
                impport_button = cmds.button(label="Import", bgc=(0.65, 1, 0))
                UI_data[impport_button] = {"asset_name":asset, "asset_path":asset_path, "catagory":catagory, "extension":extensions_button}
                cmds.button(impport_button, e=True, c=partial(importAsset, impport_button, versions, type_button))

    # Refrence Button
                refrence_button = cmds.button(label="Reference", bgc=(0.65, 1, 0))
                UI_data[refrence_button] = {"asset_name":asset, "asset_path":asset_path, "catagory":catagory, "extension":extensions_button}
                cmds.button(refrence_button, e=True, c=partial(importAsset, refrence_button, versions, type_button))

                UI_data[type_button] = {"asset": asset, "version_button": versions, "asset_path" : asset_path, "extensions":extensions_button}

                cmds.optionMenu(versions, e=True, changeCommand=partial(updateExtensions, versions, asset_path, type_button, extensions_button))

        except Exception as e:
            print(e)
            cmds.confirmDialog(title='Error populating Scene Manager', message='Error: ' + str(e))



### MAIN UI

    project_name = os.getenv('PROJECT_NAME')
    window_title = 'Scene_Manager || ' + str(project_name)

    Title = "PipeDreams"

    # all UI button paths etc go into this dictionary.
    UI_data = {}

    if cmds.window(window_title, exists=True):
        cmds.deleteUI(window_title)

    cmds.window(title=window_title, widthHeight=(750, 450), menuBar=True)

    cmds.menu(label=Title)
    cmds.menuItem(subMenu=True, label='test1')
    cmds.menuItem(label='test2')

    cmds.setParent('..', menu=True)

    cmds.menuItem(divider=True)

    cmds.radioMenuItemCollection()
    cmds.menuItem(label='Yes', radioButton=False)
    cmds.menuItem(label='Maybe', radioButton=False)
    cmds.menuItem(label='No', radioButton=True)
    cmds.menuItem(divider=True)
    cmds.menuItem(label='Top', checkBox=True)
    cmds.menuItem(label='Middle', checkBox=False)
    cmds.menuItem(label='Bottom', checkBox=True)
    cmds.menuItem(divider=True)
    cmds.menuItem(label='Option')
    cmds.menuItem(optionBox=True)

    # Importer Dropdown
    cmds.columnLayout(adjustableColumn=True)
    cmds.frameLayout(label='importer', cll=True, mh=10, )
    cmds.rowColumnLayout(numberOfColumns=2, columnAttach=(1, 'right', 0), columnWidth=[(10, 100), (2, 250)])

    cmds.button(label="Refresh")
    cmds.setParent('..')

    # Tab Setup
    form = cmds.formLayout()
    tabs = cmds.tabLayout(innerMarginWidth=20, innerMarginHeight=20)
    cmds.formLayout(form, edit=True,
                    attachForm=((tabs, 'top', 0), (tabs, 'left', 10), (tabs, 'bottom', 0), (tabs, 'right', 0)))



    ##                      Tab 1                       ###

    #   main
    main = cmds.rowColumnLayout(numberOfColumns=1, adjustableColumn=True)

    cmds.columnLayout(adjustableColumn=True)
    cmds.frameLayout(label='tmp', cll=True, cl=True, mh=10)
    cmds.rowColumnLayout(numberOfColumns=7, columnAttach=(1, 'right', 0), columnWidth=[(10, 100), (2, 250)])

    cmds.setParent(main)
    cmds.setParent('..')



    ##                      Tab 2                       ###

    #   TOP_ASSETS
    top_assets_row = cmds.rowColumnLayout(numberOfColumns=1, adjustableColumn=True)
    cmds.separator(height=20, style='in')
    cmds.text(label=project_name)
    cmds.separator(height=20, style='in')

    # loops through all the asset types dirs | char, env, veh, prop etc
    for cat in os.listdir(os.getenv("TOP_ASSETS")):
        buildUI_Catagories(UI_data, cat, "TOP_ASSETS")
        cmds.setParent(top_assets_row)

    cmds.setParent('..')



    ##                      Tab 3                       ###

    #   SHOT_ASSETS
    shot_assets_row = cmds.rowColumnLayout(numberOfColumns=1, adjustableColumn=True)
    cmds.text(label=project_name)

    cmds.columnLayout(adjustableColumn=True)
    cmds.rowColumnLayout(numberOfColumns=6)
    cmds.separator( height=10, style='in' )

    import_SRT_checkBox = cmds.checkBox(label="Import under Scene_SRT", value=True)
    test_1 = cmds.checkBox(label="Test", value=False)

    cmds.separator( height=10, style='in' )
    cmds.setParent(shot_assets_row)

    # loops through all the asset types dirs | char, env, veh, prop etc
    for cat in os.listdir(os.getenv("SHOT_ASSETS")):
        buildUI_Catagories(UI_data, cat, "SHOT_ASSETS")
        cmds.setParent(shot_assets_row)


    cmds.setParent('..')
    cmds.setParent(shot_assets_row)
    cmds.setParent(shot_assets_row)

    cmds.tabLayout(tabs, edit=True, tabLabel=((main, 'Main'), (shot_assets_row, 'Shot Assets'), (top_assets_row, "Top_Assets")))
    cmds.setParent(shot_assets_row)


    cmds.showWindow()



if __name__ == "__main__":
    Scene_Manager_UI()