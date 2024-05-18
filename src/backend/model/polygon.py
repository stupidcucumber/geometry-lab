from pydantic import BaseModel
from .point import Point
from .circle import Circle


class StarPolygon(BaseModel):
    points: list[Point]
    
    def find_biggest_circle(self) -> Circle:
        pass