from math import pi

from tracer import Canvas, Matrix, Vector, Color


canvas = Canvas(200, 200)
transform = Matrix.identity
offset = Vector.vector(0, 80, 0)
origin = Vector.vector(100, 100, 0)
red = Color(1, 0, 0)
twelfth = pi / 6

for _ in range(12):
    transform = transform.rotate_z(twelfth)
    x, y, _, _ = (transform * offset) + origin
    canvas[int(x), int(y)] = red

canvas.save("clock.ppm")
