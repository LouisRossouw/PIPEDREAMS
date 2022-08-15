import os
import imp

import maya.cmds as cmds

import scene_build.export_manager.export_utils as utils



imp.reload(utils)

def alembic_export_all(export_name, obj_selected, asset_category_eval, asset_type, export_path,
                        start_frame, end_frame, asset_name, export_version_name, save_path
                       ):
    """ basic alembic exporter to export all geo in a scene """

    # creating a geo to show scene information like PFS and ranges
    start_range = cmds.playbackOptions(q=True, min=True)
    end_range = cmds.playbackOptions(q=True, max=True)
    name = str(int(start_frame)) + '_' + str(int(end_frame))
    FPS = cmds.currentUnit( query=True, time=True )
    
    if FPS == 'ntsc':
        FPS_num = '30FPS'
    elif FPS == 'film':
        FPS_num = '24FPS'
    elif FPS == 'pal':
        FPS_num = '25FPS'
    else:
        FPS_num = 'NOT_NTSC'

    #####################################################################

    # Exporting
    path = os.getenv('SHOT_ASSETS') + '/'
    # export_name = 'testicles'

    # Create directories with version num
    filepath = cmds.file(q=True, sn=True)
    filename = os.path.basename(filepath)
    dir_name, extension = os.path.splitext(filename)

    # # export_name = dir_name # NEED TO FIX THIS
    # cat_dir = path + '\\' + asset_category_eval
    # path_to_dir = path + '\\' + asset_category_eval + '\\' + export_name
    #
    # print('writing to:')
    # print(path_to_dir)
    #
    # # creates main dir for specific asset
    # if os.path.exists(cat_dir) != True:
    #     os.mkdir(cat_dir)
    #
    # if os.path.exists(path_to_dir) != True:
    #     os.mkdir(path_to_dir)
    #
    # # creates version 001 dir
    # if os.path.exists(path_to_dir + '\\v001' ) != True:
    #     os.mkdir(path_to_dir + '\\v001' )
    #     save_path = (path_to_dir + '\\v001')
    #     export_version_name = 'v001'
    #
    # # creates version 002 + etc dir
    # else:
    #     new_version = utils.versioning(path_to_dir)[1]
    #     os.mkdir(path_to_dir + '\\v' +  new_version)
    #     save_path = (path_to_dir + '\\v' +  new_version)
    #     export_version_name = 'v' +  new_version
        
    start = int(start_frame) - 11
    end = int(end_frame) + 10

    save_name = str(asset_category_eval) + '_' + export_name + '_' + str(asset_type) + '_'+ export_version_name + '.abc'
    save_to = save_path + '/' + save_name

    # Create single geo with scene info:
    name = 'FrameRange_' + name + '__' + FPS_num + '__' + export_version_name + '_Export'
    cmds.polyPlane(name=name,
                    w=0, h=0,
                    sx=1, sy=1
                    )
    cmds.setAttr( name + '.visibility', 0)
    cmds.setAttr( name + '.translateY', 100000)

    selection_format = ''

    for obj in obj_selected:
        selection_format += ' -root ' + obj

    command_new = "-frameRange " + str(start) + " " + str(end) + " -uvWrite -worldSpace -writeVisibility -writeUVSets -dataFormat ogawa" + selection_format + " -file " + save_to

    cmds.AbcExport ( j = command_new )
    cmds.delete(name)

    



def export_ma(export_name, obj_selected, asset_category_eval, asset_type, export_path,
                        start_frame, end_frame, asset_name, export_version_name, save_path
                       ):
    """ This function exports selected as a maya scene file """

    # Exporting
    path = os.getenv('SHOT_ASSETS') + '/'

    # export_name
    cat_dir = path + '\\' + asset_category_eval
    path_to_dir = path + '\\' + asset_category_eval + '\\' + export_name

    save_name = str(asset_category_eval) + '_' + export_name + '_' + str(asset_type) + '_'+ export_version_name + '.ma'
    save_to = save_path + '/' + save_name

    cmds.file(save_to, force=True, options='v=0', type='mayaAscii', preserveReferences=True, exportSelected=True)



def export_fbx(export_name, obj_selected, asset_category_eval, asset_type, export_path,
                        start_frame, end_frame, asset_name, export_version_name, save_path
                       ):
    """ This function exports selected as a maya scene file """

    # Exporting
    path = os.getenv('SHOT_ASSETS') + '/'

    # export_name
    cat_dir = path + '\\' + asset_category_eval
    path_to_dir = path + '\\' + asset_category_eval + '\\' + export_name

    save_name = str(asset_category_eval) + '_' + export_name + '_' + str(asset_type) + '_'+ export_version_name + '.ma'
    save_to = save_path + '/' + save_name

    cmds.file(save_to, force=True, options='v=0', type='Fbx', preserveReferences=True, exportSelected=True)




if __name__ == '__main__':

    export_name = 'test'
    obj_selected = ''
    asset_category_eval = 'char'
    asset_type = 'animation'
    export_path = 'C:\\Users\\Louis\\Documents\\maya\\projects\\default\\scenes\\cache'
    start_frame = 1
    end_frame = 100
    asset_name = 'bob'
    export_version_name = '001'
    save_path = 'C:\\Users\\Louis\\Documents\\maya\\projects\\default\\scenes\\cache'


    export_ma(export_name, obj_selected, asset_category_eval, asset_type, export_path,
                        start_frame, end_frame, asset_name, export_version_name, save_path
                       )



