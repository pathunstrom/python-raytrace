from tracer import (
    Canvas,
    Color,
    Matrix,
    point,
    Ray,
    Sphere,
    Tuple,
)

vec: Tuple

canvas_pixels = 100
wall_size = 7
transform = Matrix.identity
file_name = "circle.ppm"

pixel_size = wall_size / canvas_pixels
half = wall_size / 2
color = Color(.6, .25, .5)
canvas = Canvas(canvas_pixels, canvas_pixels)

ray_origin = point(0, 0, -5)

sphere = Sphere(transform=transform)
surface_z = 10

for y in range(canvas_pixels):
    world_y = half - (pixel_size * y)
    for x in range(canvas_pixels):
        world_x = -half + (pixel_size * x)
        position = point(world_x, world_y, surface_z)
        vec = (position - ray_origin).normalize()
        ray = Ray(ray_origin, vec)
        if ray.intersects(sphere).hit():
            canvas[x, y] = color

canvas.save(file_name)
