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

import tracer

# wall_material = Material(
#     pattern=tracer.CheckeredPattern(
#         first_pattern=tracer.StripePattern(
#             transform=transforms.rotation_y(pi / 4).scale(0.2, 1, 0.2),
#             first_pattern=SolidPattern(color=Color(0.250, 0.466, 0.094)),
#             second_pattern=SolidPattern(color=Color(0.203, 0.321, 0.117))
#         ),
#         second_pattern=SolidPattern(color=Color(.4, .1, .4))
#     ),
#     specular=0.1
# )

# wall_material = Material(
#     pattern=tracer.MultiplyBlendPattern(
#         first_pattern=tracer.StripePattern(
#             first_pattern=tracer.SolidPattern(color=Color(0.1, 0.5, 0.1)),
#             second_pattern=tracer.SolidPattern(color=tracer.WHITE)
#         ),
#         second_pattern=tracer.StripePattern(
#             transform=transforms.rotation_y(pi / 2),
#             first_pattern=tracer.SolidPattern(color=Color(0.1, 0.5, 0.1)),
#             second_pattern=tracer.SolidPattern(color=tracer.WHITE)
#         )
#     )
# )

wall_material = Material(
    pattern=tracer.CheckeredPattern(
        first_pattern=tracer.SolidPattern(color=Color(.2, .5, .2)),
        second_pattern=SolidPattern(color=Color(.4, .1, .4))
    ),
    specular=0.1
)

# wall_material = Material(
#     pattern=tracer.RadialGradientPattern(
#         first_pattern=SolidPattern(color=Color(0.5, 0.1, 0.5)),
#         second_pattern=SolidPattern(color=Color(1, 0.278, 0.870))
#     )
# )

world = World(
    [
        Plane(material=wall_material)
    ],
    Light(point(2, 15, 2), Color(1, 1, 1))
)

camera = Camera(
    # 96, 54,
    320, 180,
    # 640, 360,
    pi / 2,
    Matrix.view(point(5, 2, 5), point(0, 2, 0), vector(0, 1, 0))
)

if __name__ == "__main__":
    canvas = camera.render(world)

    canvas.save("ch10-checker-board-test.ppm")
