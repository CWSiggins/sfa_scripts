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
                self.random_rotation(new_instance)
                self.random_scale(new_instance)
        else:
            print("Please ensure the object you select is a transform")

    @staticmethod
    def random_scale(new_instance):
        min_scale = 0.8
        max_scale = 1.2
        rand_scale = rand.uniform(min_scale, max_scale)
        cmds.scale(rand_scale, rand_scale, rand_scale, new_instance,
                   r=True)

    @staticmethod
    def random_rotation(new_instance):
        min_rotate_x = 10.0
        max_rotate_x = 90.0
        rand_rotation_x = rand.uniform(min_rotate_x, max_rotate_x)
        min_rotate_y = 10.0
        max_rotate_y = 90.0
        rand_rotation_y = rand.uniform(min_rotate_y, max_rotate_y)
        min_rotate_z = 10.0
        max_rotate_z = 90.0
        rand_rotation_z = rand.uniform(min_rotate_z, max_rotate_z)
        cmds.rotate(rand_rotation_x, rand_rotation_y, rand_rotation_z,
                    new_instance, r=True)
