import maya.cmds as cmds
import pymel.core as pmc

selection = cmds.ls(os=True, fl=True)
vertex_list = cmds.filterExpand(selectionMask=31, expand=True)
object_to_instance = selection[0];

if cmds.objectType(object_to_instance) == 'transform':
    vert = "vertex"
    for vert in vertex_list:
        new_instance = cmds.instance(object_to_instance)
        position = cmds.pointPosition(vert, w=True)
        pmc.move(position[0], position[1], position[2], new_instance, a=True,
                 ws=True)
else:
    print("Please ensure the object you select is a transform")