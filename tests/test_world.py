from tracer import (
    Color,
    Light,
    Material,
    point,
    Sphere,
    transforms,
    World,
)


def test_world():
    world = World()
    assert len(world) == 0
    assert len(world.lights) == 0


def test_default_world():
    light = Light(point(-10, 10, -10), Color(1, 1, 1))
    sphere_1 = Sphere(
        material=Material(
            color=Color(0.8, 1.0, 0.6),
            diffuse=0.7,
            specular=0.2
        )
    )
    sphere_2 = Sphere(
        transform=transforms.scaling(0.5, 0.5, 0.5)
    )
    world = World.default()
    assert world.lights[0] == light
    assert sphere_1 in world
    assert sphere_2 in world
