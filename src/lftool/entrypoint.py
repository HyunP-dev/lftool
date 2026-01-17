from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from lftool.view import MainWindow


def main():
    app = QApplication()
    window = MainWindow()
    window.showMaximized()
    app.exec()
