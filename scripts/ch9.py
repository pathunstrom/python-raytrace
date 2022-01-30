from math import pi

from tracer import (
    Camera,
    Color,
    Light,
    Material,
    Matrix,
    Plane,
    point,
    vector,
    Sphere,
    transforms,
    World,
    RadialGradientPattern,
    SolidPattern,
    RED,
    BLUE,
)

wall_material = Material(
    pattern=RadialGradientPattern(
        transform=transforms.scaling(10, 1, 10),
        first_pattern=SolidPattern(color=RED),
        second_pattern=SolidPattern(color=BLUE)
    ),
    specular=0.1
)

world = World(
    [
        Plane(material=wall_material)
    ],
    Light(point(2, 15, 2), Color(1, 1, 1))
)

camera = Camera(
    96, 54,
    # 640, 360,
    pi / 2,
    Matrix.view(point(0, 2, 6), point(0, 1, 0), vector(0, 1, 0))
)

if __name__ == "__main__":
    canvas = camera.render(world)

    canvas.save("ch10-radial-gradient.ppm")
