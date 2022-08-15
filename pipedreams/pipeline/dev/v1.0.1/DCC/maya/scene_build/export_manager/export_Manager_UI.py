import os
import json
import random

# third party imports
import maya.cmds as cmds
import pymel.core as pm

# local app/lib imports
import scene_build.export_manager.export as export
import scene_build.export_manager.export_utils as utils


def Exporter_window():


    def getExport_list():
        """ This gets the list of exports to display in the UI """

        shot = os.getenv('SHOT')

        try:
            sceneID = cmds.fileInfo('sceneID', q=True)[0]
        except IndexError:
            n = random.randint(1, 10000)
            cmds.fileInfo('sceneID', n)
            sceneID = cmds.fileInfo('sceneID', q=True)[0]

        data = {}

        shot_data_path = os.getenv("SHOT_DATA")
        export_data = shot_data_path + '\\export_data'
        export_data_json = export_data + '\\export_scene_data_' + str(sceneID) + '.json'

        if os.path.exists(shot_data_path) != True:
            os.mkdir(shot_data_path)

        if os.path.exists(export_data) != True:
            os.mkdir(export_data)
        else:
            pass

        if os.path.exists(export_data_json) != True:
            with open(export_data_json, 'w+') as outfile:
                json.dump(data, outfile, indent=4)

        # Read json list
        with open(export_data_json, 'r') as outfile:
            read_json = json.load(outfile)

        return(read_json)

    ###################################################

    def check():

        exports = []
        outliner = cmds.ls()

        for myObject in outliner:

            try:
                EXPORTME = cmds.getAttr(myObject + '.EXPORTME')
            except ValueError:
                EXPORTME = False

            if EXPORTME == True:
                exports.append(myObject)
            else:
                pass

        return(exports)

    ###################################################

    def save_export(*args):

        utils.obj_duplicate_renamer(rename=True)

        # Asset name
        asset_name_eval = pm.textField(asset_name, query=True, text=True)

        # Asset type
        asset_type_eval = pm.optionMenu(asset_type, query=True, value=True)

        # Export path
        export_path_eval = pm.textField(Export_path, query=True, text=True)

        # Get start frame
        start_num_eval = pm.intField(start_frame, query=True, value=True)
        end_num_eval = pm.intField(end_frame, query=True, value=True)


        if asset_name_eval == '':
            cmds.confirmDialog(title='ERROR', message='asset_name is empty, please assign a name',
                               button='Close', cancelButton='Close')
        else:


            # Get radio button selection
            p = pm.radioCollection(category, query=True, sl=True)
            selected_category_name = pm.radioButton(p, query=True, label=True)

            sceneID = cmds.fileInfo('sceneID', q=True)[0]

            shot_data_dir = os.getenv("SHOT_DATA")
            export_data_dir = shot_data_dir + '\\export_data'
            export_list_json = export_data_dir + '\\export_scene_data_' + str(sceneID) + '.json'

            with open(export_list_json, 'r') as json_config:
                data = json.load(json_config)


        ##########  add tag to selection  #############
            # This snippet adds a tag to the attribute editor, EXPORTME with a unique ID
            # and the asset name given by the user
            # This is for single selection

            sel_obj_list = []
            exportMe_TAG = []

            sel_geo = cmds.ls(sl=True)

            for s in sel_geo:

                attr_in_obj = cmds.listAttr(s)

                for attr in attr_in_obj:
                    exptMe = 'EXPORTME'

                    # IF EXPORTME exists in obj node
                    if attr.find(exptMe) != -1:
                        find = True
                    else:
                        find = False

                if find != True:
                    n = random.randint(1, 100000)
                    exportMe = 'EXPORTME_' + str(n) + '_' + str(asset_name_eval)
                    cmds.addAttr(s, longName=exportMe, attributeType='bool', k=True)
                    cmds.setAttr(s + '.' + exportMe, 1)
                    exportMe_TAG.append(str(exportMe))
                else:
                    pass

            # This is for groups and children of children
            p = cmds.listRelatives(ad=True, f=True, type="transform")
            poly = cmds.filterExpand(p, sm=12)
            cmds.select(poly, replace=True)

            newsel = cmds.ls(sl=True, )

            for i in newsel:

                attr_in_obj = cmds.listAttr(i)

                for attr in attr_in_obj:
                    exptMe = 'EXPORTME'

                    # IF EXPORTME exists in obj node
                    if attr.find(exptMe) != -1:
                        find = True
                    else:
                        find = False

                if find != True:

                    n = random.randint(1, 100000)
                    exportMe = 'EXPORTME_' + str(n) + '_' + str(asset_name_eval)

                    cmds.addAttr(i, longName=exportMe, attributeType='bool', k=True)
                    cmds.setAttr(i + '.' + exportMe, 1)
                    exportMe_TAG.append(str(exportMe))
                else:
                    pass

        ##########  add tag to selection  #############

            data[asset_name_eval] = []

            data[asset_name_eval].append({
                'asset_name' : asset_name_eval,
                'asset_type' : asset_type_eval,
                'export_path' : export_path_eval,
                'start_frame' : start_num_eval,
                'end_frame' : end_num_eval,
                'asset_category' : selected_category_name,
                'geo_to_export' : exportMe_TAG,
                    })

            with open(export_list_json, 'w') as outfile:
                json.dump(data, outfile, indent=4)

            # Refresh / reload UI to get a new list of prepped asset names
            Exporter_window()

    ###################################################

    def get_json_export(selected_checkBox):
        """ returns all the info for the specific asset that is saved in a json file """

        sceneID = cmds.fileInfo('sceneID', q=True)[0]
        shot_data_dir = os.getenv("SHOT_DATA")
        export_data_dir = shot_data_dir + '\\export_data'
        export_list_json = export_data_dir + '\\export_scene_data_' + str(sceneID) + '.json'

        with open(export_list_json, 'r') as json_config:
            data = json.load(json_config)

        export_elements = {}

        for key in data:
            if key == selected_checkBox:
                elements = (data[key][0]['geo_to_export'])
                asset_category = (data[key][0]['asset_category'])
                asset_type = (data[key][0]['asset_type'])
                export_path = (data[key][0]['export_path'])
                start_frame = (data[key][0]['start_frame'])
                end_frame = (data[key][0]['end_frame'])
                asset_name = (data[key][0]['asset_name'])

                export_elements[key] = elements

        return(export_elements, asset_category, asset_type,
               export_path, start_frame, end_frame, asset_name, elements, data, export_list_json)


    def checkBox_sel():

        for checkB in checkBox_list:

            checkBox_label = cmds.checkBox(checkB, label=True, query=True)
            checkBox_value = cmds.checkBox(checkB, value=True, query=True)

            if checkBox_value == True:
                print(checkBox_label)


    def export_selected_checkBox(*args):
        """ after the sel by tag function selects all the objs by tag, this function runs the exporting process
            to export alembic, fbx etc per asset name selection
        """

        utils.check_if_saved()
        cmds.select(deselect=True)

        # checkbox_list was appended in the UI

        for checkB in checkdict:

            checkBox_label = cmds.checkBox(checkB, label=True, query=True)
            checkBox_value = cmds.checkBox(checkB, value=True, query=True)

            version_menu = cmds.optionMenu(checkdict[checkB][0], value=True, query=True)

            if checkBox_value == True:

                p = get_json_export(checkBox_label)[0]
                asset_category_eval = get_json_export(checkBox_label)[1]
                asset_type = get_json_export(checkBox_label)[2]
                export_path = get_json_export(checkBox_label)[3]
                start_frame = get_json_export(checkBox_label)[4]
                end_frame = get_json_export(checkBox_label)[5]
                asset_name = get_json_export(checkBox_label)[6]

                for k in p:

                    selected = sel_by_tag(k, asset_ID='')

                    sel_tag = cmds.ls(selection=True)
                    polyGons = cmds.filterExpand(sel_tag, sm=12)
                    cmds.select(polyGons, replace=True)
                    sel = cmds.ls(selection=True)

                    if bool(sel) != False:



                        export_name = k
                        path = os.getenv('SHOT_ASSETS') + '/'

                        # export_name = dir_name # NEED TO FIX THIS
                        cat_dir = path + '\\' + asset_category_eval
                        path_to_dir = path + '\\' + asset_category_eval + '\\' + export_name

                        print('writing to:')
                        print(path_to_dir)

                        # creates main dir for specific asset
                        if os.path.exists(path) != True:
                            os.mkdir(path)

                        if os.path.exists(cat_dir) != True:
                            os.mkdir(cat_dir)

                        # creates version dir if not exist
                        if os.path.exists(path_to_dir) != True:
                            os.mkdir(path_to_dir)

                        # # creates version 001 dir
                        if os.path.exists(path_to_dir + '\\v' + version_menu) != True:
                            os.mkdir(path_to_dir + '\\v' + version_menu)

                        save_path = path_to_dir + '\\v' + version_menu
                        export_version_name = 'v' + version_menu

                        # Alembic CheckBox evaluation
                        abc_checkBox_eval = pm.checkBox(abc_checkBox, value=True, query=True)

                        if abc_checkBox_eval == True:
                            # Export alembic
                            export.alembic_export_all(export_name,
                                                      sel,
                                                      asset_category_eval,
                                                      asset_type,
                                                      export_path,
                                                      start_frame,
                                                      end_frame,
                                                      asset_name,
                                                      export_version_name,
                                                      save_path,
                                                      )
                        else:
                            pass

                        ma_checkBox_eval = pm.checkBox(ma_checkBox, value=True, query=True)

                        # .ma CheckBox evaluation
                        if ma_checkBox_eval == True:

                            # Export maya
                            selected = sel_by_tag(k, asset_ID='')
                            sel_tag = cmds.ls(selection=True)
                            polyGons = cmds.filterExpand(sel_tag, sm=12)
                            cmds.select(polyGons, replace=True)
                            sel = cmds.ls(selection=True)

                            export.export_ma(export_name,
                                             sel,
                                             asset_category_eval,
                                             asset_type,
                                             export_path,
                                             start_frame,
                                             end_frame,
                                             asset_name,
                                             export_version_name,
                                             save_path,
                                             )
                        else:
                            pass


                        FBX_checkBox_eval = pm.checkBox(fbx_checkBox, value=True, query=True)

                        # .ma CheckBox evaluation
                        if FBX_checkBox_eval == True:

                            # Export FBX
                            selected = sel_by_tag(k, asset_ID='')
                            sel_tag = cmds.ls(selection=True)
                            polyGons = cmds.filterExpand(sel_tag, sm=12)
                            cmds.select(polyGons, replace=True)
                            sel = cmds.ls(selection=True)

                            export.export_fbx(export_name,
                                             sel,
                                             asset_category_eval,
                                             asset_type,
                                             export_path,
                                             start_frame,
                                             end_frame,
                                             asset_name,
                                             export_version_name,
                                             save_path,
                                             )

                        else:
                            pass


                    else:
                        print('geo for ' + k + ' does not exist in outliner')

                Exporter_window()




    def sel_by_tag(asset_name, asset_ID):
        """ This function loops through the outliner and each objs attributes and searches for the asset name from the
            EXPORTME tag attr name
        """

        # Selects all geo in the viewportr
        outliner = cmds.ls(selection=False)
        polyGons_list = cmds.filterExpand(outliner, sm=12)

        selection_set = []

        for obj in outliner:

            attr_in_obj = cmds.listAttr(obj)

            for attr in attr_in_obj:

                exportMe = 'EXPORTME'

                # IF EXPORTME exists in obj node
                if attr.find(exportMe) != -1:
                    # Full EXPORTME name for node
                    exportMe_name = (attr_in_obj[-1])

                    remove_int = ''.join([i for i in exportMe_name if not i.isdigit()])
                    # Clean asset name given by the user from the exporter
                    asset_name_clean = remove_int.replace('EXPORTME__', '')
                    # Clean ID assigned to the current obj
                    asset_geo_ID = ''.join([i for i in exportMe_name if i.isdigit()])

                    outliner_name = obj

                    if asset_name == asset_name_clean:

                        attr_eval = cmds.getAttr(obj + '.' + exportMe_name, asString=True)

                        if attr_eval == True:
                            selection_set.append(obj)
                            cmds.select(selection_set, replace=True)
                        else:
                            pass
                    else:
                        pass
                else:
                    pass


    def export_remove(*args):

        for checkB in checkdict:

            checkBox_label = cmds.checkBox(checkB, label=True, query=True)
            checkBox_value = cmds.checkBox(checkB, value=True, query=True)

            version_menu = cmds.optionMenu(checkdict[checkB][0], value=True, query=True)

            if checkBox_value == True:

                elements = get_json_export(checkBox_label)[0]
                asset_category_eval = get_json_export(checkBox_label)[1]
                asset_type = get_json_export(checkBox_label)[2]
                export_path = get_json_export(checkBox_label)[3]
                start_frame = get_json_export(checkBox_label)[4]
                end_frame = get_json_export(checkBox_label)[5]
                asset_name = get_json_export(checkBox_label)[6]
                elem = get_json_export(checkBox_label)[7]
                json_data = get_json_export(checkBox_label)[8]
                json_path = get_json_export(checkBox_label)[9]

                outliner = cmds.ls()

                for element in elem:


                    for obj in outliner:

                        attr = cmds.listAttr(obj)

                        for a in attr:

                            if a.find(element) != -1:
                                print(element)
                                print('removing ' + obj)

                                cmds.deleteAttr(obj, at=element)

                    # Remove from json file
                    del json_data[checkBox_label]

                    with open(json_path, 'w') as json_config:
                        data = json.dump(json_data, json_config, indent=4)

                    Exporter_window()







    # Make a new window UI
    if pm.window('Export_Manager', exists=True):
        pm.deleteUI('Export_Manager')

    window = pm.window("Export_Manager", widthHeight=(1200, 500) )

    pm.columnLayout( adjustableColumn=True )

    ew = pm.frameLayout( label='prep_asset', borderStyle='etchedOut', cll=True, mh=10,)

    pm.rowColumnLayout( numberOfColumns=2, columnAttach=(1, 'right', 0), columnWidth=[(10, 100), (2, 250)] )

    pm.text( label='asset_name :' )
    asset_name = pm.textField()


    pm.text( label='asset_type :' )
    asset_type = pm.optionMenu()
    pm.menuItem( label='animation' )
    pm.menuItem( label='model' )

    pm.text( label='Export_path :' )
    item = os.getenv('SHOT_ASSETS')
    Export_path = pm.textField(text=item )


    pm.separator( height=40, style='in' )

    pm.rowColumnLayout(numberOfColumns=2, columnWidth=[(10, 10), (2, 50)])

    pm.text( label='start_frame :' )
    start = cmds.playbackOptions(q=True, min=True)
    start_frame = pm.intField(v=start)

    pm.text( label='end_frame :' )
    end = cmds.playbackOptions(q=True, max=True)
    end_frame = pm.intField(v=end)

    pm.setParent( '..' )
    pm.separator( height=40, style='in' )


    pm.rowColumnLayout(numberOfColumns=5,)


    category = pm.radioCollection()
    prop = pm.radioButton(label='prop')
    cam = pm.radioButton(label='cam')
    veh = pm.radioButton(label='veh')
    char = pm.radioButton(label='char')
    env = pm.radioButton(label='env')


    pm.setParent( ew )

    pm.button( label='save_export', bgc=(0.65, 1, 0), command=save_export)

    pm.setParent( '..' )


    ## Export
    pm.frameLayout( label='Export', borderStyle='etchedOut',  cll=True, mh=10,)

    pm.columnLayout( adjustableColumn=True )

    pm.gridLayout( numberOfColumns=14, cellWidthHeight=(70, 50) )

    pm.text(label='asset')
    pm.separator(style='in', hr=False)
    pm.text(label='type')
    pm.separator(style='in', hr=False)
    pm.text(label='category')
    pm.separator(style='in', hr=False)
    pm.text(label='start')
    pm.separator(style='in', hr=False)
    pm.text(label='end')
    pm.separator(style='in', hr=False)
    pm.text(label='version')
    pm.separator(style='in', hr=False)
    pm.text(label='path')
    pm.separator(style='in', hr=False)

    pm.setParent( '..' )

    pm.separator(style='in' )

    exports = getExport_list()
    sceneID = cmds.fileInfo('sceneID', q=True)[0]
    shot = os.getenv('SHOT')

    checkBox_list = []
    option_menu_versions_list = []

    checkdict = {}

    for obj in exports:


        shot_data_dir = os.getenv("SHOT_DATA")
        export_data_dir = shot_data_dir + '\\export_data'
        export_list_json = export_data_dir + '\\export_scene_data_' + str(sceneID) + '.json'

        with open(export_list_json, 'r') as json_config:
            data = json.load(json_config)

        asset_type_var = data[obj][0]['asset_type']
        asset_category_var = data[obj][0]['asset_category']
        start_frame_var = data[obj][0]['start_frame']
        end_frame_var = data[obj][0]['end_frame']
        export_path_var = data[obj][0]['export_path']
        export_name_var = data[obj][0]['asset_name']

        checkBox_gridLayout = pm.gridLayout(numberOfColumns=17, cellWidthHeight=(70, 25))
        obj = pm.checkBox( label=obj )
        checkBox_list.append(obj)

        pm.separator(style='in', hr=False)
        pm.text( label=asset_type_var)
        pm.separator(style='in', hr=False)
        pm.text( label=asset_category_var)
        pm.separator(style='in', hr=False)
        pm.text( label=start_frame_var)
        pm.separator(style='in', hr=False)
        pm.text( label=end_frame_var)
        pm.separator(style='in', hr=False)
        option_menu_versions = pm.optionMenu(label='v')

        # get version numbers to add to the list in the manager
        path = os.getenv('SHOT_ASSETS') + '/'
        versions_path = path + asset_category_var + '/' + export_name_var

        try:
            versions = tuple(reversed(utils.versioning(versions_path)))
        except WindowsError:
            versions = ['001']
        except IndexError:
            versions = ['001']

        for version in versions:
            pm.menuItem(label=version)

        pm.separator(style='in', hr=False)
        pm.optionMenu()
        pm.menuItem(label=export_path_var)
        # pm.text( label=export_path_var)

        pm.separator(style='in', hr=False)

        pm.button( label='edit')
        # remove_button = pm.button(label='remove', command=export_remove)

        checkdict[obj] = [option_menu_versions, export_name_var]

        pm.setParent( '..' )

        pm.separator(style='in', hr=True)

    #pm.rowColumnLayout( numberOfColumns=2, columnAttach=(1, 'right', 0), columnWidth=[(10, 100), (2, 250)] )
    pm.gridLayout( numberOfColumns=6, cellWidthHeight=(100, 25) )

    pm.button( label='Export_selected', bgc=(0.65, 1, 0), command=export_selected_checkBox)
    pm.button( label='Remove_selected', bgc=(0.65, 1, 0), command=export_remove)

    pm.separator(style='in', hr=False)

    ma_checkBox = pm.checkBox(label='ma', value=True)
    fbx_checkBox = pm.checkBox(label='fbx', value=False)
    abc_checkBox = pm.checkBox(label='abc', value=True)

    pm.setParent( '..' )

    pew = pm.showWindow( window )







if __name__ == '__main__':
    getVersion()
