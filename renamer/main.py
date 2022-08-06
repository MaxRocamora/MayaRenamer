# ----------------------------------------------------------------------------------------
# 3dsmax style renamer (2015-2022)
# Author: Maximiliano Rocamora / maxirocamora@gmail.com
# https://github.com/MaxRocamora/MayaRenamer
# ----------------------------------------------------------------------------------------
import os
import maya.cmds as cmds
from PySide2 import QtWidgets
from PySide2.QtCore import Qt
from PySide2 import QtUiTools

from renamer.css import css_button, groupbox_css, checkbox_css, label_css
from renamer.utils import undo_decorator, get_maya_main_window
from renamer.version import __qt__, __app__

ui_path = os.path.dirname(__file__)
ui_file = os.path.join(ui_path, 'ui', 'main_ui.ui')

DEFAULT_PADDING = 1
DEFAULT_PADDING_ZEROS = 4
DEFAULT_BASENUMBER = 1
UNDERSCORE = '_'


class Renamer(QtWidgets.QMainWindow):
    def __init__(self, parent=get_maya_main_window()):
        super().__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setObjectName(__qt__)
        self.ui = QtUiTools.QUiLoader().load(ui_file, parentWidget=None)
        self.setCentralWidget(self.ui)
        self.setWindowTitle(__app__)
        self.setWindowFlags(Qt.Tool)
        self.move(parent.geometry().center() - self.ui.geometry().center())
        self.set_connections()
        self.show()
        self.reset_ui()

    def set_connections(self):
        ''' Connections & css '''
        for widget in self.ui.findChildren(QtWidgets.QCheckBox):
            widget.setStyleSheet(checkbox_css)
        for widget in self.ui.findChildren(QtWidgets.QGroupBox):
            widget.setStyleSheet(groupbox_css)
        for widget in self.ui.findChildren(QtWidgets.QLabel):
            widget.setStyleSheet(label_css)
        css_button(self.ui, self.ui.btn_rename, 'blue')
        self.ui.btn_rename.clicked.connect(self.rename_pressed)
        css_button(self.ui, self.ui.btn_replace, 'blue')
        self.ui.btn_replace.clicked.connect(self.replace)

    def reset_ui(self):
        ''' Reset Variables and UI widgets '''
        self.ui.rad_selection.setChecked(True)
        self.input_basename = ""
        self.padding__basenumber = 1
        self.ui.line_basenumber.setText(str(DEFAULT_BASENUMBER))
        self.padding_step = 1
        self.ui.line_padding_step.setText(str(DEFAULT_PADDING))
        self.padding_zeros = 4
        self.ui.line_padding_zeros.setText(str(DEFAULT_PADDING_ZEROS))

    # ------------------------------------------------------------------------------------
    # CALLBACK METHODS
    # ------------------------------------------------------------------------------------

    @undo_decorator
    def rename_pressed(self):
        ''' rename button callback '''
        # Padding UI
        if not self.is_number(self.ui.line_basenumber.text()):
            self.ui.line_basenumber.setText(str(DEFAULT_BASENUMBER))
        self.padding__basenumber = int(self.ui.line_basenumber.text())

        if not self.is_number(self.ui.line_padding_step.text()):
            self.ui.line_padding_step.setText(str(DEFAULT_PADDING))
        self.padding_step = int(self.ui.line_padding_step.text())

        if not self.is_number(self.ui.line_padding_zeros.text()):
            self.ui.line_padding_zeros.setText(str(DEFAULT_PADDING_ZEROS))
        self.padding_zeros = int(self.ui.line_padding_zeros.text())

        # take selection
        ui_selection = cmds.ls(sl=True, uuid=True)
        if len(ui_selection) < 1:
            self.alert('Nothing Selected!', 'Rename')
            return

        for item in ui_selection:
            obj = cmds.ls(item)
            __name = str(obj[0])

            # string removes
            __name = self.remove_first_digits(__name)
            __name = self.remove_last_digits(__name)

            # set basename
            input_basename = self.ui.line_name.text()
            if self.ui.chk_name.isChecked():
                if not input_basename:
                    self.alert(
                        "Enter a basename or disable checkbox!", "Ops!")
                    return

                if self.is_number(input_basename):
                    self.alert(
                        "Your basename must not contain numbers",
                        "Ops!"
                    )
                    return
                __name = input_basename

            # affixes
            __name = self.add_prefix(__name)
            __name = self.add_suffix(__name)

            # add serializing and padding
            if self.ui.chk_use_padding.isChecked():
                padholder = str(self.padding__basenumber)
                padholder = padholder.zfill(self.padding_zeros)
                __name = __name + UNDERSCORE + padholder

            # rename it!
            if self.is_number(__name):
                print("skipping this item, the result is a number: ", obj)
                continue

            cmds.rename(obj, __name)

            self.padding__basenumber += self.padding_step

    # ------------------------------------------------------------------------------------
    # RENAME METHODS
    # ------------------------------------------------------------------------------------

    def remove_first_digits(self, name):
        ''' remove first digits if you are not setting a base name '''
        if not self.ui.chk_removefirst.isChecked():
            return name

        if self.ui.chk_name.isChecked():
            return name

        if not self.is_number(self.ui.line_removefirst.text()):
            self.ui.line_removefirst.setText('0')

        remove_amount = int(self.ui.line_removefirst.text())
        if remove_amount and len(name) > remove_amount:
            name = name[remove_amount:]
        return name

    def remove_last_digits(self, name):
        ''' remove last digits if you are not setting a base name '''
        if not self.ui.chk_removelast.isChecked():
            return name

        if self.ui.chk_name.isChecked():
            return name

        if not self.is_number(self.ui.line_removelast.text()):
            self.ui.line_removelast.setText('0')

        remove_amount = int(self.ui.line_removelast.text())
        if remove_amount and len(name) > remove_amount:
            name = name[:-remove_amount]
        return name

    def add_prefix(self, name):
        if not self.ui.chk_prefix.isChecked():
            return name

        input_prefix = self.ui.line_prefix.text()
        if not input_prefix:
            return name

        if self.is_number(input_prefix):
            return name

        return input_prefix + UNDERSCORE + name

    def add_suffix(self, name):
        # sourcery skip: assign-if-exp, reintroduce-else, swap-if-expression
        if not self.ui.chk_suffix.isChecked():
            return name

        input_suffix = self.ui.line_suffix.text()
        if not input_suffix:
            return name

        return name + UNDERSCORE + input_suffix

    # ------------------------------------------------------------------------------------
    # Replace Methods
    # ------------------------------------------------------------------------------------

    @undo_decorator
    def replace(self):
        replace_text = str(self.ui.line_find.text())
        with_text = str(self.ui.line_replace.text())

        nodes = cmds.ls() if self.ui.rad_scene.isChecked() else cmds.ls(sl=True)
        self._find_replace(nodes, replace_text, with_text)

    @undo_decorator
    def _find_replace(self, nodes, find_text, replace_text):
        ''' Find and replaces text, get nodes are based
        on scene or maya selection '''
        shapes = cmds.ls(nodes, s=True)
        shape_set = set(shapes)

        new_nodes_names = []
        failed_nodes = []
        for node in nodes:
            if find_text not in node:
                continue
            if node in shape_set:
                continue

            try:
                new_nodes_names.append((node, cmds.rename(node, '__tmp__')))
            except RuntimeError:
                failed_nodes.append(node)

        for shape in shapes:
            if find_text not in shape:
                continue
            if not cmds.objExists(shape):
                try:
                    new_name = cmds.rename(
                        shape, shape.replace(find_text, '__tmp__'))
                    new_nodes_names.append((shape, new_name))
                except RuntimeError:
                    failed_nodes.append(node)

        new_names = []
        for name, new_node in new_nodes_names:
            new_name = name.replace(find_text, replace_text)
            new_names.append(cmds.rename(new_node, new_name))

        return new_names

    # ------------------------------------------------------------------------------------
    # UTILITY METHODS
    # ------------------------------------------------------------------------------------

    def is_number(self, s):
        """ check if a string is a number """
        try:
            int(s)
            return True
        except ValueError:
            return False

    def alert(self, msg, title):
        """ Opens a messagebox UI
            msg: string.
            title: string.
        """
        msgBox = QtWidgets.QMessageBox(self)
        msgBox.setWindowTitle(title)
        msgBox.setText(msg)
        msgBox.exec_()

# ----------------------------------------------------------------------------------------
# MAIN
# ----------------------------------------------------------------------------------------


def load():
    if cmds.window(__qt__, q=1, ex=1):
        cmds.deleteUI(__qt__)
    Renamer()
