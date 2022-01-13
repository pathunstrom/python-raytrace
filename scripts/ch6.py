import time

from tracer import (
    Canvas,
    Color,
    Matrix,
    point,
    Ray,
    Sphere,
    Vector,
    Material,
    Light
)

vec: Vector

canvas_pixels = 300
wall_size = 7
transform = Matrix.identity
file_name = "singlethreaded.ppm"

pixel_size = wall_size / canvas_pixels
half = wall_size / 2
canvas = Canvas(canvas_pixels, canvas_pixels)

ray_origin = point(0, 0, -5)

sphere = Sphere(transform=transform, material=Material(color=Color(0.7, 0.3, 0.7), ambient=.2, shininess=2, diffuse=.7))
light = Light(point(-10, 10, -10), Color(1, 1, 1))

surface_z = 10

start_time = time.monotonic()

for y in range(canvas_pixels):
    world_y = half - (pixel_size * y)
    for x in range(canvas_pixels):
        world_x = -half + (pixel_size * x)
        position = point(world_x, world_y, surface_z)
        vec = (position - ray_origin).normalize()
        ray = Ray(ray_origin, vec)
        hit = ray.intersects(sphere).hit()
        if not hit:
            continue
        hit_point = ray.position(hit.distance)
        surface_normal = hit.hull.normal_at(hit_point)
        eye_vector = -ray.direction
        color = hit.hull.material.lighting(light, hit_point, eye_vector, surface_normal)
        canvas[x, y] = color

canvas.save(file_name)

print(f"Run time: {time.monotonic() - start_time} seconds")