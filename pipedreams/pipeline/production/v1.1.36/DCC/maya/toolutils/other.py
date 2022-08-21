import os
from maya import cmds


def camera_build():
    """ Creates a quick camera in a specific hierarchy """

    camera = cmds.camera(n='camcam')
    cameraShape = camera[1]

    # Cam_SRT
    cam_SRT_create = cmds.circle(n='cam_SRT')
    cam_SRT = cam_SRT_create[0]
    cmds.setAttr(cam_SRT+'.rx', 90)
    cmds.setAttr(cam_SRT+'.sx', 2)
    cmds.setAttr(cam_SRT+'.sy', 2)
    cmds.setAttr(cam_SRT+'.sz', 2)
    cmds.makeIdentity(cam_SRT, apply=True)

    # cam_y
    cam_y_create = cmds.spaceLocator(n='cam_y')
    cam_y = cam_y_create[0]
    cmds.setAttr(cam_y+'.sx', keyable=False)
    cmds.setAttr(cam_y+'.sy', keyable=False)
    cmds.setAttr(cam_y+'.sz', keyable=False)

    # cam_z
    cam_z_create = cmds.spaceLocator(n='cam_z')
    cam_z = cam_z_create[0]
    cmds.setAttr(cam_z+'.sx', keyable=False)
    cmds.setAttr(cam_z+'.sy', keyable=False)
    cmds.setAttr(cam_z+'.sz', keyable=False)

    # cam_trans
    cam_trans_create = cmds.spaceLocator(n='cam_trans')
    cam_trans = cam_trans_create[0]
    cmds.setAttr(cam_trans+'.sx', keyable=False)
    cmds.setAttr(cam_trans+'.sy', keyable=False)
    cmds.setAttr(cam_trans+'.sz', keyable=False)

    # cam_rot
    cam_rot_create = cmds.spaceLocator(n='cam_rot')
    cam_rot = cam_rot_create[0]
    cmds.setAttr(cam_rot+'.sx', keyable=False)
    cmds.setAttr(cam_rot+'.sy', keyable=False)
    cmds.setAttr(cam_rot+'.sz', keyable=False)

    # cam_noise
    cam_noise_create = cmds.spaceLocator(n='cam_noise')
    cam_noise = cam_noise_create[0]
    cmds.setAttr(cam_noise+'.sx', keyable=False)
    cmds.setAttr(cam_noise+'.sy', keyable=False)
    cmds.setAttr(cam_noise+'.sz', keyable=False)

    # parent
    cmds.parent(camera, cam_noise)
    cmds.parent(cam_noise, cam_rot)
    cmds.parent(cam_rot, cam_trans)
    cmds.parent(cam_trans, cam_z)
    cmds.parent(cam_z, cam_y)
    cmds.parent(cam_y, cam_SRT)