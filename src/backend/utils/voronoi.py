from ..model import StarPolygon, Point, Circle
from shapely.geometry import Point as ShapelyPoint, Polygon as ShapelyPolygon
import pyvoronoi as pyv


def filter_outer_points(polygon: StarPolygon, points: list[Point]) -> list[Point]:
    shapely_polygon = ShapelyPolygon(polygon.asarray())
    shapely_points = [ShapelyPoint(point.x, point.y) for point in points]
    return [
        Point(x = point.x, y = point.y) for point in shapely_points if point.within(shapely_polygon)
    ]


def find_voroni_vertices(polygon: StarPolygon) -> list[Point]:
    polygon_verteces = polygon.asarray()
    pv = pyv.Pyvoronoi(100)
    for index in range(len(polygon_verteces)):
        pv.AddSegment(
            [
                polygon_verteces[index],
                polygon_verteces[index + 1 if index + 1 < len(polygon_verteces) else 0]
            ]
        )
    pv.Construct()
    raw_points = [
        Point(x=int(vertex.X), y=int(vertex.Y)) for vertex in pv.GetVertices()
    ]
    return filter_outer_points(polygon=polygon, points=raw_points)
    
    
def find_voronoi_circles(polygon: StarPolygon) -> list[Circle]:
    result = []
    vertices = find_voroni_vertices(polygon=polygon)
    shapely_polygon = ShapelyPolygon(polygon.asarray())
    shapely_points = [ShapelyPoint(point.x, point.y) for point in vertices]
    for index, shapely_point in enumerate(shapely_points):
        result.append(
            Circle(
                center=vertices[index],
                radius=int(shapely_polygon.boundary.distance(shapely_point))
            )
        )
    return result