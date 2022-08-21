""" Simple tool to add animation to selected limbs while skinning """
import os
import json

import maya.cmds as cmds
from functools import partial




def QuickAnim_Skin_UI():
    """ Loads the main UI """

    def run(*args):
        """ Runs the tool on button press """

        left_checkbox_eval = cmds.checkBox(check_left, query=True, value=True)
        right_checkbox_eval = cmds.checkBox(check_right, query=True, value=True)

        RIG = cmds.optionMenu(selected_RIG, query=True, value=True)
        cmds.select(RIG)

        selected = button_data[args[0]]
        selection_controls = return_controls()

        # Add color to selected button
        cmds.button(args[0], edit=True, bgc=(1, 0, 0.65),)

        if left_checkbox_eval == True:
            key("L0", selection_controls, selected)
        if right_checkbox_eval == True:
            key("R0", selection_controls, selected)

        cmds.select(clear=True)




    def key(limb, selection_controls, selected):
        """ Sets a keys on the selected control """

        key_data = get_component_cordinates(limb)

        for key, values in key_data[selected].items():

                count = -1
                for sel in selection_controls:

                    if key in sel:
                        if "ctl" in sel:
                            if "Shape" not in sel:

                                # Key all attributes on frame 0
                                cmds.setKeyframe(sel)

                                # Get data to set keys on specific attributes every 1 second for every set data
                                for dic in values:

                                    count += 1
                                    time = str(count / 2) + 'sec'
                                    cmds.setKeyframe(sel, time=[time])

                                    for v in dic:

                                        attribute_name = v
                                        attribute_value = dic[v]

                                        print(f"{count} - Setting Keys - {sel} | {attribute_name, attribute_value}")

                                        cmds.setKeyframe(
                                                        sel,
                                                        at=attribute_name,
                                                        time=[time],
                                                        v=attribute_value
                                                        )




    def get_component_cordinates(limb):
        """ Returns a list of the values for every control for when the tool needs to set keys """

        # Finds height by boundingbox and devides value to get a good amount to drop the cog
        Yheight = selected_BBOX_measure()[1] / 4

        data = {}

        # data[button match] = {selected cntrl match} : [{key frame}, {key next frame}, {key next next frame etc}]

        data["separator_1"] = ""

        data["Head_Neck"] = {"neck_C0_fk0_ctl" : [{"rx":0}, {"rx":30}, {"rz":0}, {"rx":-30}, {"rx":0}, {"ry":-30}, {"ry":30}, {"ry":0}, {"rz":-25}, {"rz":25}, {"rz":0}],
                            "neck_C0_fk1_ctl": [{"rx": 0}, {"rx": 30}, {"rz": 0}, {"rx": -30}, {"rx": 0}, {"ry": -30}, {"ry": 30}, {"ry": 0}, {"rz": -25}, {"rz": 25}, {"rz": 0}],
                             "neck_C0_head_ctl": [{"rx": 0}, {"rx": 30}, {"rz": 0}, {"rx": -30}, {"rx": 0}, {"ry": -30}, {"ry": 30}, {"ry": 0}, {"rz": -25}, {"rz": 25}, {"rz": 0}]}

        data["separator_1"] = ""

        data["Shoulder"] = {"shoulder_"+limb+"_ctl" : [{"ry":0}, {"ry":-30}, {"ry":0}, {"ry":15}, {"ry":0}, {"rz":-50},
                                                       {"rz":0}, {"rz":25}, {"rz":0}]}

        data["Arm"] = {"arm_"+limb+"_fk0_ctl" : [{"ry":0}, {"ry":80}, {"rz":-90, "ry":80}, {"rz":-90, "ry":0}, {"ry":0},
                                                 {"ry":-90}, {"ry":0},]}

        data["Forarm"] = {"arm_"+limb+"_fk1_ctl" : [{"rz":0}, {"rz":-120}, {"rz":0}]}

        data["Hand"] = {"arm_"+limb+"_fk2_ctl" : [{"ry":0}, {"ry":-90}, {"ry":0}, {"ry":90}, {"ry":0}, {"rx":-90},
                                                  {"rx":0}, {"rx":90}, {"rx":0}, {"rx":-32, "ry":-35, "rz":-20}, {"ry":0}]}

        data["Fingers"] = {"finger_"+limb+"_fk0_ctl" : [{"rz":0}, {"rz":90}, {"rz":0}],
                           "finger_" + limb + "_fk1_ctl": [{"rz": 0}, {"rz": 90}, {"rz": 0}],
                            "finger_" + limb + "_fk2_ctl": [{"rz": 0}, {"rz": 90}, {"rz": 0}]}
#
        data["separator_2"] = ""

        data["Body_COG"] = {"body_C0_ctl" : [{"ty":0}, {"ty":-Yheight}, {"ty":0}, {"rx":90}, {"rx":0}, {"rx":-60}, {"rx":0}]}

        data["FK_Spine"] = {"spine_C0_fk0_ctl" : [{"rx":0}, {"rx":38}, {"rx":0}, {"rx":-20}, {"rx":0}, {"rz":25}, {"rz":0}, {"rz":-25}, {"rz":0}, {"ry":30}, {"ry":0}, {"ry":-30}, {"ry":0}],
                           "spine_C0_fk1_ctl": [{"rx": 0}, {"rx": 38}, {"rx": 0},{"rx":-20}, {"rx":0}, {"rz":25}, {"rz":0}, {"rz":-25}, {"rz":0}, {"ry":30}, {"ry":0}, {"ry":-30}, {"ry":0}],
                            "spine_C0_fk2_ctl": [{"rx": 0}, {"rx": 38}, {"rx": 0}, {"rx":-20}, {"rx":0}, {"rz":25}, {"rz":0}, {"rz":-25}, {"rz":0}, {"ry":30}, {"ry":0}, {"ry":-30}, {"ry":0}]}
#
        data["separator_3"] = ""

        data["Leg_L"] = {"leg_L0_ik_ctl" : [{"ty":0}, {"ty":50, "tz":30}, {"ty":73, "tz":-61, "rx":135}, {"ty":61, "tz":-69, "rx":98}, {"ty":0}, {"tx":70, "ty":58, "rx":30, "rz":65}, {"rx":0}]}
        data["Leg_R"] = {"leg_R0_ik_ctl" : [{"ty":0}, {"ty":50, "tz":30}, {"ty":73, "tz":-61, "rx":135}, {"ty":61, "tz":-69, "rx":98}, {"ty":0}, {"tx":-70, "ty":58, "rx":30, "rz":-65}, {"rx":0}]}

        data["Foot"] = {"leg_"+limb+"_ik_ctl" : [{"rx":0}, {"rx":-35}, {"rx":0}, {"rx":30}, {"rx":0}, {"ry":-50}, {"ry":0}, {"ry":50}, {"ry":0}, {"rz":-35}, {"rz":0}, {"rz":35}, {"rz":0}]}

        data["separator_4"] = ""

        return(data)




    def return_controls():
        """ returns a list of all the controls(children) within the selected rig """

        selection = cmds.ls(selection=True)
        selection_children = cmds.listRelatives(selection, ad=True)

        if bool(selection) == True:

            select_list = []

            for child in selection_children:
                if "ctl" in child:
                    if "Shape" not in child:
                        select_list.append(child)

            return (select_list)

        else:
            print("Nothing Selected")
            cmds.confirmDialog(title='Nothing Selected', message='Empty Selection - Please Select an Mgear Rig')




    def clear_all_keys(*args):
        """ Clears all existing keys, and resets all controls to 0 """

        RIG = cmds.optionMenu(selected_RIG, query=True, value=True)
        cmds.select(RIG)

        selection_controls = return_controls()

        for selected in selection_controls:

            if "ctl" in selected:
                if "Shape" not in selected:

                    all_keys = sorted(cmds.keyframe(selected, q=True) or [])
                    cmds.cutKey(selected, time=(-100, 1000), option="keys")

                    attribute = ["tx", "ty", "tz", "rx", "ry", "rz"]

                    for attr in attribute:

                        try:
                            cmds.setAttr(str(selected) + "." + attr, 0)
                        except RuntimeError:
                            pass

        cmds.select(clear=True)

        # Clear component button color
        for button in button_data:
            cmds.button(button, edit=True, bgc=(.35,.35,.35))
        # Clear Pose buttons color
        for pose_button in POSE_button_DATA:
            cmds.button(pose_button, edit=True, bgc=(.35, .35, .35))




    def selected_BBOX_measure():
        """ Returns the selected boundingBox measurements """

        RIG = cmds.optionMenu(selected_RIG, query=True, value=True)
        cmds.select(RIG)

        sel = cmds.ls(selection=True)
        Unit_measurement = cmds.currentUnit(query=True, linear=True)

        # X min | Y min | Z min ||| X max | Y max | Z max
        BBOX = cmds.exactWorldBoundingBox(sel[0])

        Xmin = BBOX[0]
        Ymin = BBOX[1]
        Zmin = BBOX[2]

        Xmax = BBOX[3]
        Ymax = BBOX[4]
        Zmax = BBOX[5]

        Xwidth_scale = Xmax - Xmin
        Yheight_scale = Ymax - Ymin
        Zdepth_scale = Zmax - Zmin

        cmds.select(clear=True)

        Output = f"X - {round(Xwidth_scale, 2)} {Unit_measurement}\nY - {round(Yheight_scale, 2)} {Unit_measurement}\nZ - {round(Zdepth_scale, 2)} {Unit_measurement}"

        return(Xwidth_scale, Yheight_scale, Zdepth_scale)




    def min_max_keys(selection_controls):
        """ checks object for its first key and last key and returns their frames """

        keys = []
        for sel in selection_controls:

            if "ctl" in sel:
                if "Shape" not in sel:

                    keyframe_info = cmds.keyframe(sel, q=True)

                    if keyframe_info != None:

                        for k in keyframe_info:

                            keys.append(k)

        first_frame_key = sorted(keys)[0]
        last_frame_key = sorted(keys)[-1]

        return (first_frame_key, last_frame_key)




    def write_to_json(json_path, data):
        """ Create and write to json file """

        with open(json_path, 'w') as f:
            json.dump(data, f, indent=6)




    def read_json(json_path):
        """ Reads json file """
        with open(json_path) as f:
            json_file = json.loads(f.read())

        return (json_file)




    def check_dirs():
        """ checks if dirs exists """

        directories = ["Pipedreams", "data", "QuickAnim_Skin"]
        sub_directories = ["Animation", "Pose"]

        Documents_path = os.path.expanduser('~')

        if "Documents" not in Documents_path:
            Documents_path += "/Documents"

        for dir in directories:
            Documents_path += "/" + dir
            if os.path.exists(Documents_path) != True:
                os.mkdir(Documents_path)

        # home_path = os.getenv("HOME")
        Documents_path = os.path.expanduser('~')
        if "Documents" not in Documents_path:
            Documents_path += "/Documents"

        for sub in sub_directories:
            subs_path = Documents_path + "/Pipedreams/data/QuickAnim_Skin/" + sub

            if os.path.exists(subs_path) != True:
                os.mkdir(subs_path)




    def getData(controls_list):
        """ Gets every controls attribute data and stores it in a dictionary """

        data = {}

        for control in controls_list:
            get_TRANSLATE = cmds.getAttr(control + ".translate")
            get_ROTATE = cmds.getAttr(control + ".rotate")

            data[control] = {"translate": get_TRANSLATE, "rotate": get_ROTATE}

        return (data)




    def exportDataPose(FILE_PATH):
        """" Writes out controls and their data """

        save_name = cmds.textField(save_name_input, query=True, text=True)

        if save_name == "":
            print("Save Text field empty")
            cmds.confirmDialog(title='Empty text field', message='Empty text field empty, please name the export under "Save Name"')

        elif save_name != "":
            print("Exporting: " + save_name)

            export_type = cmds.optionMenu(save_type, query=True, value=True)

            controls_list = return_controls()
            controls_data = getData(controls_list)

            Documents_path = os.path.expanduser('~')
            if "Documents" not in Documents_path:
                Documents_path += "/Documents"

            save_path = Documents_path + "/Pipedreams/data/QuickAnim_Skin/" + export_type + "/" + save_name + "_" + export_type + ".json"
            print("Writing to json")
            write_to_json(save_path, controls_data)
            print("Done.")

            UpdateUI(window)




    def importDataPose(*args):
        """ Imports existing pose data and applies it to the rig """

        clear_all_keys()

        selected = POSE_button_DATA[args[0]]
        button_split = selected.split("_")[1]
        data_type = button_split.split(".")[0]


        for pose_buttons in POSE_button_DATA:
            cmds.button(pose_buttons, edit=True, bgc=(0.35, 0.35, 0.35))
        cmds.button(args[0], edit=True, bgc=(1, 0, 0.65))

        Documents_path = os.path.expanduser('~')
        if "Documents" not in Documents_path:
            Documents_path += "/Documents"

        file_import_path = Documents_path + "/Pipedreams/data/QuickAnim_Skin/" + data_type + "/" + selected

        controls_list = read_json(file_import_path)

        for control in controls_list:

            translate_attrs = controls_list[control]["translate"][0]
            rotate_attrs = controls_list[control]["rotate"][0]

            tx = float(translate_attrs[0])
            ty = float(translate_attrs[1])
            tz = float(translate_attrs[2])

            rx = float(rotate_attrs[0])
            ry = float(rotate_attrs[1])
            rz = float(rotate_attrs[2])

            try:
                cmds.setAttr(control + ".translate", tx, ty, tz)
                cmds.setAttr(control + ".rotate", rx, ry, rz)
            except Exception as locked_attr:
                pass




    def deletePose(*args):
        """ This removes an existing pose """

        selected = POSE_button_DATA[args[0]]
        button_split = selected.split("_")[1]
        data_type = button_split.split(".")[0]
        button_path = args[0]

        confirmation_Dialog = cmds.confirmDialog(title='Delete Pose', message='Are you sure you want to delete ' + selected + "?",
                           button=['Yes', 'No'], defaultButton='Yes',
                           cancelButton='No', dismissString='No')

        if confirmation_Dialog == "Yes":
            file_import_path = os.getenv("HOME") + "/Documents/Pipedreams/data/QuickAnim_Skin/" + data_type + "/" + selected
            os.remove(file_import_path)

            UpdateUI(window)
        elif confirmation_Dialog == "No":
            pass
        else:
            pass




    def UpdateUI(window):
        """ Deletes the UI window and reloads it """

        try:
            cmds.evalDeferred(QuickAnim_Skin_UI)
            cmds.deleteUI(window)
        except Exception:
            pass




    def updateButtonSaveUI(*args):
        """ Updates the save button UI """

        save_type = args[0]
        cmds.button(save_button, edit=True, label="Save " + save_type)




    def findRigInOutliner():
        """ Searches for rigs in outliener to populate the optionMneu """

        data = []

        outliner = cmds.ls(assemblies=True)

        for rig in outliner:
            if "_rig" in rig:
                data.append(rig)

        found_rig = bool(data)

        if found_rig == False:
            print("No rig found")
            cmds.confirmDialog(title='No rig found', message='No rig found in the Outliner, please add _rig')

        return(data)



### UI

    window = cmds.window(title='QuickAnim Skin', iconName="QuickAnim Skin", widthHeight=(350, 700))
    # Ensures directories exists, to store json files for poses.
    check_dirs()

    ## Exports
    cmds.columnLayout(adjustableColumn=True)


    # Save Dropdown
    edit = cmds.frameLayout(label='testy', cll=False, mh=10, cl=False)
    cmds.rowColumnLayout(numberOfColumns=2, columnAttach=(1, 'left', 0), columnWidth=[(10, 100), (2, 250)])

    cmds.text(label="")
    selected_RIG = cmds.optionMenu()
    for rig in findRigInOutliner():
        cmds.menuItem(label=rig)

    cmds.setParent("..")
    cmds.setParent("..")


    # Save Dropdown
    edit = cmds.frameLayout(label='Save', cll=True, mh=10, cl=True)
    cmds.rowColumnLayout(numberOfColumns=2, columnAttach=(1, 'left', 0), columnWidth=[(10, 100), (2, 250)])


    #   # save poses
    cmds.text(label="Save Name:")
    save_name_input = cmds.textField()


    #   # save type
    cmds.text(label="Save Type:")
    save_type = cmds.optionMenu(changeCommand=updateButtonSaveUI)
    cmds.menuItem(label='Pose')
    cmds.menuItem(label='Animation')


    #   # export Button
    cmds.text(label="")
    save_button = cmds.button(label="Save Pose", bgc=(0.65, 1, 0), command=exportDataPose)

    cmds.setParent(edit)
    cmds.setParent("..")


#   # Components
    cmds.columnLayout(adjustableColumn=True)
    components = cmds.frameLayout(label='Components', cll=True, mh=10)
    cmds.rowColumnLayout(numberOfColumns=2, columnAttach=(1, 'right', 1), columnWidth=[(10, 100), (2, 250)])



    check_left = cmds.checkBox("Left", value=True)
    check_right = cmds.checkBox("Right")

    button_list = get_component_cordinates(limb="None")

    button_data = {}

    for button in button_list:

        if "separator" in button:
            cmds.text(label="")
            cmds.separator()
        else:
            cmds.text(label="")
            button_path = cmds.button(label=button, bgc=[.35,.35,.35])
            button_data[button_path] = button

            cmds.button(button_path, e=True, c=partial(run, button_path))

    cmds.text(label="")
    cmds.button(label="clear keys", bgc=(0.65, 1, 0), command=clear_all_keys)

    cmds.setParent(components)
    cmds.setParent("..")


## Imports

    cmds.columnLayout(adjustableColumn=True)
    edit = cmds.frameLayout(label='Poses', cll=True, mh=10, cl=True)
    cmds.rowColumnLayout(numberOfColumns=3, columnAttach=(1, 'right', 0), columnWidth=[(10, 100), (2, 250)])


    # populate with poses / anims
    Documents_path = os.path.expanduser('~')
    if "Documents" not in Documents_path:
        Documents_path += "/Documents"

    import_path = Documents_path + "/Pipedreams/data/QuickAnim_Skin/"
    pose_dir = os.listdir(import_path + "/Pose")
    anim_dir = os.listdir(import_path + "/Animation")

    POSE_button_DATA = {}

    for anim_button in pose_dir:
        cmds.text(label="   ")


        # Pose button
        anim_button_path = cmds.button(label=anim_button.split("_")[0], bgc=[.35,.35,.35])
        POSE_button_DATA[anim_button_path] = anim_button
        cmds.button(anim_button_path, e=True, c=partial(importDataPose, anim_button_path))


        # Delete Pose Button
        delete_button_path = cmds.button(label="Delete")
        POSE_button_DATA[delete_button_path] = anim_button
        cmds.button(delete_button_path, e=True, c=partial(deletePose, delete_button_path))

    cmds.setParent("..")
    cmds.setParent("..")

    cmds.showWindow(window)






if __name__ == "__main__":

    QuickAnim_Skin_UI()





















