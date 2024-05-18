from PyQt6.QtCore import QObject
from PyQt6.QtWidgets import (
    QWidget,
    QLayout
)


def instantiate_box(widgets: list[QWidget], layout: QLayout, parent: QObject | None = None) -> QWidget:
    widget = QWidget(parent)
    for _widget in widgets: 
        layout.addWidget(_widget)
    widget.setLayout(layout)
    return widget