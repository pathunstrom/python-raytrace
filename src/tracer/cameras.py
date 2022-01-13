from __future__ import annotations

from functools import partial
from itertools import product
from math import tan
from multiprocessing import Pool
from os import cpu_count

from tracer.matrices import Matrix
from tracer.physicals import Ray
from tracer.renderer import Canvas
from tracer.tuples import Tuple, Color
from tracer.worlds import World


class Camera:
    """A camera"""

    def __init__(self, horizontal_pixels: int, vertical_pixels: int, field_of_view: int | float, transform: Matrix = Matrix.identity):
        self.horizontal_pixels = horizontal_pixels
        self.vertical_pixels = vertical_pixels
        self.field_of_view = field_of_view
        self.transform = transform
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

    def _get_pixel(self, world: World, x: int, y: int) -> tuple[int, int, Color]:
        ray = self.ray_for_pixel(x, y)
        return x, y, world.color_at(ray)

    def render(self, world) -> Canvas:
        cpus = max(cpu_count() // 2, 1)

        total_pixels = self.horizontal_pixels * self.vertical_pixels
        coordinates = product(range(self.horizontal_pixels), range(self.vertical_pixels))
        pool = Pool(cpus)
        pixels = pool.starmap(func=partial(self._get_pixel, world), iterable=coordinates, chunksize=total_pixels // cpus)

        canvas = Canvas(self.horizontal_pixels, self.vertical_pixels)
        for x, y, color in pixels:
            canvas[x, y] = color

        return canvas
