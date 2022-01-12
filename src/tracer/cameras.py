from __future__ import annotations

from math import tan

from tracer.matrices import Matrix
from tracer.physicals import Ray
from tracer.tuples import Tuple


class Camera:
    """A camera"""

    def __init__(self, horizontal_pixels: int, vertical_pixels: int, field_of_view: int | float):
        self.horizontal_pixels = horizontal_pixels
        self.vertical_pixels = vertical_pixels
        self.field_of_view = field_of_view
        self.transform = Matrix.identity
        half_view = tan(field_of_view / 2)
        aspect = horizontal_pixels / vertical_pixels
        if aspect >= 1:
            self.half_width = half_view
            self.half_height = half_view / aspect
        else:
            self.half_width = half_view * aspect
            self.half_height = half_view
        self.pixel_size = self.half_width * 2 / self.horizontal_pixels

    def ray_for_pixel(self, pixel_x: int, pixel_y: int) -> Ray:
        x_offset = (pixel_x + 0.5) * self.pixel_size
        y_offset = (pixel_y + 0.5) * self.pixel_size

        world_x = self.half_width - x_offset
        world_y = self.half_height - y_offset

        transform = self.transform.inverse()
        pixel: Tuple = transform * Tuple.point(world_x, world_y, -1)
        origin: Tuple = transform * Tuple.point(0, 0, 0)
        direction = (pixel - origin).normalize()

        return Ray(origin, direction)
