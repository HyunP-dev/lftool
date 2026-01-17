from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from lftool.model import AccessLogModel
from lftool.parser.nginxparser import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(1200, 720)

        splitter = QSplitter()

        self.log_view = QTreeView()
        self.log_view.setEditTriggers(QTreeView.EditTrigger.NoEditTriggers)
        self.log_view.setRootIsDecorated(False)
        self.log_view.setUniformRowHeights(True)

        splitter.addWidget(side_view := QTreeView())
        splitter.addWidget(self.log_view)
        splitter.setSizes([200, 1200])
        self.side_view = side_view

        self.log_view.setModel(log_model := AccessLogModel(self))
        log_model.open()

        side_view.setModel(side_model := QStandardItemModel())
        side_view.setEditTriggers(QTreeView.EditTrigger.NoEditTriggers)
        side_view.setHeaderHidden(True)

        self.log_model = log_model
        self.side_model = side_model

        self.setCentralWidget(self.log_view)  # TODO: let this better.
