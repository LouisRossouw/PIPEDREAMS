import maya.cmds as cmds



def SCM_import(action, asset_path,asset_type,
               catagory, asset_name, current_version, NameSpace):
    """ Function for the import / reference / reload button in Maya Scene Manager."""

    if action == "Reference":
        reference_assets(NameSpace, asset_path, catagory)

    if action == "Reload":
        reload_assets(asset_path, asset_name, asset_type)

    if action == "Import":
        import_assets(asset_path, asset_type, catagory, asset_name, current_version)




def asset_setup(imported, asset_type,
                catagory, asset_name, current_version):
    """ Groups and adds a color to the assets based on what category it comes from. """

    if asset_type != "rig":

        selection = cmds.ls(imported)
        group_name = cmds.group(selection, name=catagory + "_" + asset_name + "_" + current_version)

        if catagory == "char":

            cmds.setAttr(group_name + ".useOutlinerColor", True)
            cmds.setAttr(group_name + ".outlinerColor", 1, 0, 0.7)

        elif catagory == "env":

            cmds.setAttr(group_name + ".useOutlinerColor", True)
            cmds.setAttr(group_name + ".outlinerColor", 0.2, 1, 0.4)

        elif catagory == "prop":

            cmds.setAttr(group_name + ".useOutlinerColor", True)
            cmds.setAttr(group_name + ".outlinerColor", 0.8, 1, 0)

        elif catagory == "cam":

            cmds.setAttr(group_name + ".useOutlinerColor", True)
            cmds.setAttr(group_name + ".outlinerColor", 0.4, 1, 0.8)

        elif catagory == "veh":

            cmds.setAttr(group_name + ".useOutlinerColor", True)
            cmds.setAttr(group_name + ".outlinerColor", 0.5, 1, 0.1)




def import_assets(asset_path,
                 asset_type, catagory,
                 asset_name, current_version):
    """ Local Import of asset. """

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

    # Groups and adds a color.
    asset_setup(imported, asset_type, catagory, asset_name, current_version)




def reference_assets(NameSpace, asset_path, catagory):
    """ Refrences the asset into Maya. """

    Namespace_query = NameSpace

    if Namespace_query == True:
        cmds.file(asset_path, r=True, namespace=catagory)

    elif Namespace_query == False:
        cmds.file(asset_path, r=True, dns=True)



def reload_assets(asset_path, asset_name, asset_type):
    """ Reloads / Updates the existing asset to which ever version the user selects. """

    # check if file exists
    exists = cmds.file(asset_path, query=True, exists=True)

    if exists == True:

        refNodes = cmds.ls(type="reference")
        for ref in refNodes:

            if str(asset_name + "_" + asset_type) in str(ref):

                print("Updating Reference for: ", asset_name)
                cmds.file(asset_path, loadReference=ref)



