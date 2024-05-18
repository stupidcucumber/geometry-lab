from PyQt6.QtCore import QObject
from PyQt6.QtWidgets import (
    QMainWindow,
    QToolBar
)


class MainWindow(QMainWindow):
    def __init__(self, width: int, height: int, parent: QObject | None = None, **kwargs) -> None:
        super(MainWindow, self).__init__(parent, **kwargs)
        self.setWindowTitle('Biggest circle finder 🐦‍🔥')
        self.setGeometry(0, 0, width, height)
        self._setup_layout()
        
    def _create_toolbar(self) -> QToolBar:
        toolbar = QToolBar(self)
        toolbar.addAction('Info', lambda: print('Opens Info Window!'))
        return toolbar
        
    def _setup_layout(self) -> None:
        toolbar = self._create_toolbar()
        self.addToolBar(toolbar)