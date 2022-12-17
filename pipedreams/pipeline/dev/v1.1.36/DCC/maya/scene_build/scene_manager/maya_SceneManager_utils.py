import maya.cmds as cmds


def import_asset(action, asset_path,
                 asset_type, catagory,
                 asset_name, current_version, NameSpace):

    # import / reference action
    if action == "Import":

        # popup for import
        cmds.textManip(v=True)
        cmds.headsUpMessage('Imported ' + asset_path, time=2.0)
        cmds.textManip(v=True)

        # checks outliner for all existing items
        before = set(cmds.ls(type="transform"))
        cmds.file(asset_path, i=True, namespace=catagory)

        # checks outliner for new items
        after = set(cmds.ls(type="transform"))

        # compares and gets the difference
        imported = after - before

        if asset_type != "rig":
            selection = cmds.ls(imported)
            group_name = cmds.group(selection, name=catagory + "_" + asset_name + "_" + current_version)

            if catagory == "char":
                cmds.setAttr(group_name + ".useOutlinerColor", True)
                cmds.setAttr(group_name + ".outlinerColor", 1 ,0 ,0.7)
            elif catagory == "env":
                cmds.setAttr(group_name + ".useOutlinerColor", True)
                cmds.setAttr(group_name + ".outlinerColor", 0.2, 1, 0.4)
            elif catagory == "prop":
                cmds.setAttr(group_name + ".useOutlinerColor", True)
                cmds.setAttr(group_name + ".outlinerColor", 0.8, 1, 0)
            elif catagory == "cam":
                cmds.setAttr(group_name + ".useOutlinerColor", True)
                cmds.setAttr(group_name + ".outlinerColor", 0.4 ,1 ,0.8)
            elif catagory == "veh":
                cmds.setAttr(group_name + ".useOutlinerColor", True)
                cmds.setAttr(group_name + ".outlinerColor", 0.5 ,1 ,0.1)


    if action == "Reference":
        Namespace_query = NameSpace

        if Namespace_query == True:
            cmds.file(asset_path, r=True, namespace=catagory)
        elif Namespace_query == False:
            cmds.file(asset_path, r=True, dns=True)



    if action == "Reload":

        # check if file exists
        exists = cmds.file(asset_path, query=True, exists=True)
        if exists == True:
            refNodes = cmds.ls(type="reference")
            for ref in refNodes:

                if str(asset_name + "_" + asset_type) in str(ref):
                    print("Updating Reference for: ", asset_name)
                    cmds.file(asset_path, loadReference=ref)