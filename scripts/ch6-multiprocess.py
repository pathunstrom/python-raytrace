from itertools import product
from multiprocessing import Pool
from os import cpu_count
from time import monotonic

from tracer import (
    Canvas,
    Color,
    Matrix,
    point,
    Ray,
    Sphere,
    Material,
    Light
)

canvas_pixels = 300
wall_size = 7
transform = Matrix.identity
file_name = "multiprocessed.ppm"

surface_z = 10
pixel_size = wall_size / canvas_pixels
half = wall_size / 2
canvas = Canvas(canvas_pixels, canvas_pixels)

ray_origin = point(0, 0, -5)

sphere = Sphere(transform=transform, material=Material(color=Color(0.7, 0.3, 0.7), ambient=.2, shininess=2, diffuse=.7))
light = Light(point(-10, 10, -10), Color(1, 1, 1))


def calculate_ray(x, y):
    world_y = half - (pixel_size * y)
    world_x = -half + (pixel_size * x)
    position = point(world_x, world_y, surface_z)
    vec = (position - ray_origin).normalize()
    ray = Ray(ray_origin, vec)
    hit = ray.intersects(sphere).hit()
    if not hit:
        return x, y, Color(0, 0, 0)
    hit_point = ray.position(hit.distance)
    surface_normal = hit.hull.normal_at(hit_point)
    eye_vector = -ray.direction
    color = hit.hull.material.lighting(light, hit_point, eye_vector, surface_normal)
    return x, y, color


if __name__ == "__main__":
    start_time = monotonic()

    inputs = product(range(canvas_pixels), range(canvas_pixels))
    cpus = cpu_count() // 2
    pool = Pool(cpus)
    pixels = pool.starmap(func=calculate_ray, iterable=inputs, chunksize=canvas_pixels ** 2 // cpus)
    pool.close()
    pool.join()
    for x, y, color in pixels:
        canvas[x, y] = color
    canvas.save(file_name)
    print(f"Run time: {monotonic() - start_time} seconds")
