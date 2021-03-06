# -*- coding: utf-8 -*-
"""
This module contains some dialogs.
"""
import sys
import logging

from PyQt5.QtGui import QIcon, QPixmap, QFontMetrics
from PyQt5.QtCore import Qt, QSize, pyqtSlot
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QDesktopWidget,
    QTextEdit,
    QProgressBar,
    QPushButton,
    QApplication,
    QGridLayout,
    QMessageBox,
    QDialogButtonBox,
    QComboBox,
    QSizePolicy,
)

import venvipy_rc  # pylint: disable=unused-import
from get_data import __version__


logger = logging.getLogger(__name__)



#]===========================================================================[#
#] PROGRESS BAR DIALOG [#====================================================[#
#]===========================================================================[#

class ProgBarDialog(QDialog):
    """
    Dialog showing a progress bar during the create process.
    """
    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):
        self.setFixedSize(350, 85)
        self.center()
        self.setWindowIcon(QIcon(":/img/profile.png"))
        self.setWindowFlag(Qt.WindowCloseButtonHint, False)
        self.setWindowFlag(Qt.WindowMinimizeButtonHint, False)

        self.status_label = QLabel(self)
        self.place_holder = QLabel(self)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setFixedSize(325, 23)
        self.progress_bar.setRange(0, 0)

        v_layout = QVBoxLayout()
        v_layout.addWidget(self.status_label)
        v_layout.addWidget(self.progress_bar)
        v_layout.addWidget(self.place_holder)

        h_layout = QHBoxLayout(self)
        h_layout.setContentsMargins(0, 15, 0, 0)
        h_layout.addLayout(v_layout)

        self.setLayout(h_layout)


    def center(self):
        """Center window."""
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())



#]===========================================================================[#
#] CONSOLE DIALOG [#=========================================================[#
#]===========================================================================[#

class ConsoleDialog(QDialog):
    """
    Dialog box printing the output to a console-like widget during the
    installation process.
    """
    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):
        self.resize(880, 510)
        self.center()
        self.setWindowIcon(QIcon(":/img/profile.png"))
        self.setWindowFlag(Qt.WindowCloseButtonHint, False)
        self.setWindowFlag(Qt.WindowMinimizeButtonHint, False)

        self.setStyleSheet(
            """
            QTextEdit {
                background-color: black;
                color: lightgrey;
                selection-background-color: rgb(50, 50, 60);
                selection-color: rgb(0, 255, 0)
            }
            """
        )

        self.console_window = QTextEdit()
        self.console_window.setReadOnly(True)
        self.console_window.setFontFamily("Monospace")
        self.console_window.setFontPointSize(11)

        v_layout = QVBoxLayout(self)
        v_layout.addWidget(self.console_window)


    def center(self):
        """Center window."""
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


    @pyqtSlot(str)
    def update_status(self, message):
        """
        Print the output from stdin/ stderr to `console_window`.
        """
        metrix = QFontMetrics(self.console_window.font())
        formatted_text = metrix.elidedText(
            message, Qt.ElideNone, self.console_window.width()
        )
        self.console_window.append(formatted_text)

    def append(self, message):
        """
        Print the output from stdin/ stderr to `console_window`.
        """
        # metrix = QFontMetrics(self.console_window.font())
        # formatted_text = metrix.elidedText(
        #     message, Qt.ElideNone, self.console_window.width()
        # )
        formatted_text = message
        self.console_window.append(formatted_text)

    def finish_fail(self):
        """
        Show info message when the installation process failed.
        """
        message_txt = (
            "Could not install from requirements.\n\n"
            "File not found.\n"
        )
        logger.error("Could not install from requirements")
        QMessageBox.critical(self, "Error", message_txt)



#]===========================================================================[#
#] APPLICATION INFO DIALOG [#================================================[#
#]===========================================================================[#

class InfoAboutVenviPy(QDialog):
    """
    The "Info about VenviPy" dialog.
    """
    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):
        self.setWindowTitle("About VenviPy")
        self.setFixedSize(420, 350)
        self.center()
        self.setWindowIcon(QIcon(":/img/profile.png"))
        self.setWindowFlag(Qt.WindowMinimizeButtonHint, False)

        # logo
        logo = QLabel()
        pixmap = QPixmap(":/img/default.png")
        logo_scaled = pixmap.scaled(136, 136, Qt.KeepAspectRatio)
        logo.setPixmap(logo_scaled)

        place_holder = QLabel(maximumHeight=1)

        # title
        title_label = QLabel(
            '<p><span style="font-size:12pt;">\
                <b>VenviPy</b>\
            </span></p>'
        )
        #title_label.setFont(QFont("FreeSerif", italic=True))

        # version
        version_label = QLabel(
            f'<p><span style="font-size:11pt;">\
                {__version__}\
            </span></p>'
        )

        # subtitle
        subtitle_label = QLabel(
            '<p><span style="font-size:11pt;">\
                Virtual Environment Manager for Python\
            </span></p>'
        )

        repo_label = QLabel(
            '<p><span style="font-size:11pt;">\
            <a href="https://github.com/sinusphi/venvipy">\
                Website\
            </a></span></p>',
            openExternalLinks=True
        )

        # copyright
        copyright_label = QLabel(
            '<p><span style="font-size:10pt;">\
                Copyright © 2019-2020 Youssef Serestou\
            </span></p>\
            <p><span style="font-size:10pt;">\
                Windows Port, Oct 2020, by E.R. Uber\
            </span></p>'
        )

        # close button
        close_button = QPushButton("Close", clicked=self.close)
        close_button.setMinimumSize(QSize(110, 15))


        grid_layout = QGridLayout(self)
        grid_layout.setContentsMargins(15, 15, 10, 15)

        grid_layout.addWidget(logo, 0, 0, Qt.AlignHCenter)
        grid_layout.addWidget(place_holder, 1, 0, Qt.AlignHCenter)
        grid_layout.addWidget(title_label, 2, 0, Qt.AlignHCenter)
        grid_layout.addWidget(version_label, 3, 0, Qt.AlignHCenter)
        grid_layout.addWidget(subtitle_label, 4, 0, Qt.AlignHCenter)
        grid_layout.addWidget(repo_label, 5, 0, Qt.AlignHCenter)
        grid_layout.addWidget(copyright_label, 6, 0, Qt.AlignHCenter)
        grid_layout.addWidget(close_button, 7, 0, Qt.AlignRight)
        self.setLayout(grid_layout)


    def center(self):
        """Center window."""
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

#]===========================================================================[#
#] LOGGING LEVEL DIALOG [#===================================================[#
#]===========================================================================[#
class LoggingLevelDialog(QDialog):
    
    level_names = list()

    def __init__(self, parent=None, level_limit=100, icon=None):
        """
        A simple dialog that allows user to select a logging level.

        Parameters
        ----------
        parent : QWidget, optional
            This dialog's parent widget, if any
        level_limit : int, optional
            The number of logging levels to search for logging level names.
            The default value finds all the standard Python logging levels
            and supports discovering custom logging levels within the first
            100 logging levels. Change this limit if your application defines
            logging levels above 100.
        icon : str, optional
            Provide a path to an icon image to change this dialog's icon.
        """
        super(LoggingLevelDialog, self).__init__(parent)

        self.level_limit = level_limit
        self.icon = icon

        self.initUI()

    def initUI(self):
        self.setWindowTitle(f"Set Logging Level")
        self.setFixedSize(250, 150)
        self.center()
        if self.icon:
            self.setWindowIcon(QIcon(self.icon))
        self.setWindowFlag(Qt.WindowMinimizeButtonHint, False)
        self.setWindowFlag(Qt.WindowSystemMenuHint, True)
        self.setWindowFlag(Qt.WindowTitleHint, True)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        if not len(self.level_names) > 0:
            for i in range(self.level_limit):
                if not logging.getLevelName(i).startswith('Level'):
                    self.level_names.append((logging.getLevelName(i), i))

        # self.level_names if no custom levels added
        # [('NOTSET', 0), ('DEBUG', 10), ('INFO', 20), ('WARNING', 30), ('ERROR', 40), ('CRITICAL', 50)]

        self.buttonBox = QDialogButtonBox(QBtn)
        
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.vlayout = QVBoxLayout()

        self.combobox = QComboBox()

        for level_name, level_number in self.level_names:
            self.combobox.addItem(level_name)

        self.combobox.currentIndexChanged.connect(self.updatelogginglevel)

        self.vlayout.addWidget(self.combobox)
        self.vlayout.addWidget(self.buttonBox)
        self.setLayout(self.vlayout)

    def center(self):
        """Center Dialog."""
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def updatelogginglevel(self, i):
        self.level = self.combobox.currentText()

#]===========================================================================[#
#] Projects List DIALOG [#===================================================[#
#]===========================================================================[#
class ProjectsDialog(QDialog):
    def __init__(self, venv, parent=None,):
        super(ProjectsDialog, self).__init__(parent)

        self.venv = venv

        self.initUI()

    def initUI(self):

        self.setWindowTitle(f"Dev Projects that reference venv {self.venv}")
        self.setFixedSize(880, 510)
        self.center()
        self.setWindowIcon(QIcon(":/img/profile.png"))
        self.setWindowFlag(Qt.WindowCloseButtonHint, False)
        self.setWindowFlag(Qt.WindowMinimizeButtonHint, False)
        self.setWindowFlag(Qt.WindowMinimizeButtonHint, False)
        self.setWindowFlag(Qt.WindowSystemMenuHint, True)
        self.setWindowFlag(Qt.WindowTitleHint, True)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)

        self.setStyleSheet(
            """
            QTextEdit {
                background-color: black;
                color: lightgrey;
                selection-background-color: rgb(50, 50, 60);
                selection-color: rgb(0, 255, 0)
            }
            """
        )

        self.projects_list = QTextEdit()
        self.projects_list.setReadOnly(True)
        self.projects_list.setFontFamily("Monospace")
        self.projects_list.setFontPointSize(11)

        self.close = QPushButton('Close', self)
        #sizePolicy = QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        # sizePolicy.setHorizontalStretch(1)
        # sizePolicy.setVerticalStretch(1)
        #self.close.setSizePolicy(sizePolicy)
        self.close.setToolTip("Close this dialog...")
        self.close.clicked.connect(self.close_clicked)

        v_layout = QVBoxLayout(self)
        v_layout.addWidget(self.projects_list)
        v_layout.addWidget(self.close)

    def center(self):
        """Center Dialog."""
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def update(self, text):
        self.projects_list.append(text)

    def close_clicked(self):
        self.accept()



if __name__ == "__main__":

    app = QApplication(sys.argv)

    #progress_dialog = ProgBarDialog()
    #progress_dialog.show()

    #console_dialog = ConsoleDialog()
    #console_dialog.show()

    info_about_venvipy = InfoAboutVenviPy()
    info_about_venvipy.show()

    sys.exit(app.exec_())
