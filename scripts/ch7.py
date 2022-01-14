from math import pi

from tracer import (
    Camera,
    Color,
    Light,
    Material,
    Matrix,
    point,
    vector,
    Sphere,
    transforms,
    World,
)

wall_material = Material(color=Color(0.7, 0.4, 0.65), specular=0)
world = World(
    [
        Sphere(
            transform=transforms.scaling(10, 0.01, 10),
            material=wall_material
        ),
        Sphere(
            transform=Matrix.identity.scale(10, 0.01, 10).rotate_x(pi / 2).rotate_y(-pi / 4).translate(0, 0, 5),
            material=wall_material
        ),
        Sphere(
            transform=Matrix.identity.scale(10, 0.01, 10).rotate_x(pi / 2).rotate_y(pi / 4).translate(0, 0, 5),
            material=wall_material
        ),
        Sphere(
            transform=transforms.translation(-0.5, 1, 0.5).scale(0.75, 1, 0.75),
            material=Material(color=Color(0.4, 0.45, 0.45), diffuse=0.8, specular=2, shininess=400)
        ),
        Sphere(
            transform=Matrix.identity.scale(0.5, 0.5, 0.5).shear(0, 1, 0, 0.25, 0, 0).translate(0.75, 0.5, 1.5),
            material=Material(color=Color(0.5, 1, 0.1), diffuse=0.7, specular=0.3)
        ),
        Sphere(
            transform=Matrix.identity.scale(0.33, 0.1, 0.33).translate(-1.5, 1, -0.3),
            material=Material(color=Color(1, 0.6, 0.6), diffuse=0.9, specular=0.65)
        )
    ],
    Light(point(-10, 10, -10), Color(1, 1, 1))
)

camera = Camera(
    # 96, 54,
    640, 360,
    pi / 5,
    Matrix.view(point(-4, 2, -4), point(-0.5, 1, 0), vector(0, 1, 0))
)

if __name__ == "__main__":
    canvas = camera.render(world)

    canvas.save("ch7-7.ppm")
