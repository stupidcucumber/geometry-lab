import numpy as np
from ..model import StarPolygon, Point


def generate_star_polygon(center: Point, n_vertices: int = 5, min_radius: float = 10,
                          max_radius: float = 20) -> StarPolygon:
    '''
        This function generates star polygons.
    '''
    distance = np.random.rand(n_vertices)
    alpha = np.sort((np.random.rand(n_vertices) * 360))
    params = np.stack([alpha, distance])
    parameters_rad = (params * np.asarray([[np.pi / 180], [max_radius - min_radius]]))
    delta_xs = np.cos(parameters_rad[0]) * parameters_rad[1]
    delta_ys = np.sin(parameters_rad[0]) * parameters_rad[1]
    points = [
        Point(x=int(center.x + delta_x), y=int(center.y + delta_y))
        for delta_x, delta_y in zip(delta_xs, delta_ys)
    ]
    return StarPolygon(points=points)