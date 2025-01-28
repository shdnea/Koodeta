"""
        @since          2025-28-01
        @lastupdate     2025-28-01

        @author         Syahdan Micoy Nazera (shdnea@gmail.com)

        @brief          Varmula UI Module
        @dependencies   Python 3.10, hutil.Qt
        @version        1.0.0
"""

from hutil.Qt import QtCore, QtWidgets


class VarmulaUI(QtWidgets.QWidget):
    def __init__(self):
        super(VarmulaUI, self).__init__()
        main_layout = QtWidgets.QVBoxLayout(self)

        self.group_box = QtWidgets.QGroupBox("Project Name :")
        group_layout = QtWidgets.QVBoxLayout(self.group_box)

        self.line_edit = QtWidgets.QLineEdit("Koodeta")
        self.line_edit.setAlignment(QtCore.Qt.AlignCenter)
        self.line_edit.setFixedSize(435, 50)
        group_layout.addWidget(self.line_edit)

        self.label = QtWidgets.QLabel("Project Variant :")
        self.combo_box = QtWidgets.QComboBox()
        self.combo_box.addItems(["Personal", "Global"])

        form_layout = QtWidgets.QHBoxLayout()
        form_layout.addWidget(self.label)
        form_layout.addWidget(self.combo_box)

        self.push_button = QtWidgets.QPushButton("Initialize")
        self.push_button.setFixedHeight(30)

        main_layout.addWidget(self.group_box)
        main_layout.addLayout(form_layout)
        main_layout.addWidget(self.push_button)

        self.setLayout(main_layout)
        self.setFixedSize(480, 230)

        # Center Window
        screen_geometry = QtWidgets.QDesktopWidget().availableGeometry()  
        window_geometry = self.geometry()
        center_position = (screen_geometry.center() - window_geometry.center())  
        self.move(center_position)