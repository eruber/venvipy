# -*- coding: utf-8 -*-
"""Set the default venv directory."""
import os

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication, QAction, QVBoxLayout, QHBoxLayout,
                             QToolButton, QPushButton, QSpacerItem, QDialog,
                             QFrame, QSizePolicy, QGridLayout, QLineEdit,
                             QLabel, QFileDialog)




class SelectDefaultDir(QDialog):
    """
    Set the default directory, where to look for virtual environments.
    """

    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):

        self.setWindowTitle("Set Default Directory")
        self.setGeometry(600, 365, 500, 100)
        self.setFixedSize(500, 100)

        self.setStyleSheet(
            """
            QToolTip {
                background-color: rgb(47, 52, 63);
                border: rgb(47, 52, 63);
                color: rgb(210, 210, 210);
                padding: 1px;
                opacity: 325
            }
            """
        )

        v_Layout = QVBoxLayout(self)
        h_Layout = QHBoxLayout()
        gridLayout = QGridLayout()

        defaultDirLabel = QLabel("Default Venv Directory:")
        self.defaultDirLineEdit = QLineEdit()
        defaultDirLabel.setBuddy(self.defaultDirLineEdit)

        folder_icon = QIcon.fromTheme("folder")

        browseToolButton = QToolButton(
            toolTip="Browse",
            icon=folder_icon,
            clicked=self.select_dir
        )
        browseToolButton.setFixedSize(26, 27)

        horizontalLine = QFrame(
            frameShape=QtWidgets.QFrame.HLine,
            frameShadow=QtWidgets.QFrame.Sunken
        )

        cancelButton = QPushButton(
            "Cancel", clicked=self.reject
        )

        okButton = QPushButton(
            "OK", clicked=self.okButton_clicked
        )

        spacerItem = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum
        )

        gridLayout.addWidget(defaultDirLabel, 0, 0, 1, 1)
        gridLayout.addWidget(self.defaultDirLineEdit, 0, 1, 1, 1)
        gridLayout.addWidget(browseToolButton, 0, 2, 1, 1)

        h_Layout.addItem(spacerItem)
        h_Layout.addWidget(okButton, 0, Qt.AlignBottom)
        h_Layout.addWidget(cancelButton, 0, Qt.AlignBottom)

        v_Layout.addLayout(gridLayout)
        v_Layout.addWidget(horizontalLine)
        v_Layout.addLayout(h_Layout)


    def select_dir(self):
        """
        Select directory which should be set as default.
        """
        directory = QFileDialog.getExistingDirectory()
        self.defaultDirLineEdit.setText(directory)


    def okButton_clicked(self):
        """
        Store the absolute path to the selected dir in `recources/default`.
        """
        current_dir = os.path.dirname(os.path.realpath(__file__))
        default_file = os.path.join(current_dir, "resources", "default")
        default_path = self.defaultDirLineEdit.text()

        with open(default_file, "w") as f:
            f.write(default_path)
            print(
                f"[INFO]: Setting default venv directory to '{default_path}'"
            )

        self.accept()




if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    settingsUI = SelectDefaultDir()
    settingsUI.show()

    sys.exit(app.exec_())
