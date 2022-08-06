import maya.cmds as cmds
from PySide2 import QtWidgets
from maya import OpenMayaUI as omui
from shiboken2 import wrapInstance


def undo_decorator(func):
    ''' maya undo decorator '''
    def wrapper(*args, **kwargs):
        cmds.undoInfo(openChunk=True)
        try:
            ret = func(*args, **kwargs)
        finally:
            cmds.undoInfo(closeChunk=True)
        return ret
    return wrapper


def get_maya_main_window():
    ''' returns maya main window '''
    return wrapInstance(int(omui.MQtUtil.mainWindow()), QtWidgets.QWidget)
