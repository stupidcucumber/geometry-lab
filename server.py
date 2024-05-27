from pydantic import BaseModel
from fastapi import FastAPI
from src.backend.model import (
    StarPolygon,
    Point,
    Circle
)
from src.backend.utils import (
    find_voroni_vertices,
    generate_star_polygon,
    find_voronoi_circles
)


api = FastAPI()


@api.post('/voronoi/polygon/verteces') 
def get_voronoi_vertices(starPolygon: StarPolygon) -> list[Point]:
    return find_voroni_vertices(starPolygon)


@api.post('/voronoi/polygon/circles')
def get_voronoi_circles(starPolygon: StarPolygon) -> list[Circle]:
    return find_voronoi_circles(polygon=starPolygon)


class GeneratePolygonRequest(BaseModel):
    centerPoint: Point
    minRadius: int
    maxRadius: int
    nVertices: int

@api.post('/generate/polygon')
def post_polygon_params(request: GeneratePolygonRequest) -> StarPolygon:
    return generate_star_polygon(
        center=request.centerPoint,
        n_vertices=request.nVertices,
        min_radius=request.minRadius,
        max_radius=request.maxRadius
    )