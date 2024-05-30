from typing import Callable
from PyQt6.QtCore import QObject
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QLineEdit,
    QCheckBox,
    QComboBox
)
from ...backend.model import Point
from .canvas import Canvas


class ManualControls(QWidget):
    def __init__(self, canvas: Canvas, parent: QObject | None = None) -> None:
        super(ManualControls, self).__init__(parent)
        self.canvas = canvas
        self.checkbox = QCheckBox('Show all circles', self)
        self.checkbox.stateChanged.connect(
            lambda e: self.canvas.draw_all(e == 2)
        )
        self._setup_layout()
        
    def _instantiate_find_circle_buttons(self) -> QPushButton:
        button = QPushButton('Find circle', self)
        button.pressed.connect(
            lambda: self.canvas.manual_find(draw_all_circles=self.checkbox.isChecked())
        )
        return button
    
    def _instantiate_clear_canvas_button(self) -> QPushButton:
        button = QPushButton('Clear', self)
        button.pressed.connect(
            lambda: self.canvas.clear()
        )
        return button
        
    def _setup_layout(self) -> None:
        layout = QVBoxLayout(self)
        layout.addWidget(
            self._instantiate_find_circle_buttons()
        )
        layout.addWidget(
            self._instantiate_clear_canvas_button()
        )
        layout.addWidget(
            self.checkbox
        )


class GenerationControls(QWidget):
    def __init__(self, canvas: Canvas, parent: QObject | None = None) -> None:
        super(GenerationControls, self).__init__(parent)
        self.canvas = canvas
        self.checkbox = QCheckBox('Show all circles', self)
        self.checkbox.stateChanged.connect(
            lambda e: self.canvas.draw_all(e == 2)
        )
        self.min_radius: int = 50
        self.max_radius: int = 500
        self.n_vertices: int = 10
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
            
    def _instantiate_generate_button(self) -> QPushButton:
        button = QPushButton('Generate', self)
        button.pressed.connect(
            lambda: self.canvas.generate(
                center_point=Point(x=500, y=500),
                min_radius=self.min_radius,
                max_radius=self.max_radius,
                n_vertices=self.n_vertices,
                draw_all_circles=self.checkbox.isChecked()
            )
        )
        return button
        
    def _instantiate_clear_canvas_button(self) -> QPushButton:
        button = QPushButton('Clear', self)
        button.pressed.connect(
            lambda: self.canvas.clear()
        )
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
        
    def _setup_layout(self) -> None:
        layout = QVBoxLayout(self)
        layout.addWidget(
            self._create_input_box(
                parent=self,
                label='Min radius:',
                default=str(self.min_radius),
                slot=lambda e: self._set_min_radius(e)
            )
        )
        layout.addWidget(
            self._create_input_box(
                parent=self,
                label='Max radius:',
                default=str(self.max_radius),
                slot=lambda e: self._set_max_radius(e)
            )
        )
        layout.addWidget(
            self._create_input_box(
                parent=self,
                label='Number of vertices: ', 
                default=str(self.n_vertices),
                slot=lambda e: self._set_n_vertices(e)
            )
        )
        layout.addWidget(
            self._instantiate_generate_button()
        )
        layout.addWidget(
            self._instantiate_clear_canvas_button()
        )
        layout.addWidget(
            self.checkbox
        )


class ControlsView(QWidget):
    def __init__(self, canvas: Canvas, parent: QObject | None = None) -> None:
        super(ControlsView, self).__init__(parent)
        self.canvas = canvas
        self.combo_box: QComboBox = self._instantiate_combo_box()
        self._setup_layout()
    
    def _clean_layout(self) -> None:
        for i in reversed(range(self.layout().count())): 
            widget = self.layout().itemAt(i).widget()
            if widget != self.combo_box:
                widget.deleteLater()
    
    def _update_layout(self) -> None:
        self._clean_layout()
        self._setup_layout()

    def _instantiate_combo_box(self) -> QComboBox:
        combo_box = QComboBox()
        combo_box.addItem(
            'Manual control',
            'manual'
        )
        combo_box.addItem(
            'Generation control',
            
        )
        combo_box.currentTextChanged.connect(
            lambda: self._update_layout()
        )
        return combo_box
        
    def _setup_layout(self) -> None:
        if not self.layout():
            base_layout = QVBoxLayout(self)
        else:
            base_layout = self.layout()
        base_layout.addWidget(self.combo_box)
        base_layout.addWidget(
            ManualControls(canvas=self.canvas) if self.combo_box.currentData() == 'manual' else GenerationControls(canvas=self.canvas)
        )
        self.setMaximumWidth(200)