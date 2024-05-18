from pydantic import BaseModel
from .point import Point


class Circle(BaseModel):
    center: Point
    radius: float