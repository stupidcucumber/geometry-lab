from ..model import StarPolygon, Point
from scipy.spatial import Voronoi


def find_voroni_vertices(polygon: StarPolygon) -> list[Point]:
    voronoi = Voronoi(polygon.asarray())
    return [Point(x=int(x), y=int(y)) for x, y in voronoi.vertices]