"""
        @since          2025-28-01
        @lastupdate     2025-28-01

        @author         Syahdan Micoy Nazera (shdnea@gmail.com)

        @brief          Tool for Establishing Projects, Assets, 
                        and Shots in Houdini.
        @dependencies   Python 3.10, hou
        @version        1.0.0
        @todos          
"""

import hou
from hutil.Qt import QtCore, QtGui

from .ui import VarmulaUI
from Utility.utils import WidgetUtils

from .constant import (
    WINDOW_ICON,
    INIT_ICON
)

class Varmula(VarmulaUI):
    def __init__(self):
        super().__init__()
        self.setup_window()
        self.apply_stylesheet()

    def setup_window(self):
        self.setWindowTitle("Varmulas")
        self.setParent(hou.ui.mainQtWindow(), QtCore.Qt.Window)

        # Icon
        self.setWindowIcon(QtGui.QIcon(WINDOW_ICON))
        self.push_button.setIcon(QtGui.QIcon(INIT_ICON))

    def apply_stylesheet(self):
        style = WidgetUtils.koodeta_stylesheet()
        with open(style, "r") as file:
            style = file.read()
        self.setStyleSheet(style)


def run():
    win = Varmula()
    win.show()



