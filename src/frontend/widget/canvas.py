from PyQt6.QtCore import QObject, Qt
from PyQt6.QtWidgets import (
    QLabel
)
from PyQt6.QtGui import (
    QMouseEvent, 
    QPixmap, 
    QPainter,
    QPen
)
from ...backend.model import Point, StarPolygon, Circle
from ..utils import (
    get_voronoi_verteces,
    generate_star_polygon,
    get_voronoi_circles
)


class Canvas(QLabel):
    def __init__(self, width: int, height: int, parent: QObject | None = None, **kwargs) -> None:
        super(Canvas, self).__init__(parent, **kwargs)
        self.canvas_width = width
        self.canvas_height = height
        self.polygon: StarPolygon | None = None
        self.voronoi_vertices: list[Point] | None = None
        self.voronoi_circles: list[Point] | None = None
        self._setup_layout()
        self.mouse_x: int = None
        self.mouse_y: int = None
        self.points: list[Point] = []
        
    def _create_pen(self, width: int, color: Qt.GlobalColor = Qt.GlobalColor.black) -> QPen:
        pen = QPen()
        pen.setWidth(width)
        pen.setColor(color)
        return pen
        
    def _draw_point(self, pixmap: QPixmap, point: Point, color: Qt.GlobalColor) -> None:
        painter = QPainter(pixmap)
        painter.setPen(
            self._create_pen(width=1, color=color)
        )
        painter.drawEllipse(point.x, point.y, 2, 2)
        painter.end()
        
    def _draw_circle(self, pixmap: QPixmap, circle: Circle, color: Qt.GlobalColor) -> None:
        painter = QPainter(pixmap)
        painter.setPen(
            self._create_pen(width=1, color=color)
        )
        painter.drawEllipse(
            circle.center.x - circle.radius, 
            circle.center.y - circle.radius, 
            circle.radius * 2, 
            circle.radius * 2
        )
        painter.end()
    
    def _draw_line(self, pixmap: QPixmap, first_point: Point, second_point: Point, color: Qt.GlobalColor) -> None:
        painter = QPainter(pixmap)
        painter.setPen(
            self._create_pen(width=1, color=color)
        )
        painter.drawLine(
            first_point.x, first_point.y,
            second_point.x, second_point.y
        )
        painter.end()
    
    def _draw_voroniy_diagram(self, polygon: StarPolygon, pixmap: QPixmap, color: Qt.GlobalColor) -> None:
        pass
        
    def _draw_polygon(self, pixmap: QPixmap, polygon: StarPolygon) -> None:
        points = polygon.points
        previous_point = points[0]
        self._draw_point(pixmap=pixmap, point=previous_point, color=Qt.GlobalColor.black)
        for point in points[1:]:
            self._draw_point(pixmap=pixmap, point=point, color=Qt.GlobalColor.black)
            self._draw_line(
                pixmap=pixmap,
                first_point=previous_point, second_point=point, color=Qt.GlobalColor.red
            )
            previous_point = point
        self._draw_line(
            pixmap=pixmap,
            first_point=points[0], second_point=points[-1], color=Qt.GlobalColor.red
        )
    
    def clear(self) -> None:
        self.points.clear()
        pixmap = self.pixmap()
        pixmap.fill(Qt.GlobalColor.white)
        self.setPixmap(pixmap)
        self.update()
        
    def generate(self, center_point: Point, min_radius: int = 50, max_radius: int = 300,
                 n_vertices: int = 10) -> None:
        self.clear()
        self.polygon = generate_star_polygon(
            center=center_point,
            n_vertices=n_vertices, min_radius=min_radius, max_radius=max_radius
        )
        self.points = self.polygon.points
        pixmap = self.pixmap()
        self._draw_polygon(polygon=self.polygon, pixmap=pixmap)
        self._draw_point(pixmap=pixmap, point=center_point,color=Qt.GlobalColor.green)
        self.setPixmap(pixmap)
        self.draw_voronoi_verteces()
        self.draw_voronoi_circles()
    
    def draw_voronoi_verteces(self) -> None:
        if not self.polygon:
            return
        if not self.voronoi_vertices:
            self.voronoi_vertices = get_voronoi_verteces(polygon=self.polygon)
        pixmap = self.pixmap()
        for point in self.voronoi_vertices:
            self._draw_point(pixmap=pixmap, point=point, color=Qt.GlobalColor.blue)
        self.setPixmap(pixmap)
        
    def draw_voronoi_circles(self) -> None:
        if not self.polygon:
            return
        if not self.voronoi_circles:
            self.voronoi_circles = get_voronoi_circles(polygon=self.polygon)
        pixmap = self.pixmap()
        for circle in self.voronoi_circles:
            self._draw_circle(pixmap=pixmap, circle=circle, color=Qt.GlobalColor.blue)
        self.setPixmap(pixmap)
    
    def mousePressEvent(self, ev: QMouseEvent | None) -> None:
        point = Point(x=ev.pos().x(), y=ev.pos().y())
        self.points.append(point)
        pixmap = self.pixmap()
        self._draw_point(
            pixmap=pixmap,
            point=point,
            color=Qt.GlobalColor.black
        )
        self.setPixmap(pixmap)
        
    
    def _setup_layout(self) -> None:
        canvas = QPixmap(self.canvas_width, self.canvas_height)
        canvas.fill(Qt.GlobalColor.white)
        self.setPixmap(canvas)