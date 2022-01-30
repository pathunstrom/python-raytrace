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
    StripePattern,
    RED,
    BLUE,
)

wall_material = Material(color=Color(.30, .23, .05), specular=0.1)

walls = [
    Plane(material=wall_material, transform=transforms.rotation_x(pi / 2).translate(0, 0, 10).rotate_y(pi / 3 * rads))
    for rads
    in range(6)
]
world = World(
    [
        Plane(material=wall_material),
        *walls,
        Sphere(
            transform=transforms.translation(0, 1, 0).scale(2, 2, 2),
            material=Material(
                color=Color(0.4, 0.2, 0.3),
                diffuse=0.8,
                specular=2,
                shininess=400,
                pattern=StripePattern(
                    a=RED, b=BLUE,
                    transform=transforms.rotation_z(pi / 3).scale(0.25, 0.25, 0.25)
                )
            )
        ),
        Sphere(
            transform=Matrix.identity.scale(0.5, 0.5, 0.5).translate(1.75, 0.5, 0.5).scale(2, 2, 2,),
             material=Material(color=Color(0.5, 1, 0.1), diffuse=0.7, specular=0.3)
        ),
        Sphere(
            transform=Matrix.identity.scale(0.33, 0.33, 0.33).translate(-1.5, 0.33, -0.3).scale(2, 2, 2),
            material=Material(color=Color(1, 0.6, 0.6), diffuse=0.9, specular=0.65)
        )
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

    canvas.save("ch10-0.ppm")
