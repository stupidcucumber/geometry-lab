from typing import Callable
from PyQt6.QtCore import QObject
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QLineEdit,
    QCheckBox
)
from ...backend.model import Point
from .canvas import Canvas


class Controls(QWidget):
    def __init__(self, canvas: Canvas, parent: QObject | None = None) -> None:
        super(Controls, self).__init__(parent)
        self.canvas = canvas
        self.min_radius = 50
        self.max_radius = 500
        self.n_vertices = 10
        self.checkbox = QCheckBox('Show all circles', self)
        self.checkbox.stateChanged.connect(
            lambda e: self.canvas.draw_all(e == 2)
        )
        self._setup_layout()
        
    def _set_min_radius(self, input: str | int) -> None:
        if input != '':
            self.min_radius = int(input)
        
    def _set_max_radius(self, input: str | int) -> None:
        if input != '':
            self.max_radius = int(input)
        
    def _set_n_vertices(self, input: str | int) -> None:
        if input != '':
            self.n_vertices = int(input)
        
    def _create_button(self, label: str, parent: QObject, slot: Callable, 
                       size: tuple[int, int]) -> QPushButton:
        button = QPushButton(label, parent)
        button.setMaximumSize(size[0], size[1])
        button.pressed.connect(slot)
        return button
    
    def _create_input(self, parent: QObject, default: str, slot: Callable) -> QLineEdit:
        line_edit = QLineEdit(default, parent)
        line_edit.setMaximumSize(100, 40)
        line_edit.textEdited.connect(slot)
        return line_edit
    
    def _create_input_box(self, parent: QObject, label: str, default: str, slot: Callable) -> QWidget:
        widget = QWidget(parent)
        layout = QVBoxLayout(widget)
        layout.addWidget(
            QLabel(label, widget)
        )
        layout.addWidget(
            self._create_input(parent=widget, default=default, slot=slot)
        )
        widget.setLayout(layout)
        return widget
    
    def _create_inputs_box(self, inputs: list[QWidget]) -> QWidget:
        widget = QWidget(self)
        layout = QVBoxLayout(widget)
        for _widget in inputs:
            layout.addWidget(_widget)
        widget.setLayout(layout)
        return widget
        
    def _setup_layout(self) -> None:
        base_layout = QVBoxLayout(self)
        base_layout.addWidget(
            self._create_inputs_box(
                inputs=[
                    self._create_input_box(
                        parent=self, label='Min Radius', default=str(self.min_radius),
                        slot=lambda event: self._set_min_radius(event)
                    ),
                    self._create_input_box(
                        parent=self, label='Max Radius', default=str(self.max_radius),
                        slot=lambda event: self._set_max_radius(event)
                    ),
                    self._create_input_box(
                        parent=self, label='Number of vertices', default=str(self.n_vertices),
                        slot=lambda event: self._set_n_vertices(event)
                    )
                ]
            )
        )
        base_layout.addWidget(self.checkbox)
        base_layout.addWidget(
            self._create_button(
                'Generate', self, 
                lambda: self.canvas.generate(
                    center_point=Point(x=500, y=500),
                    min_radius=self.min_radius,
                    max_radius=self.max_radius,
                    n_vertices=self.n_vertices,
                    draw_all_circles=self.checkbox.isChecked()
                ),
                size=(200, 50)
            )
        )
        base_layout.addWidget(
            self._create_button(
                'Clear', self, 
                lambda: self.canvas.clear(),
                size=(200, 50)
            )
        )
        self.setMaximumWidth(200)