"""
        @file           utils.py

        @author         Syahdan Micoy Nazera
        
        @since          2025-01-15
        @lastupdate     2025-13-05

        @brief          Utility functions for Houdini
        @dependencies   Python 3.10, hou
        @version        1.0.0
        @todos          Add more utility functions
"""

import os
import traceback
from PySide2.QtWidgets import QWidget
from PySide2.QtCore import QFile, QTextStream

import hou

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
    
class LogUtils:
    """Utility class for logging. """
    @staticmethod
    def log_error(message):
        """Log an error message."""
        print(f"ERROR: {message}")

    @staticmethod
    def log_warning(message):
        """Log a warning message."""
        print(f"WARNING: {message}")

    @staticmethod
    def log_info(message):
        """Log an info message."""
        print(f"INFO: {message}")

    @staticmethod
    def log_env_variables():
        """Log environment variables."""
        env_vars = os.environ
        for key, value in env_vars.items():
            print(f"{key} : {value}")
    