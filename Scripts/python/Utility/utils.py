"""
        @file       utils.py
        @author     Syahdan Micoy Nazera
        @since      2025-01-15

        @brief     -
"""


"""
TODO : Add more utility functions
"""

import os
import traceback
from PySide2.QtWidgets import QWidget
from PySide2.QtCore import QFile, QTextStream


class WidgetUtils:
    """Utility class for widgets."""

    @staticmethod
    def koodeta_stylesheet():
        """Load and apply QSS file."""

        cwd = FileUtils.q_script_folder()
        file_name = "stylesheet.qss"
        style = f"{cwd}/{file_name}"
        return style

class FileUtils:
    """Utility class for file operations."""

    def q_working_directory():
        """Get the current working directory."""
        return os.getcwd()

    def q_script_file():
        """Get the current file path."""
        return os.path.abspath(__file__)
    
    def q_script_folder():
        """Get the folder of the current script."""
        return os.path.dirname(os.path.abspath(__file__))