import functools

import maya.cmds as cmds
from maya import OpenMayaUI as omui

from PySide6 import QtWidgets
from shiboken6 import wrapInstance


def undo_decorator(func):
    """Maya undo decorator."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        cmds.undoInfo(openChunk=True)
        try:
            ret = func(*args, **kwargs)
        finally:
            cmds.undoInfo(closeChunk=True)
        return ret

    return wrapper


def get_maya_main_window():
    """Returns maya main window."""
    return wrapInstance(int(omui.MQtUtil.mainWindow()), QtWidgets.QWidget)
