import os
import json
import time
import random

import maya.cmds as cmds
from functools import partial


# local app/lib imports
import scene_build.export_manager.export as export
import scene_build.export_manager.export_utils as utils



def Export_Manager():
    """ Start the Export Manager UI. """


    def write_to_json(json_path, data):
        """ Create and write to json file """
        with open(json_path, 'w') as f:
            json.dump(data, f, indent=6)




    def read_json(json_path):
        """ Reads json file """
        with open(json_path) as f:
            json_file = json.loads(f.read())

        return (json_file)




### save export
    def SaveExport(*args):
        """ preps and saves the selected obj to a json data base and export list """

        sceneID = cmds.fileInfo('sceneID', q=True)[0]
        shot_data_dir = os.getenv("SHOT_DATA")
        export_data_dir = shot_data_dir + '\\export_data'
        export_list_json = export_data_dir + '\\export_scene_data_' + str(sceneID) + '.json'

        # Query UI
        asset_name = cmds.textField(txtField_ASSET_NAME, query=True, text=True)
        asset_category = cmds.optionMenu(opMenu_ASSET_CATEGORY, query=True, value=True)
        asset_type = cmds.optionMenu(opMenu_ASSET_TYPE, query=True, value=True)
        asset_destination = cmds.optionMenu(opMenu_ASSET_DESTINATION, query=True, value=True)
        export_path = cmds.textField(txtFielf_EXPORT_PATH, query=True, text=True)
        start_frame = cmds.intField(intField_START_RANGE, query=True, value=True)
        end_frame = cmds.intField(intField_END_RANGE, query=True, value=True)

        # get selection list
        selected_geo = cmds.ls(sl=True)

        data = read_json(export_list_json)

        if bool(selected_geo) != None:
            if bool(asset_name) != None:

                data[asset_name] = {
                                    "asset_name":asset_name,
                                    "asset_category":asset_category,
                                    "selected":selected_geo,
                                    "asset_type":asset_type,
                                    "asset_destination":asset_destination,
                                    "export_path":export_path,
                                    "start_frame":start_frame,
                                    "end_frame":end_frame,

                                    "user":os.environ['COMPUTERNAME'],
                                    "time":time.time(),
                                    }

                write_to_json(export_list_json, data)


        cmds.evalDeferred(Export_Manager)




    def addTag(asset_name, selected_geo):
        """ Adds an EXPORTME tag to the selected obj """
        for selected in selected_geo:
            attr_in_obj = cmds.listAttr(selected)
            for attr in attr_in_obj:
                exptMe = 'EXPORTME'
                # IF EXPORTME exists in obj node
                if attr.find(exptMe) != -1:
                    find = True
                else:
                    find = False

            if find != True:
                n = random.randint(1, 100000)
                exportMe = 'EXPORTME_' + str(n) + '_' + str(asset_name)
                cmds.addAttr(selected, longName=exportMe, attributeType='bool', k=True)
                cmds.setAttr(selected + '.' + exportMe, 1)
            else:
                pass




    def populateExportList(*args):
        """ gets all existing saved export data for this specific scene and adds it to the UI export list """

        UIdata = {}

        sceneID = cmds.fileInfo('sceneID', q=True)[0]
        shot_data_dir = os.getenv("SHOT_DATA")
        export_data_dir = shot_data_dir + '\\export_data'
        export_list_json = export_data_dir + '\\export_scene_data_' + str(sceneID) + '.json'

        data = read_json(export_list_json)

        count = 0
        for asset in data:

            count += 1

            asset_name = data[asset]["asset_name"]
            asset_category = data[asset]["asset_category"]
            asset_type = data[asset]["asset_type"]

            asset_destination = data[asset]["asset_destination"]
            export_path = data[asset]["export_path"]

            start_frame = data[asset]["start_frame"]
            end_frame = data[asset]["end_frame"]

            user = data[asset]["user"]
            time = data[asset]["time"]


            cat_list = ["char", "prop", "veh", "env", "cam"]
            types_list = ["anim", "rig", "geo", "lights", "fx"]
            dest_list = ["Top Assets", "Shot Assets"]

            unique_user = user + "_" + str(count)

            path = os.getenv(asset_destination.upper().replace(" ", "_"))
            path_category = (path + "/" + asset_category)
            path_type = (path_category + "/" + asset_name)
            asset_name_path = (path_type + "/" + asset_type)


    # data
            cmds.text(count, parent=UI_saved_asset_list, font="tinyBoldLabelFont")                                      # Count
            cmds.separator(style='in', hr=False, parent=UI_saved_asset_list)

            asset_checkbox = cmds.checkBox(asset_name, parent=UI_saved_asset_list)                                          # asset name ###### NEED TO MAKE SURE WHEN CHANGING VALUE IT
            cmds.separator(style='in', hr=False, parent=UI_saved_asset_list)                                            ### RECHECKS THE VERSION NUMBER

            type_menu = cmds.optionMenu(parent=UI_saved_asset_list, changeCommand=rowTypeChange)                        # type
            for ty in types_list:
                cmds.menuItem(ty)
            cmds.optionMenu(type_menu, edit=True, v=asset_type)
            cmds.separator(style='in', hr=False, parent=UI_saved_asset_list)

            cat_menu = cmds.optionMenu(parent=UI_saved_asset_list, changeCommand=rowTypeChange)                                                      # category
            for cat in cat_list:
                cmds.menuItem(cat)
            cmds.optionMenu(cat_menu, edit=True, v=asset_category)
            cmds.separator(style='in', hr=False, parent=UI_saved_asset_list)

            dest_menu = cmds.optionMenu(parent=UI_saved_asset_list, changeCommand=rowTypeChange)                                                     # destination
            for dest in dest_list:
                cmds.menuItem(dest)
            cmds.optionMenu(dest_menu, edit=True, v=asset_destination)
            cmds.separator(style='in', hr=False, parent=UI_saved_asset_list)

            start_intField = cmds.intField(value=start_frame, parent=UI_saved_asset_list, bgc=(0.3,0.3,0.3))            # start
            cmds.separator(style='in', hr=False, parent=UI_saved_asset_list)

            end_intField = cmds.intField(value=end_frame, parent=UI_saved_asset_list, bgc=(0.3,0.3,0.3))                # end
            cmds.separator(style='in', hr=False, parent=UI_saved_asset_list)

            version_optionMenu = cmds.optionMenu(label="", parent=UI_saved_asset_list)                                  # Version
            versions = versioning(asset_name_path)[1]
            for v in versions:
                cmds.menuItem(label=v)
            cmds.separator(style='in', hr=False, parent=UI_saved_asset_list)

            cmds.text(unique_user, parent=UI_saved_asset_list, font="tinyBoldLabelFont")                                # user
            cmds.separator(style='in', hr=False, parent=UI_saved_asset_list)

            cmds.text(time, parent=UI_saved_asset_list, font="tinyBoldLabelFont")                                       # time
            cmds.separator(style='in', hr=False, parent=UI_saved_asset_list)

            cmds.text(export_path, parent=UI_saved_asset_list, font="tinyBoldLabelFont")                                # export_path
            cmds.separator(style='in', hr=False, parent=UI_saved_asset_list)

            delete_row = cmds.button(label="Delete",parent=UI_saved_asset_list)
            cmds.button(delete_row, e=True, c=partial(deleteRow, delete_row))

            save_row = cmds.button(label="Save",parent=UI_saved_asset_list)
            cmds.button(save_row, e=True, c=partial(saveRow, save_row))

            UIdata[count] = {
                            "Query_box": asset_checkbox,
                            "asset_name": asset_name,
                            "asset_category": cat_menu,
                            "asset_type": type_menu,
                            "asset_destination": dest_menu,
                            "export_path": export_path,
                            "version":version_optionMenu,
                            "start_frame": start_intField,
                            "end_frame": end_intField,

                            "user": user,
                            "time": time,
                            "delete_row":delete_row,
                            "save_row": save_row
                        }

        return(UIdata)




    def saveRow(*args):
        """ saves the specific asset in the checklist after the user has changed its settings. """

        button_path = args[0]
        scene_data = getSceneData()[1]
        data = read_json(scene_data)

        for row in UIdata:
            button_path_data = UIdata[row]["save_row"]
            if button_path == button_path_data:

                row_asset_name = UIdata[row]["asset_name"]

                if row_asset_name in data:

                    # Get data for specific asset.
                    query_checkbox = cmds.checkBox(UIdata[row]["Query_box"], query=True, value=True)
                    asset_name = UIdata[row]["asset_name"]
                    query_type = cmds.optionMenu(UIdata[row]["asset_type"], query=True, value=True)
                    query_category = cmds.optionMenu(UIdata[row]["asset_category"], query=True, value=True)
                    query_destination = cmds.optionMenu(UIdata[row]["asset_destination"], query=True, value=True)
                    query_start = cmds.intField(UIdata[row]["start_frame"], query=True, value=True)
                    query_end = cmds.intField(UIdata[row]["end_frame"], query=True, value=True)

                    # Update the assets data based on users input.
                    data[asset_name]["asset_category"] = query_category
                    data[asset_name]["asset_type"] = query_type
                    data[asset_name]["asset_destination"] = query_destination
                    data[asset_name]["start_frame"] = query_start
                    data[asset_name]["end_frame"] = query_end
                    data[asset_name]["time"] = time.time()

                    write_to_json(scene_data, data)

                    # Reload UI
                    cmds.evalDeferred(Export_Manager)




    def deleteRow(*args):
        """ Removes the saved asset row from the UI and the dictionairy, and removes the tag from the specific asset. """

        button_path = args[0]
        scene_data = getSceneData()[1]
        data = read_json(scene_data)

        for row in UIdata:
            button_path_data = UIdata[row]["delete_row"]
            if button_path == button_path_data:

                row_asset_name = UIdata[row]["asset_name"]

                if row_asset_name in data:
                    del data[row_asset_name]

                    write_to_json(scene_data, data)

                    # Reload UI
                    cmds.evalDeferred(Export_Manager)




    def getSceneData():

        sceneID = cmds.fileInfo('sceneID', q=True)[0]
        shot_data_dir = os.getenv("SHOT_DATA")
        export_data_dir = shot_data_dir + '\\export_data'
        export_list_json = export_data_dir + '\\export_scene_data_' + str(sceneID) + '.json'

        return(sceneID, export_list_json)




    def clearOptionMenu(optionMneu_path):
        """ pass the optionmenu and it will clear all the items """

        # loop through existing menus in the optionMenu and destroy them
        for item in cmds.optionMenu(optionMneu_path, q=True, ill=True) or []:
            cmds.deleteUI(item)




    def rowTypeChange(*args):
        """ Updates a rows version when a user changes input like the category for example. """

        data = read_json(getSceneData()[1])

        for row in UIdata:

            query_checkbox = cmds.checkBox(UIdata[row]["Query_box"], query=True, value=True)
            asset_name = UIdata[row]["asset_name"]
            query_type = cmds.optionMenu(UIdata[row]["asset_type"], query=True, value=True)
            query_category = cmds.optionMenu(UIdata[row]["asset_category"], query=True, value=True)
            query_destination = cmds.optionMenu(UIdata[row]["asset_destination"], query=True, value=True)
            query_start = cmds.intField(UIdata[row]["start_frame"], query=True, value=True)
            query_end = cmds.intField(UIdata[row]["end_frame"], query=True, value=True)
            #query_version = cmds.optionMenu(UIdata[row]["version"], query=True, value=True)

            path = os.getenv(query_destination.upper().replace(" ", "_"))

            path_category = (path + "/" + query_category)
            path_type = (path_category + "/" + asset_name)
            asset_name_path = (path_type + "/" + query_type)
            full_save_path = asset_name_path

            clearOptionMenu(UIdata[row]["version"])

            try:
                for vers in versioning(full_save_path)[1]:
                    cmds.menuItem(label=vers, parent=UIdata[row]["version"])
            except FileNotFoundError as e:
                cmds.menuItem(label="v001", parent=UIdata[row]["version"])




    def exportSelected(*args):
        """ loops through all the checkboxes in the export list, and exports the checked checkboxes """

        utils.check_if_saved()
        data = read_json(getSceneData()[1])

        for row in UIdata:

            query_checkbox = cmds.checkBox(UIdata[row]["Query_box"], query=True, value=True)
            asset_name = UIdata[row]["asset_name"]
            query_type = cmds.optionMenu(UIdata[row]["asset_type"], query=True, value=True)
            query_category = cmds.optionMenu(UIdata[row]["asset_category"], query=True, value=True)
            query_destination = cmds.optionMenu(UIdata[row]["asset_destination"], query=True, value=True)

            query_start = cmds.intField(UIdata[row]["start_frame"], query=True, value=True)
            query_end = cmds.intField(UIdata[row]["end_frame"], query=True, value=True)
            query_version = cmds.optionMenu(UIdata[row]["version"], query=True, value=True)

            path = os.getenv(query_destination.upper().replace(" ", "_"))

            path_category = (path + "/" + query_category)
            path_type = (path_category + "/" + asset_name)
            asset_name_path = (path_type + "/" + query_type)


            if query_checkbox == True:

                if os.path.exists(path_category) != True:
                    os.mkdir(path_category)
                if os.path.exists(path_type) != True:
                    os.mkdir(path_type)
                if os.path.exists(asset_name_path) != True:
                    os.mkdir(asset_name_path)

                full_save_path = asset_name_path + "/" + query_version

                if os.path.exists(full_save_path) != True:
                    os.mkdir(full_save_path)


                cmds.select(data[asset_name]["selected"])

                for format in export_list_checkBox:

                    query_format_check = cmds.checkBox(format, query=True, label=True)
                    query_format_check_value = cmds.checkBox(format, query=True, value=True)

                    if query_format_check_value == True:

                        save_file = full_save_path + '/' + asset_name + "_" + query_type + "_" + query_version

                        exportAsset(query_format_check,
                                    save_file,
                                    query_start,
                                    query_end,
                                    query_category
                                    )

                        print("\n\n *** Exported: ", asset_name, " | ", query_type, " | ", query_version)
                        print(save_file)


                        TOP_DATA = os.path.dirname(os.getenv("TOP_ASSETS")) + "/data"
                        CAPTURES_DATA_DIR = TOP_DATA + "/exports"
                        if os.path.exists(CAPTURES_DATA_DIR) != True:
                            os.mkdir(CAPTURES_DATA_DIR)

                        JSON_EXPORTS = CAPTURES_DATA_DIR + "/exports.json"

                        if os.path.exists(JSON_EXPORTS) != True:
                            test_data = {}
                            test_data[asset_name] = {
                                                    query_version : {
                                                                    "SHOT": os.getenv("SHOT"),
                                                                    "PROJECT": os.getenv("PROJECT"),
                                                                    "PROJECT_NAME": os.getenv("PROJECT_NAME"),
                                                                    "START": query_start,
                                                                    "END": query_end,
                                                                    "CATEGORY": query_category,
                                                                    "DESTINATION": query_destination,
                                                                    "POSTED_TO_DISCORD": False,
                                                                    "USER": os.environ['COMPUTERNAME'],
                                                                    "PATH": save_file
                                                                    }
                                                    }
                            write_to_json(JSON_EXPORTS, test_data)
                        else:
                            test_data = read_json(JSON_EXPORTS)
                            test_data[asset_name] = {
                                                    query_version : {
                                                                    "SHOT": os.getenv("SHOT"),
                                                                    "PROJECT": os.getenv("PROJECT"),
                                                                    "PROJECT_NAME": os.getenv("PROJECT_NAME"),
                                                                    "START": query_start,
                                                                    "END": query_end,
                                                                    "CATEGORY": query_category,
                                                                    "DESTINATION": query_destination,
                                                                    "POSTED_TO_DISCORD": False,
                                                                    "USER": os.environ['COMPUTERNAME'],
                                                                    "PATH": save_file
                                                                    }
                                                    }
                            write_to_json(JSON_EXPORTS, test_data)

        reloadUI()




    def exportAsset(query_format_check,
                    save_file,
                    query_start,
                    query_end,
                    query_category
                    ):
        """ filters and exports selected assets """

        if query_format_check == "mb":
            export_mayaBinary(save_file)
        elif query_format_check == "abc":
            exportAlembic(save_file, query_start, query_end, query_category)
        elif query_format_check == "fbx":
            print("")
        elif query_format_check == "obj":
            export_OBJ(save_file)




    def filterCamera_OR_geo(query_category, selection_list):
        """ filters between geo and cameras based on what catagory is selected in the export manager """

        objects = []
        # if catorgy is cam, then run this code to select camera and not geo.
        if query_category == "cam":

            # determines if a camera is selected on its own, if its a group with children then we loop until we find the camera.
            all_cameras = cmds.listCameras()
            for cam in all_cameras:

                if cam not in selection_list:

                    for sel in selection_list:
                        selection_children = cmds.listRelatives(sel, ad=True)

                        for obj in selection_children:
                            if obj in all_cameras:
                                objects.append(obj)

                else:
                    objects = selection_list

        # if catorgy is something else, then run this code to return a list of all GEO of selected.
        else:
            objects_to_select = cmds.filterExpand(selection_list, sm=12)  # selects polygons only
            objects = objects_to_select

        return(objects)




    def exportAlembic(save_file, query_start, query_end, query_category):
        """ Exports the alembic. """

        selection_list = cmds.ls(selection=True)

        for obj in selection_list:

            objects_to_select = filterCamera_OR_geo(query_category, selection_list)
            cmds.select(objects_to_select, replace=True)

            # get names in selection
            selection = cmds.ls(selection=True, o=1)

            selection_formatted = ''
            # format it so it fits into the abcexport j mel command
            for sel in selection:
                selection_formatted += ' -root ' + sel
                # formats into single string ex |pCube1|pSphere1|pCube2|group1|pCube3

            command_new = "-frameRange " + str(query_start) + " " + str(query_end) + " -uvWrite -worldSpace -writeVisibility -writeUVSets -dataFormat ogawa" + selection_formatted + " -file " + save_file + ".abc"
            cmds.AbcExport(j=command_new)




    def export_mayaBinary(save_file):
        """ This function exports selected as a maya scene file """
        cmds.file(save_file, force=True, options='v=0', type='mayaBinary', preserveReferences=True, exportSelected=True)




    def export_OBJ(save_file):
        """ This function exports selected as a maya scene file """
        cmds.file(save_file, force=True, options='v=0', type='OBJexport', preserveReferences=True, exportSelected=True)




    def versioning(path_to_dir):
        """ This function returns the current version and the next version number """

        try:
            list_contents = os.listdir(path_to_dir)

            if bool(list_contents) == False:
                latest_version = "v001"

                new_version = "v001"
                current_version = "v001"
                list_contents = ["v001"]

            elif bool(list_contents) == True:
                sort = sorted(list_contents, reverse=True)
                latest_version = sort[0]

                chop_name_end = latest_version[-3:]

                latest_version = int(chop_name_end)
                new_version_num = latest_version + 1

                new_version = ('v{0:03d}'.format(new_version_num))
                current_version = ('{0:03d}'.format(latest_version))

                list_contents.append(new_version)
            version_list = sorted(list_contents, reverse=True)

        except FileNotFoundError:
            new_version = ["v001"]
            version_list = ["v001"]

        return (new_version, version_list)




## UI Updates
    def UICheck(*args):
        """ Checks the UI and changes the settings. """

        asset_name = cmds.textField(txtField_ASSET_NAME, query=True, text=True)
        asset_category = cmds.optionMenu(opMenu_ASSET_CATEGORY, query=True, value=True)
        asset_type = cmds.optionMenu(opMenu_ASSET_TYPE, query=True, value=True)
        asset_destination = cmds.optionMenu(opMenu_ASSET_DESTINATION, query=True, value=True)
        export_path = cmds.textField(txtFielf_EXPORT_PATH, query=True, text=True)

        if asset_type == "anim":
            cmds.optionMenu(opMenu_ASSET_DESTINATION, edit=True, sl=2)
            cmds.textField(txtFielf_EXPORT_PATH, edit=True, text=os.getenv("SHOT_ASSETS"))
        if asset_type == "rig":
            cmds.optionMenu(opMenu_ASSET_DESTINATION, edit=True, sl=1)
            cmds.textField(txtFielf_EXPORT_PATH, edit=True, text=os.getenv("TOP_ASSETS"))
        if asset_type == "geo":
            cmds.optionMenu(opMenu_ASSET_DESTINATION, edit=True, sl=1)
            cmds.textField(txtFielf_EXPORT_PATH, edit=True, text=os.getenv("TOP_ASSETS"))
        if asset_type == "lights":
            cmds.optionMenu(opMenu_ASSET_DESTINATION, edit=True, sl=2)
            cmds.textField(txtFielf_EXPORT_PATH, edit=True, text=os.getenv("SHOT_ASSETS"))




    def UIDestination(*args):
        """  Updates export path when asset destination changes """
        asset_destination = cmds.optionMenu(opMenu_ASSET_DESTINATION, query=True, value=True)
        if asset_destination == "Top Assets":
            cmds.textField(txtFielf_EXPORT_PATH, edit=True, text=os.getenv("TOP_ASSETS"))
        if asset_destination == "Shot Assets":
            cmds.textField(txtFielf_EXPORT_PATH, edit=True, text=os.getenv("SHOT_ASSETS"))




    def dataCheck():
        """ Runs a quick check to see if the data json file exists, if not, creates it. """

        try:
            sceneID = cmds.fileInfo('sceneID', q=True)[0]
        except Exception as e:
            print("No Scene ID, adding scene ID")
            print(e)
            # Set unique scene ID
            unique_ID = str(random.randint(1, 1000000))
            cmds.fileInfo('sceneID', unique_ID)

            sceneID = cmds.fileInfo('sceneID', q=True)[0]

        shot_data_dir = os.getenv("SHOT_DATA")
        export_data_dir = shot_data_dir + '\\export_data'
        export_list_json = export_data_dir + '\\export_scene_data_' + str(sceneID) + '.json'

        if os.path.exists(export_data_dir) != True:
            os.mkdir(export_data_dir)
        if os.path.exists(export_list_json) != True:
            data = {}
            write_to_json(export_list_json, data)





    def reloadUI(*args):
        """ Reloads UI. """
        cmds.evalDeferred(Export_Manager)



    def addText(*args):

        selected_text = cmds.optionMenu(existingMenu, query=True, value=True)
        cmds.textField(txtField_ASSET_NAME, edit=True, text=selected_text)



    def populateExistingMenus():
        """ Populates the existing assets menu. """

        all_existing_assets = []

        existingMenu = cmds.optionMenu(changeCommand=addText)

        top_asset_dir = os.getenv('TOP_ASSETS')
        shot_asset_dir = os.getenv('SHOT_ASSETS')

        asset_catagories = os.listdir(top_asset_dir)
        for cat in asset_catagories:
            for asset in os.listdir(top_asset_dir + "/" + cat):

                if asset not in all_existing_assets:
                    all_existing_assets.append(asset)

        shot_asset_catagories = os.listdir(shot_asset_dir)
        for cata in shot_asset_catagories:
            for asset in os.listdir(shot_asset_dir + "/" + cata):

                if asset not in all_existing_assets:
                    all_existing_assets.append(asset)

        clean_items_list = []
        for item in all_existing_assets:
            if item not in clean_items_list:
                clean_items_list.append(item)


        for item in clean_items_list:
            cmds.menuItem(item)

        return existingMenu


## UI
    dataCheck()

    if cmds.window('Export_Manager_dev', exists=True):
        cmds.deleteUI('Export_Manager_dev')

    window = cmds.window("Export_Manager_dev", widthHeight=(1500, 500))

    cmds.columnLayout(adjustableColumn=True)
    cmds.button(label="Refresh", command=reloadUI)
    cmds.setParent("..")

    Prep_layout = cmds.columnLayout( adjustableColumn=True )
    cmds.frameLayout(label='Prep', cll=True, mh=10,bgc=(0.22,0.22,0.22))
    cmds.gridLayout( numberOfColumns=3, cellWidthHeight=(200, 20) )

    cmds.text(label="")
    existingMenu = populateExistingMenus()
    cmds.setParent("..")

    cmds.gridLayout( numberOfColumns=3, cellWidthHeight=(200, 20) )

    cmds.text(label="Asset Name : ")
    txtField_ASSET_NAME = cmds.textField()
    cmds.text(label="")

    cmds.text(label="Asset Category : ")
    asset_destination = ["char", "prop", "veh", "env", "cam"]
    opMenu_ASSET_CATEGORY = cmds.optionMenu()
    for types in asset_destination:
        cmds.menuItem(types)
    cmds.text(label="") # EMPTY

    cmds.text(label="Asset Type : ")
    asset_types = ["anim", "rig", "geo", "lights", "fx"]
    opMenu_ASSET_TYPE = cmds.optionMenu(changeCommand=UICheck)
    for types in asset_types:
        cmds.menuItem(types)
    cmds.text(label="") # EMPTY

    cmds.text(label="Asset Destination : ")
    asset_destination = ["Top Assets", "Shot Assets"]
    opMenu_ASSET_DESTINATION = cmds.optionMenu(changeCommand=UIDestination)
    for types in asset_destination:
        cmds.menuItem(types)
    cmds.text(label="") # EMPTY


    cmds.text(label="Export Path : ")
    txtFielf_EXPORT_PATH = cmds.textField(text=os.getenv('SHOT_ASSETS'))
    cmds.text(label="") # EMPTY

    cmds.setParent("..")

    cmds.separator(height=1, style='in')

    cmds.gridLayout(numberOfColumns=3, cellWidthHeight=(135, 20))

    cmds.text(label="Range : ")
    intField_START_RANGE = cmds.intField(value=cmds.playbackOptions(q=True, min=True))
    intField_END_RANGE = cmds.intField(value=cmds.playbackOptions(q=True, max=True))

    cmds.setParent("..")

    cmds.gridLayout( numberOfColumns=1, cellWidthHeight=(100, 20) )


    cmds.button(label="Save to Exporter", bgc=(0.65, 1, 0), command=SaveExport)


    cmds.setParent("..")
    cmds.setParent(Prep_layout)

    cmds.columnLayout( adjustableColumn=True )
    cmds.frameLayout(label='Export List', cll=True, mh=10,bgc=(0.22,0.22,0.22))
    #cmds.rowColumnLayout( numberOfColumns=2, columnAttach=(1, 'right', 10), columnWidth=[(1, 500), (2, 250)] )

    cmds.gridLayout( numberOfColumns=22, cellWidthHeight=(60, 20), bgc=(0.22,0.22,0.22))

    cmds.text(label='')
    cmds.separator(style='in', hr=False)
    cmds.text(label='Asset', font="boldLabelFont")
    cmds.separator(style='in', hr=False)
    cmds.text(label='Type', font="boldLabelFont")
    cmds.separator(style='in', hr=False)
    cmds.text(label='Category', font="boldLabelFont")
    cmds.separator(style='in', hr=False)
    cmds.text(label='Dest', font="boldLabelFont")
    cmds.separator(style='in', hr=False)
    cmds.text(label='Start', font="boldLabelFont")
    cmds.separator(style='in', hr=False)
    cmds.text(label='End', font="boldLabelFont")
    cmds.separator(style='in', hr=False)
    cmds.text(label='Version', font="boldLabelFont")
    cmds.separator(style='in', hr=False)
    cmds.text(label='User', font="boldLabelFont")
    cmds.separator(style='in', hr=False)
    cmds.text(label='Time', font="boldLabelFont")
    cmds.separator(style='in', hr=False)

    cmds.text(label='Path', font="boldLabelFont")
    cmds.separator(style='in', hr=False)

    cmds.setParent( '..' )


# populate saved asset data here
    UI_saved_asset_list = cmds.gridLayout( numberOfColumns=24, cellWidthHeight=(60, 15) )
    UIdata = populateExportList()
    cmds.setParent( '..' )
    cmds.separator(height=1, style='in')
##

    cmds.gridLayout( numberOfColumns=7, cellWidthHeight=(100, 25) )
    cmds.button(label="Exported Selected", bgc=(0.65, 1, 0), command=exportSelected)

    cmds.text(label=" : ")

    MB_checkBox_list = cmds.checkBox(label="mb", v=1)
    ABC_checkBox_list = cmds.checkBox(label="abc", v=1)
    FBX_checkBox_list = cmds.checkBox(label="fbx")
    OBJ_checkBox_list = cmds.checkBox(label="obj")
    export_list_checkBox = [MB_checkBox_list, ABC_checkBox_list, FBX_checkBox_list, OBJ_checkBox_list]

    UICheck()



    cmds.showWindow(window)







if __name__ == '__main__':
    Export_Manager()
