import logging

from PySide2 import QtWidgets, QtCore
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import maya.cmds as cmds
import pymel.core as pmc
import random as rand

log = logging.getLogger(__name__)


def maya_main_window():
    """Return the maya main window widget"""
    main_window = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window), QtWidgets.QWidget)


class ScatterToolUI(QtWidgets.QDialog):
    """Scatter UI Class"""

    def __init__(self):
        super(ScatterToolUI, self).__init__(parent=maya_main_window())
        self.setWindowTitle("Scatter")
        self.setMinimumWidth(500)
        self.setMaximumHeight(200)


class ScatterTool(object):

    @QtCore.Slot()
    def scatter(self):
        """Scatter object along the vertices of another object"""
        selection = cmds.ls(os=True, fl=True)
        vertex_list = cmds.filterExpand(selectionMask=31, expand=True)
        object_to_instance = selection[0]
        if cmds.objectType(object_to_instance) == 'transform':
            for vertex in vertex_list:
                new_instance = cmds.instance(object_to_instance)
                position = cmds.pointPosition(vertex, w=True)
                pmc.move(position[0], position[1], position[2], new_instance,
                         a=True, ws=True)
                min_rotate = 10.0
                max_rotate = 90.0
                rand_rotation = rand.uniform(min_rotate, max_rotate)
                print(rand_rotation)
                cmds.rotate(rand_rotation, rand_rotation, rand_rotation,
                            new_instance, r=True)
        else:
            print("Please ensure the object you select is a transform")
