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
        self.voronoi_circles: list[Circle] | None = None
        self.center_point: Point | None = None
        self.points: list[Point] = []
        self._setup_layout()
        self.mouse_x: int = None
        self.mouse_y: int = None
        
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
        painter.drawEllipse(point.x-1, point.y-1, 2, 2)
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
        
    def erase_all(self) -> None:
        pixmap = self.pixmap()
        pixmap.fill(Qt.GlobalColor.white)
        self.setPixmap(pixmap)
        self.update()
    
    def clear(self) -> None:
        self.points.clear()
        self.voronoi_circles = None
        self.voronoi_vertices = None
        self.polygon = None
        self.erase_all()
        
    def manual_find(self, draw_all_circles: bool = False) -> None:
        self.polygon: StarPolygon = StarPolygon(points=self.points, center=None)
        pixmap = self.pixmap()
        self._draw_polygon(pixmap=pixmap, polygon=self.polygon)
        self.setPixmap(pixmap)
        self.draw_voronoi_circles(draw_all_circles=draw_all_circles)
        
    def generate(self, center_point: Point, min_radius: int = 50, max_radius: int = 300,
                 n_vertices: int = 10, draw_all_circles: bool = False) -> None:
        self.clear()
        self.center_point = center_point
        self.polygon = generate_star_polygon(
            center=self.center_point,
            n_vertices=n_vertices, min_radius=min_radius, max_radius=max_radius
        )
        self.center_point = center_point
        self.draw_all(draw_all_circles=draw_all_circles)
        
    def draw_all(self, draw_all_circles: bool = False) -> None:
        if not self.polygon:
            return
        self.erase_all()
        pixmap = self.pixmap()
        self._draw_polygon(polygon=self.polygon, pixmap=pixmap)
        if self.center_point:
            self._draw_point(pixmap=pixmap, point=self.center_point,color=Qt.GlobalColor.green)
        self.setPixmap(pixmap)
        self.draw_voronoi_verteces()
        self.draw_voronoi_circles(draw_all_circles=draw_all_circles)
    
    def draw_voronoi_verteces(self) -> None:
        if not self.polygon:
            return
        if not self.voronoi_vertices:
            self.voronoi_vertices = get_voronoi_verteces(polygon=self.polygon)
        pixmap = self.pixmap()
        for point in self.voronoi_vertices:
            self._draw_point(pixmap=pixmap, point=point, color=Qt.GlobalColor.blue)
        self.setPixmap(pixmap)
        
    def draw_voronoi_circles(self, draw_all_circles: bool = True) -> None:
        if not self.polygon:
            return
        if not self.voronoi_circles:
            self.voronoi_circles = get_voronoi_circles(polygon=self.polygon)
        pixmap = self.pixmap()
        if draw_all_circles:
            for circle in self.voronoi_circles:
                self._draw_circle(pixmap=pixmap, circle=circle, color=Qt.GlobalColor.blue)
        else:
            biggest_circle = self.voronoi_circles[0]
            for circle in self.voronoi_circles:
                if circle.radius > biggest_circle.radius:
                    biggest_circle = circle
            self._draw_circle(pixmap=pixmap, circle=biggest_circle, color=Qt.GlobalColor.blue)
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