# ----------------------------------------------------------------------------------------
# 3dsmax style renamer
# Author: Maximiliano Rocamora / maxirocamora@gmail.com
# https://github.com/MaxRocamora/MayaRenamer
# ----------------------------------------------------------------------------------------
import os

import maya.cmds as cmds
from PySide6 import QtUiTools, QtWidgets
from PySide6.QtCore import Qt

from renamer import naming
from renamer.css import checkbox_css, css_button, groupbox_css, label_css
from renamer.utils import get_maya_main_window, undo_decorator
from renamer.version import __app__, __qt__

UI_FILE = os.path.join(os.path.dirname(__file__), 'ui', 'main_ui.ui')

DEFAULT_PADDING = 1
DEFAULT_PADDING_ZEROS = 4
DEFAULT_BASENUMBER = 1


class Renamer(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        """Main Renamer Class."""
        parent = parent or get_maya_main_window()
        super().__init__(parent)
        self.base_number = DEFAULT_BASENUMBER
        self.padding_step = DEFAULT_PADDING
        self.padding_zeros = DEFAULT_PADDING_ZEROS
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setObjectName(__qt__)
        self.ui = QtUiTools.QUiLoader().load(UI_FILE, parentWidget=None)
        self.setCentralWidget(self.ui)
        self.setWindowTitle(__app__)
        self.setWindowFlags(Qt.Tool)
        self.move(parent.geometry().center() - self.ui.geometry().center())
        self.set_connections()
        self.show()
        self.reset_ui()

    def set_connections(self):
        """Connections & css."""
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
        """Reset Variables and UI widgets."""
        self.ui.rad_selection.setChecked(True)
        self.ui.line_basenumber.setText(str(DEFAULT_BASENUMBER))
        self.ui.line_padding_step.setText(str(DEFAULT_PADDING))
        self.ui.line_padding_zeros.setText(str(DEFAULT_PADDING_ZEROS))

    # ------------------------------------------------------------------------------------
    # CALLBACK METHODS
    # ------------------------------------------------------------------------------------

    def _read_int(self, line_edit, default: int, minimum: int = None) -> int:
        """Read an int from a line edit, resetting the field if the text is invalid."""
        value = naming.parse_int(line_edit.text(), default, minimum)
        if str(value) != line_edit.text().strip():
            line_edit.setText(str(value))
        return value

    @undo_decorator
    def rename_pressed(self):
        """Rename button callback."""
        self.base_number = self._read_int(self.ui.line_basenumber, DEFAULT_BASENUMBER)
        self.padding_step = self._read_int(self.ui.line_padding_step, DEFAULT_PADDING)
        self.padding_zeros = self._read_int(
            self.ui.line_padding_zeros, DEFAULT_PADDING_ZEROS, minimum=0
        )

        uuids = cmds.ls(sl=True, uuid=True)
        if not uuids:
            self.alert('Nothing Selected!', 'Rename')
            return

        use_basename = self.ui.chk_name.isChecked()
        basename = self.ui.line_name.text()
        if use_basename:
            if not basename:
                self.alert('Enter a basename or disable checkbox!', 'Ops!')
                return
            if naming.is_number(basename):
                self.alert('Your basename must not contain numbers', 'Ops!')
                return

        failed = []
        for uuid in uuids:
            nodes = cmds.ls(uuid, long=True)
            if not nodes:
                continue
            node = nodes[0]

            new_name = basename if use_basename else naming.short_name(node)
            if not use_basename:
                new_name = self.remove_first_digits(new_name)
                new_name = self.remove_last_digits(new_name)
            new_name = self.add_prefix(new_name)
            new_name = self.add_suffix(new_name)

            if self.ui.chk_use_padding.isChecked():
                new_name = naming.add_padding(
                    new_name, self.base_number, self.padding_zeros
                )

            if naming.is_number(new_name):
                print(f'Skipping {node}: the result is a number')
                continue

            try:
                cmds.rename(node, new_name)
            except RuntimeError as error:
                failed.append(f'{naming.short_name(node)}: {error}')
                continue

            self.base_number += self.padding_step

        if failed:
            self.alert('Could not rename:\n' + '\n'.join(failed), 'Rename')

    # ------------------------------------------------------------------------------------
    # RENAME METHODS
    # ------------------------------------------------------------------------------------

    def remove_first_digits(self, name: str) -> str:
        """Remove first characters of the name."""
        if not self.ui.chk_removefirst.isChecked():
            return name
        amount = self._read_int(self.ui.line_removefirst, 0, minimum=0)
        return naming.remove_first(name, amount)

    def remove_last_digits(self, name: str) -> str:
        """Remove last characters of the name."""
        if not self.ui.chk_removelast.isChecked():
            return name
        amount = self._read_int(self.ui.line_removelast, 0, minimum=0)
        return naming.remove_last(name, amount)

    def add_prefix(self, name: str) -> str:
        """Add prefix to the name."""
        if not self.ui.chk_prefix.isChecked():
            return name
        return naming.add_prefix(name, self.ui.line_prefix.text())

    def add_suffix(self, name: str) -> str:
        """Add suffix to the name."""
        if not self.ui.chk_suffix.isChecked():
            return name
        return naming.add_suffix(name, self.ui.line_suffix.text())

    # ------------------------------------------------------------------------------------
    # Replace Methods
    # ------------------------------------------------------------------------------------

    @undo_decorator
    def replace(self):
        """Replace button callback."""
        find_text = self.ui.line_find.text()
        replace_text = self.ui.line_replace.text()
        if not find_text:
            self.alert('Enter the text to find!', 'Replace')
            return

        if self.ui.rad_scene.isChecked():
            nodes = cmds.ls(long=True)
        else:
            nodes = cmds.ls(sl=True, long=True)
        failed = self._find_replace(nodes, find_text, replace_text)
        if failed:
            self.alert('Could not rename:\n' + '\n'.join(failed), 'Replace')

    def _find_replace(self, nodes: list, find_text: str, replace_text: str) -> list:
        """Replace text in node names. Returns descriptions of nodes that failed.

        Nodes are tracked by UUID so renaming a parent does not invalidate its children.
        """
        uuids = [
            uuid
            for node, uuid in zip(nodes, cmds.ls(nodes, uuid=True))
            if find_text in naming.short_name(node)
        ]

        failed = []
        for uuid in uuids:
            current = cmds.ls(uuid, long=True)
            if not current:
                continue
            old_name = naming.short_name(current[0])
            if find_text not in old_name:
                continue
            try:
                cmds.rename(current[0], old_name.replace(find_text, replace_text))
            except RuntimeError as error:
                failed.append(f'{old_name}: {error}')
        return failed

    # ------------------------------------------------------------------------------------
    # UTILITY METHODS
    # ------------------------------------------------------------------------------------

    def alert(self, message: str, title: str):
        """Opens a messagebox UI."""
        msg_box = QtWidgets.QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec()


# ----------------------------------------------------------------------------------------
# MAIN
# ----------------------------------------------------------------------------------------


def load():
    """Load Renamer UI, closing any previous instance."""
    for widget in QtWidgets.QApplication.allWidgets():
        if widget.objectName() == __qt__ and isinstance(widget, QtWidgets.QMainWindow):
            widget.close()
    return Renamer()
