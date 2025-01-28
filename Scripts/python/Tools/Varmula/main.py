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
from hutil.Qt import QtCore
from .ui import VarmulaUI

class Varmula(VarmulaUI):
    def __init__(self):
        super().__init__()
        self.setup_window()
        
    def setup_window(self):
        self.setWindowTitle("Varmulas")
        self.setParent(hou.ui.mainQtWindow(), QtCore.Qt.Window)

def run():
    win = Varmula()
    win.show()



