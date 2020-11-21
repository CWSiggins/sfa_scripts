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
        self.scatter_tool = ScatterTool()
        self.open_tool_window()

    def open_tool_window(self):
        if len(self.scatter_tool.selection) == 2:
            super(ScatterToolUI, self).__init__(parent=maya_main_window())
            self.setWindowTitle("Scatter Tool")
            # self.setMinimumWidth(500)
            # self.setMaximumHeight(200)
            self.create_ui()
            self.create_connections()
        else:
            super(ScatterToolUI, self).__init__(parent=maya_main_window())
            self.setWindowTitle("Please Select Only Two Objects to Use This "
                                "Tool")
            self.setMinimumWidth(500)
            self.setMaximumHeight(200)

    def create_ui(self):
        self.title_lbl = QtWidgets.QLabel("Scatter Objects")
        self.title_lbl.setStyleSheet("font: bold 20px")
        self.selection_lay = self._object_selection()
        self._create_modifier_headers_lay = self._create_modifier_headers()
        self.button_lay = self._create_button_ui()
        self.set_layout()

    def set_layout(self):
        self.main_lay = QtWidgets.QVBoxLayout()
        self.main_lay.addWidget(self.title_lbl)
        self.main_lay.addLayout(self.selection_lay)
        self.main_lay.addLayout(self._create_modifier_headers_lay)
        self.main_lay.addLayout(self.button_lay)
        self.setLayout(self.main_lay)

    def create_connections(self):
        """Connect Signals and Slots"""
        self.scatter_btn.clicked.connect(self._scatter)
        self.selection_btn.clicked.connect(self._add_selection)
        self.swap_btn.clicked.connect(self._swap_selection)

    @QtCore.Slot()
    def _object_selection(self):
        self.object_to_scatter_with_lbl = QtWidgets. \
            QLabel("Object to Scatter With:")
        self.object_to_scatter_to_lbl = QtWidgets. \
            QLabel("Object to Scatter To:")
        self.object_to_scatter_with_lbl.setMinimumWidth(100)
        self.object_to_scatter_to_lbl.setMinimumWidth(100)
        self.selection_btn = QtWidgets.QPushButton("Add Selection")
        self.swap_btn = QtWidgets.QPushButton("Swap Selection")
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.object_to_scatter_with_lbl, 0, 0)
        layout.addWidget(self.object_to_scatter_to_lbl, 0, 1)
        layout.addWidget(self.selection_btn, 1, 0)
        layout.addWidget(self.swap_btn, 1, 1)
        return layout

    @QtCore.Slot()
    def _add_selection(self):
        """Add current selections to tool"""
        self.object_to_scatter_with = self.scatter_tool.selection[0]
        current_object_to_scatter_with = "Object to Scatter With: " \
                                         + str(self.object_to_scatter_with)
        self.object_to_scatter_with_lbl.setText(current_object_to_scatter_with)
        self.object_to_scatter_to = self.scatter_tool.selection[1]
        current_object_to_scatter_to = "Object to Scatter To: " \
                                       + str(self.object_to_scatter_to)
        self.object_to_scatter_to_lbl.setText(current_object_to_scatter_to)

    @QtCore.Slot()
    def _swap_selection(self):
        """Swap current selection"""
        self.scatter_tool.selection.insert(0,
                                           self.scatter_tool.selection.pop())
        self.object_to_scatter_with = self.scatter_tool.selection[0]
        current_object_to_scatter_with = "Object to Scatter With: " \
                                         + str(self.object_to_scatter_with)
        self.object_to_scatter_with_lbl.setText(current_object_to_scatter_with)
        self.object_to_scatter_to = self.scatter_tool.selection[1]
        current_object_to_scatter_to = "Object to Scatter To: " \
                                       + str(self.object_to_scatter_to)
        self.object_to_scatter_to_lbl.setText(current_object_to_scatter_to)

    @QtCore.Slot()
    def _scatter(self):
        """Scatter objects"""
        self._set_scatter_properties_from_ui()
        self.scatter_tool.scatter()

    def _set_scatter_properties_from_ui(self):
        self.scatter_tool = ScatterTool()
        self.scatter_tool.selection[0] = self.object_to_scatter_with
        self.scatter_tool.selection[1] = self.object_to_scatter_to
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

    def _create_modifier_headers(self):
        self.scale_header_lbl = QtWidgets.QLabel("Random Scale Modifier")
        self.scale_header_lbl.setStyleSheet("font: bold 15px")
        self.rotate_header_lbl = QtWidgets.QLabel("Random Rotation "
                                                  "Modifier")
        self.rotate_header_lbl.setStyleSheet("font: bold 15px")
        self.misc_header_lbl = QtWidgets.QLabel("Miscellaneous Modifiers")
        self.misc_header_lbl.setStyleSheet("font: bold 15px")
        return self._create_modifiers_layout()

    def _create_modifiers_layout(self):
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.scale_header_lbl, 2, 0, 1, 4)
        layout.addWidget(self.rotate_header_lbl, 4, 0, 1, 4)
        layout.addWidget(self.misc_header_lbl, 8, 0, 1, 4)
        self._create_min_scale_ui(layout)
        self._create_max_scale_ui(layout)
        self._create_min_x_rotation_ui(layout)
        self._create_max_x_rotation_ui(layout)
        self._create_min_y_rotation_ui(layout)
        self._create_max_y_rotation_ui(layout)
        self._create_min_z_rotation_ui(layout)
        self._create_max_z_rotation_ui(layout)
        return layout

    def _create_max_z_rotation_ui(self, layout):
        self.max_z_rotation_sbx = QtWidgets.QSpinBox()
        self.max_z_rotation_sbx. \
            setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        self.max_z_rotation_sbx.setFixedWidth(100)
        self.max_z_rotation_sbx.setMaximum(360)
        self.max_z_rotation_sbx.setMinimum(-360)
        self.max_z_rotation_sbx.setValue(self.scatter_tool.max_rotate_z)
        layout.addWidget(QtWidgets.QLabel("Maximum Z Rotate:"), 7, 2, 1, 1)
        layout.addWidget(self.max_z_rotation_sbx, 7, 3, 1, 1)

    def _create_min_z_rotation_ui(self, layout):
        self.min_z_rotation_sbx = QtWidgets.QSpinBox()
        self.min_z_rotation_sbx. \
            setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        self.min_z_rotation_sbx.setFixedWidth(100)
        self.min_z_rotation_sbx.setMaximum(360)
        self.min_z_rotation_sbx.setMinimum(-360)
        self.min_z_rotation_sbx.setValue(self.scatter_tool.min_rotate_z)
        layout.addWidget(QtWidgets.QLabel("Minimum Z Rotate:"), 7, 0, 1, 1)
        layout.addWidget(self.min_z_rotation_sbx, 7, 1, 1, 1)

    def _create_max_y_rotation_ui(self, layout):
        self.max_y_rotation_sbx = QtWidgets.QSpinBox()
        self.max_y_rotation_sbx. \
            setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        self.max_y_rotation_sbx.setFixedWidth(100)
        self.max_y_rotation_sbx.setMaximum(360)
        self.max_y_rotation_sbx.setMinimum(-360)
        self.max_y_rotation_sbx.setValue(self.scatter_tool.max_rotate_y)
        layout.addWidget(QtWidgets.QLabel("Maximum Y Rotate:"), 6, 2, 1, 1)
        layout.addWidget(self.max_y_rotation_sbx, 6, 3, 1, 1)

    def _create_min_y_rotation_ui(self, layout):
        self.min_y_rotation_sbx = QtWidgets.QSpinBox()
        self.min_y_rotation_sbx. \
            setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        self.min_y_rotation_sbx.setFixedWidth(100)
        self.min_y_rotation_sbx.setMaximum(360)
        self.min_y_rotation_sbx.setMinimum(-360)
        self.min_y_rotation_sbx.setValue(self.scatter_tool.min_rotate_y)
        layout.addWidget(QtWidgets.QLabel("Minimum Y Rotate:"), 6, 0, 1, 1)
        layout.addWidget(self.min_y_rotation_sbx, 6, 1, 1, 1)

    def _create_max_x_rotation_ui(self, layout):
        self.max_x_rotation_sbx = QtWidgets.QSpinBox()
        self.max_x_rotation_sbx.setMaximum(360)
        self.max_x_rotation_sbx.setMinimum(-360)
        self.max_x_rotation_sbx. \
            setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        self.max_x_rotation_sbx.setFixedWidth(100)
        self.max_x_rotation_sbx.setValue(self.scatter_tool.max_rotate_x)
        layout.addWidget(QtWidgets.QLabel("Maximum X Rotate:"), 5, 2, 1, 1)
        layout.addWidget(self.max_x_rotation_sbx, 5, 3, 1, 1)

    def _create_min_x_rotation_ui(self, layout):
        self.min_x_rotation_sbx = QtWidgets.QSpinBox()
        self.min_x_rotation_sbx.setMaximum(360)
        self.min_x_rotation_sbx.setMinimum(-360)
        self.min_x_rotation_sbx. \
            setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        self.min_x_rotation_sbx.setFixedWidth(100)
        self.min_x_rotation_sbx.setValue(self.scatter_tool.min_rotate_x)
        layout.addWidget(QtWidgets.QLabel("Minimum X Rotate:"), 5, 0, 1, 1)
        layout.addWidget(self.min_x_rotation_sbx, 5, 1, 1, 1)

    def _create_max_scale_ui(self, layout):
        self.max_scale_sbx = QtWidgets.QDoubleSpinBox()
        self.max_scale_sbx.setSingleStep(0.1)
        self.max_scale_sbx. \
            setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        self.max_scale_sbx.setFixedWidth(100)
        self.max_scale_sbx.setValue(self.scatter_tool.max_scale)
        layout.addWidget(QtWidgets.QLabel("Maximum Scale:"), 3, 2, 1, 1)
        layout.addWidget(self.max_scale_sbx, 3, 3, 1, 1)

    def _create_min_scale_ui(self, layout):
        self.min_scale_sbx = QtWidgets.QDoubleSpinBox()
        self.min_scale_sbx.setSingleStep(0.1)
        self.min_scale_sbx. \
            setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        self.min_scale_sbx.setFixedWidth(100)
        self.min_scale_sbx.setValue(self.scatter_tool.min_scale)
        layout.addWidget(QtWidgets.QLabel("Minimum Scale:"), 3, 0, 1, 1)
        layout.addWidget(self.min_scale_sbx, 3, 1, 1, 1)


class ScatterTool(object):

    def __init__(self):
        self.selection = cmds.ls(os=True, fl=True)
        self.max_rotate_z = 0
        self.min_rotate_z = 0
        self.max_rotate_y = 0
        self.min_rotate_y = 0
        self.max_rotate_x = 0
        self.min_rotate_x = 0
        self.min_scale = 1.0
        self.max_scale = 1.0
        self.align = False
        self.undo = False

    def scatter(self):
        """Scatter object along the vertices of another object"""
        vertex_list = cmds.ls(str(self.selection[1]) + '.vtx[*]', fl=True)
        object_to_instance = self.selection[0]
        if cmds.objectType(object_to_instance) == 'transform':
            for vertex in vertex_list:
                new_instance = cmds.instance(object_to_instance)
                position = cmds.pointPosition(vertex, w=True)
                pmc.move(position[0], position[1], position[2], new_instance,
                         a=True, ws=True)
                if self.align is True:
                    self.align_to_faces(new_instance, vertex)
                self.random_rotation(new_instance)
                self.random_scale(new_instance)
                if self.undo is True:
                    cmds.delete(new_instance)
        else:
            print("Please ensure the object you select is a transform")

    @staticmethod
    def align_to_faces(new_instance, vertex):
        faces = cmds.polyListComponentConversion(vertex, fromVertex=True,
                                                 toFace=True)
        faces = cmds.filterExpand(faces, selectionMask=34,
                                  expand=True)
        ave_vtx_normal, tangent, tangent2 = ScatterTool.find_average_normal(
            faces)
        pos = cmds.xform(vertex, query=True, worldSpace=True,
                         translation=True)
        matrix = [tangent2.x, tangent2.y, tangent2.z, 0.0,
                  ave_vtx_normal.x, ave_vtx_normal.y,
                  ave_vtx_normal.z, 0.0,
                  tangent.x, tangent.y, tangent.z, 0.0,
                  pos[0], pos[1], pos[2], 1.0]
        cmds.xform(new_instance, worldSpace=True, matrix=matrix)

    @staticmethod
    def find_average_normal(faces):
        face_normals = []
        for face in faces:
            mesh_face = pmc.MeshFace(face)
            face_normals.append(mesh_face.getNormal())
        sum_of_normals = sum(face_normals)
        ave_vtx_normal = sum_of_normals / len(sum_of_normals)
        ave_vtx_normal.normalize()
        tangent = ave_vtx_normal.cross(pmc.dt.Vector(0, 1, 0))
        tangent.normalize()
        tangent2 = ave_vtx_normal.cross(tangent)
        tangent2.normalize()
        return ave_vtx_normal, tangent, tangent2

    def random_scale(self, new_instance):
        rand_scale = rand.uniform(self.min_scale, self.max_scale)
        cmds.scale(rand_scale, rand_scale, rand_scale, new_instance,
                   r=True)

    def random_rotation(self, new_instance):
        rand_rotation_x = \
            rand.uniform(self.min_rotate_x, self.max_rotate_x)
        rand_rotation_y = \
            rand.uniform(self.min_rotate_y, self.max_rotate_y)
        rand_rotation_z = \
            rand.uniform(self.min_rotate_z, self.max_rotate_z)
        cmds.rotate(rand_rotation_x, rand_rotation_y, rand_rotation_z,
                    new_instance, r=True)
