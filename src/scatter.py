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
        self.setWindowTitle("Scatter Tool")
        self.setMinimumWidth(325)
        self.setMaximumHeight(200)
        self.scatter_tool = ScatterTool()
        self.create_ui()
        self.create_connections()

    def create_ui(self):
        self.title_lbl = QtWidgets.QLabel("Scatter Objects")
        self.title_lbl.setStyleSheet("font: bold 20px")
        self.scale_lay = self._create_max_scale_ui()
        self.min_x_rotate_lay = self._create_min_x_rotation_ui()
        self.max_x_rotate_lay = self._create_max_x_rotation_ui()
        self.min_y_rotate_lay = self._create_min_y_rotation_ui()
        self.max_y_rotate_lay = self._create_max_y_rotation_ui()
        self.min_z_rotate_lay = self._create_min_z_rotation_ui()
        self.max_z_rotate_lay = self._create_max_z_rotation_ui()
        self.button_lay = self._create_button_ui()
        self.main_lay = QtWidgets.QVBoxLayout()
        self.main_lay.addWidget(self.title_lbl)
        self.main_lay.addLayout(self.scale_lay)
        self.main_lay.addLayout(self.min_x_rotate_lay)
        self.main_lay.addLayout(self.max_x_rotate_lay)
        self.main_lay.addLayout(self.min_y_rotate_lay)
        self.main_lay.addLayout(self.max_y_rotate_lay)
        self.main_lay.addLayout(self.min_z_rotate_lay)
        self.main_lay.addLayout(self.max_z_rotate_lay)
        self.main_lay.addLayout(self.button_lay)
        self.setLayout(self.main_lay)

    def create_connections(self):
        """Connect Signals and Slots"""
        self.scatter_btn.clicked.connect(self._scatter)

    @QtCore.Slot()
    def _scatter(self):
        """Scatter objects"""
        self._set_scatter_properties_from_ui()
        self.scatter_tool.scatter()

    def _set_scatter_properties_from_ui(self):
        self.scatter_tool.min_scale = self.min_scale_sbx.value()
        self.scatter_tool.max_scale = self.max_scale_sbx.value()
        self.scatter_tool.min_rotate_x = self.min_x_rotation_sbx.value()
        self.scatter_tool.min_rotate_x = self.min_x_rotation_sbx.value()
        self.scatter_tool.min_rotate_y = self.min_y_rotation_sbx.value()
        self.scatter_tool.min_rotate_y = self.min_y_rotation_sbx.value()
        self.scatter_tool.min_rotate_z = self.min_z_rotation_sbx.value()
        self.scatter_tool.min_rotate_z = self.min_z_rotation_sbx.value()

    def _create_button_ui(self):
        self.scatter_btn = QtWidgets.QPushButton("Scatter")
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.scatter_btn)
        return layout

    def _create_min_scale_ui(self):
        layout = self._create_modifier_headers()
        self.min_scale_sbx = QtWidgets.QDoubleSpinBox()
        self.min_scale_sbx.setSingleStep(0.1)
        self.min_scale_sbx.\
            setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        self.min_scale_sbx.setFixedWidth(100)
        self.min_scale_sbx.setValue(self.scatter_tool.min_scale)
        layout.addWidget(QtWidgets.QLabel("Minimum Scale:"), 1, 0)
        layout.addWidget(self.min_scale_sbx, 1, 1)
        return layout

    def _create_max_scale_ui(self):
        layout = self._create_min_scale_ui()
        self.max_scale_sbx = QtWidgets.QDoubleSpinBox()
        self.max_scale_sbx.setSingleStep(0.1)
        self.max_scale_sbx. \
            setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        self.max_scale_sbx.setFixedWidth(100)
        self.max_scale_sbx.setValue(self.scatter_tool.max_scale)
        layout.addWidget(QtWidgets.QLabel("Maximum Scale:"), 2, 0)
        layout.addWidget(self.max_scale_sbx, 2, 1)
        return layout

    def _create_min_x_rotation_ui(self):
        layout = QtWidgets.QGridLayout()
        self.min_x_rotation_sbx = QtWidgets.QSpinBox()
        self.min_x_rotation_sbx.\
            setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        self.min_x_rotation_sbx.setFixedWidth(100)
        self.min_x_rotation_sbx.setValue(self.scatter_tool.min_rotate_x)
        layout.addWidget(QtWidgets.QLabel("Minimum X Rotate:"), 5, 0)
        layout.addWidget(self.min_x_rotation_sbx, 5, 1)
        return layout

    def _create_max_x_rotation_ui(self):
        layout = QtWidgets.QGridLayout()
        self.max_x_rotation_sbx = QtWidgets.QSpinBox()
        self.max_x_rotation_sbx. \
            setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        self.max_x_rotation_sbx.setFixedWidth(100)
        self.max_x_rotation_sbx.setValue(self.scatter_tool.max_rotate_x)
        layout.addWidget(QtWidgets.QLabel("Maximum X Rotate:"), 5, 2)
        layout.addWidget(self.max_x_rotation_sbx, 5, 3)
        return layout

    def _create_min_y_rotation_ui(self):
        layout = QtWidgets.QGridLayout()
        self.min_y_rotation_sbx = QtWidgets.QSpinBox()
        self.min_y_rotation_sbx.\
            setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        self.min_y_rotation_sbx.setFixedWidth(100)
        self.min_y_rotation_sbx.setValue(self.scatter_tool.min_rotate_y)
        layout.addWidget(QtWidgets.QLabel("Minimum Y Rotate:"), 6, 0)
        layout.addWidget(self.min_y_rotation_sbx, 6, 1)
        return layout

    def _create_max_y_rotation_ui(self):
        layout = QtWidgets.QGridLayout()
        self.max_y_rotation_sbx = QtWidgets.QSpinBox()
        self.max_y_rotation_sbx. \
            setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        self.max_y_rotation_sbx.setFixedWidth(100)
        self.max_y_rotation_sbx.setValue(self.scatter_tool.max_rotate_y)
        layout.addWidget(QtWidgets.QLabel("Maximum Y Rotate:"), 6, 2)
        layout.addWidget(self.max_y_rotation_sbx, 6, 3)
        return layout

    def _create_min_z_rotation_ui(self):
        layout = QtWidgets.QGridLayout()
        self.min_z_rotation_sbx = QtWidgets.QSpinBox()
        self.min_z_rotation_sbx.\
            setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        self.min_z_rotation_sbx.setFixedWidth(100)
        self.min_z_rotation_sbx.setValue(self.scatter_tool.min_rotate_z)
        layout.addWidget(QtWidgets.QLabel("Minimum Z Rotate:"), 7, 0)
        layout.addWidget(self.min_z_rotation_sbx, 7, 1)
        return layout

    def _create_max_z_rotation_ui(self):
        layout = QtWidgets.QGridLayout()
        self.max_z_rotation_sbx = QtWidgets.QSpinBox()
        self.max_z_rotation_sbx. \
            setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        self.max_z_rotation_sbx.setFixedWidth(100)
        self.max_z_rotation_sbx.setValue(self.scatter_tool.max_rotate_z)
        layout.addWidget(QtWidgets.QLabel("Maximum Z Rotate:"), 7, 2)
        layout.addWidget(self.max_z_rotation_sbx, 7, 3)
        return layout

    def _create_modifier_headers(self):
        self.scale_header_lbl = QtWidgets.QLabel("Random Scale Modifier")
        self.scale_header_lbl.setStyleSheet("font: bold 15px")
        self.rotate_header_lbl = QtWidgets.QLabel("Random Rotation Modifier")
        self.rotate_header_lbl.setStyleSheet("font: bold 15px")
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.scale_header_lbl, 0, 0)
        layout.addWidget(self.rotate_header_lbl, 4, 0)
        return layout


class ScatterTool(object):

    def __init__(self):
        self.max_rotate_z = 0
        self.min_rotate_z = 0
        self.max_rotate_y = 0
        self.min_rotate_y = 0
        self.max_rotate_x = 0
        self.min_rotate_x = 0
        self.min_scale = 1.0
        self.max_scale = 1.0

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

    def random_scale(self, new_instance):
        rand_scale = rand.uniform(self.min_scale, self.max_scale)
        cmds.scale(rand_scale, rand_scale, rand_scale, new_instance,
                   r=True)

    def random_rotation(self, new_instance):
        rand_rotation_x = rand.uniform(self.min_rotate_x, self.max_rotate_x)
        rand_rotation_y = rand.uniform(self.min_rotate_y, self.max_rotate_y)
        rand_rotation_z = rand.uniform(self.min_rotate_z, self.max_rotate_z)
        cmds.rotate(rand_rotation_x, rand_rotation_y, rand_rotation_z,
                    new_instance, r=True)
