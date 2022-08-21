import os

from maya import cmds








def sel_all_geo(long_name=bool):
    """ this selects only the geo in the scene """

    # Selects all geo in the viewportr
    outliner = cmds.ls(selection = True)
    polyGons = cmds.filterExpand(outliner, sm = 12)
    cmds.select(polyGons, replace = True)

    # get names in selection
    # selection = cmds.ls(sl=1,o=1)
    if long_name == False:
        selection = cmds.ls(sl=1,o=1)
    elif long_name == True:
        selection = cmds.ls(sl=1,o=1,l=1)

    selection_formatted = ''    
    # format it so it fits into the abcexport j mel command
    for sel in selection:
        selection_formatted += ' -root ' + sel
        # formats into single string ex |pCube1|pSphere1|pCube2|group1|pCube3
    return(selection_formatted, selection)


def obj_duplicate_renamer(rename=bool):
    """ Rename an obj that already has the same name as another obj in the scene """

    listA = []
    listB_full_path = []

    selected_geo = sel_all_geo(long_name=False)[1]

    i = 0
    for obj in selected_geo:
        # This returns a clean name - Maya is weird
        try:
            parent_name = cmds.listRelatives(obj, parent=True)
            if parent_name != None:
                name_clean = obj.replace(parent_name[0] + '|', '')
            else:
                name_clean = obj[0]
            full_name = parent_name[0] + '|' + name_clean
        except TypeError:
            name_clean = obj.replace('|', '')

        # Checks if it is in the list, if it is, it increments the number and then appends
        if name_clean in listA:
            i += 1
            name_clean = name_clean + '_' + str(i)
            cmds.rename(full_name, name_clean)

        else:
            pass

        listA.append(name_clean)
    return(name_clean, listA)


def versioning(path_to_dir):
    """ This function returns the current version and the next version number """
    list_contents = os.listdir(path_to_dir)
    sort = sorted(list_contents, reverse=True)
    latest_version = sort[0]

    chop_name_end = latest_version[-3:]
    
    latest_version = int(chop_name_end)
    new_version_num = latest_version + 1
    new_version = ('{0:03d}'.format(new_version_num))

    current_version = ('{0:03d}'.format(latest_version))
    return(current_version, new_version)


def check_if_saved():
    """ This checks if the maya scene is saved, if not program stops """

    filepath = cmds.file(q=True, sn=True)
    filename = os.path.basename(filepath)
    dir_name, extension = os.path.splitext(filename)

    if (bool(dir_name)) == False:
        cmds.confirmDialog(title = 'ERROR', message='Please save the scene first before exporting',
                            button='Close', cancelButton='Close')
        exit()


def json_export_info():
    """ export info from a specific export / shot """
    pass



if __name__ == '__main__':
    p = obj_duplicate_renamer(rename=True)
    print(p[1])




