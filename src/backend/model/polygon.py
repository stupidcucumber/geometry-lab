import numpy as np
from pydantic import BaseModel
from .point import Point


class StarPolygon(BaseModel):
    points: list[Point]
    center: Point | None = None
    
    def asarray(self) -> np.ndarray:
        return np.asarray([[point.x, point.y] for point in self.points])