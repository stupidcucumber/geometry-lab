from PyQt6.QtCore import QObject, Qt
from PyQt6.QtWidgets import (
    QLabel
)
from PyQt6.QtGui import (
    QMouseEvent, 
    QPixmap, 
    QPainter
)
from ...backend.model import Point


class Canvas(QLabel):
    def __init__(self, width: int, height: int, parent: QObject | None = None, **kwargs) -> None:
        super(Canvas, self).__init__(parent, **kwargs)
        self.canvas_width = width
        self.canvas_height = height
        self._setup_layout()
        self.mouse_x: int = None
        self.mouse_y: int = None
        self.points: list[Point] = []
    
    def clear(self) -> None:
        self.points.clear()
        pixmap = self.pixmap()
        pixmap.fill(Qt.GlobalColor.white)
        self.setPixmap(pixmap)
        self.update()
        
    def generate(self) -> None:
        self.clear()
        print('Generating...')
    
    def mousePressEvent(self, ev: QMouseEvent | None) -> None:
        point = Point(x=ev.pos().x(), y=ev.pos().y())
        self.points.append(point)
        pixmap = self.pixmap()
        painter = QPainter(pixmap)
        painter.drawEllipse(point.x, point.y, 5, 5)
        painter.end()
        self.setPixmap(pixmap)
    
    def _setup_layout(self) -> None:
        canvas = QPixmap(self.canvas_width, self.canvas_height)
        canvas.fill(Qt.GlobalColor.white)
        self.setPixmap(canvas)