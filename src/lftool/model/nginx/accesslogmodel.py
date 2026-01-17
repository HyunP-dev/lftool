from functools import cache

from joblib import Parallel, delayed
from PySide6.QtCore import *
from PySide6.QtGui import QIcon
from tqdm import tqdm

from lftool.parser.nginxparser import *
from lftool.toolkit.ipv4band import IPv4RBand


@cache
def get_country_icon(country: str):
    return QIcon(f"./assets/images/flags/4x3/{country.lower()}.svg")


class AccessLogModel(QAbstractTableModel):
    def __init__(self, parent):
        super().__init__(parent)
        self.logs: list[NGINXAccessLog] = []
        self.addresses = set()

    def open(self, path: str = "/usr/local/var/log/nginx/access.log"):
        self.addresses.clear()

        with open(path) as f:
            lines = f.readlines()

        for access_log in tqdm(
            Parallel(n_jobs=8)(delayed(parse_access_log)(line) for line in lines)
        ):
            self.addresses.add(access_log.remote_addr)
            self.logs.append(access_log)
        self.layoutChanged.emit()

    @cache
    def data(self, index: QModelIndex, role=Qt.ItemDataRole.DisplayRole):
        access_log: NGINXAccessLog = self.logs[index.row()]

        if role == Qt.ItemDataRole.DisplayRole:
            return access_log[index.column()]

        if (
            role == Qt.ItemDataRole.DecorationRole
            and index.column() == 0
            and (band := IPv4RBand.of(access_log.remote_addr))
        ):
            return get_country_icon(band.country)

    def rowCount(self, parent: QModelIndex = QModelIndex()):
        return len(self.logs)

    def columnCount(self, parent: QModelIndex = QModelIndex()):
        return len(NGINXAccessLog._fields)

    def headerData(self, section: int, orientation: Qt.Orientation, /, role: int = ...):
        if (
            orientation == Qt.Orientation.Horizontal
            and role == Qt.ItemDataRole.DisplayRole
        ):
            return NGINXAccessLog._fields[section]
        return None
