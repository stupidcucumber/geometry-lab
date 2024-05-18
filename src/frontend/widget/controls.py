from typing import Callable
from PyQt6.QtCore import QObject
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton
)
from .canvas import Canvas


class Controls(QWidget):
    def __init__(self, canvas: Canvas, parent: QObject | None = None) -> None:
        super(Controls, self).__init__(parent)
        self.canvas = canvas
        self._setup_layout()
        
    def _create_button(self, label: str, parent: QObject, slot: Callable) -> QPushButton:
        button = QPushButton(label, parent)
        button.pressed.connect(slot)
        return button
        
    def _setup_layout(self) -> None:
        base_layout = QVBoxLayout(self)
        base_layout.addWidget(
            self._create_button('Generate', self, lambda: self.canvas.generate())
        )
        base_layout.addWidget(
            self._create_button('Clear', self, lambda: self.canvas.clear())
        )
        self.setLayout(base_layout)