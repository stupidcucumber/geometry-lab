import requests
from ...backend.model import StarPolygon, Point, Circle


def get_voronoi_verteces(polygon: StarPolygon) -> list[Point]:
    response = requests.post(
        url='http://127.0.0.1:8081/voronoi/polygon/verteces',
        json=polygon.model_dump()
    )
    data = response.json()
    return [Point(**s_point) for s_point in data]


def get_voronoi_circles(polygon: StarPolygon) -> list[Circle]:
    response = requests.post(
        url='http://127.0.0.1:8081/voronoi/polygon/circles',
        json=polygon.model_dump()
    )
    data = response.json()
    return [Circle(**s_circle) for s_circle in data]


def generate_star_polygon(center: Point, n_vertices: int = 5, min_radius: int = 10,
                          max_radius: int = 20) -> StarPolygon:
    response = requests.post(
        url='http://127.0.0.1:8081/generate/polygon',
        json={
                'centerPoint': center.model_dump(),
                'minRadius': int(min_radius),
                'maxRadius': int(max_radius),
                'nVertices': n_vertices
            }
    )
    return StarPolygon(**response.json())
