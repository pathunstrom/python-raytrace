from pytest import mark

from tracer import (
    BLACK,
    Color,
    Intersection,
    Light,
    Material,
    point,
    Ray,
    Sphere,
    transforms,
    vector,
    WHITE,
    World,
)


def test_world():
    world = World()
    assert len(world) == 0
    assert world.light is None


def test_default_world():
    light = Light(point(-10, 10, -10), WHITE)
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
    assert world.light == light
    assert sphere_1 in world
    assert sphere_2 in world


def test_world_intersect():
    world = World.default()
    ray = Ray(point(0, 0, -5), vector(0, 0, 1))
    intersections = list(world.intersect(ray))
    assert len(intersections) == 4
    for intersection, expected_distance in zip(intersections, [4, 4.5, 5.5, 6]):
        assert intersection.distance == expected_distance


def test_world_shade_hit():
    world = World.default()
    ray = Ray(point(0, 0, -5), vector(0, 0, 1))
    shape = world.children[0]
    intersection = Intersection(4, shape)
    computations = intersection.prepare_computations(ray)
    color = world.shade_hit(computations)
    assert color == Color(0.38066, 0.47583, 0.2855)


def test_world_shade_hit_inside():
    world = World.default()
    world.light.position = point(0, 0.25, 0)
    ray = Ray(point(0, 0, 0), vector(0, 0, 1))
    shape = world.children[1]
    intersection = Intersection(0.5, shape)
    computations = intersection.prepare_computations(ray)
    color = world.shade_hit(computations)
    assert color == Color(0.90498, 0.90498, 0.90498)


def test_world_shade_given_shadow():
    world = World(
        [
            Sphere(),
            Sphere(transform=transforms.translation(0, 0, 10))
        ],
        Light(point(0, 0, -10))
    )

    ray = Ray(point(0, 0, 5), vector(0, 0, 1))
    intersection = Intersection(4, world.children[1])
    computations = intersection.prepare_computations(ray)
    assert world.shade_hit(computations) == Color(0.1, 0.1, 0.1)


def test_world_color_at_no_hit():
    world = World.default()
    ray = Ray(point(0, 0, -5), vector(0, 1, 0))
    color = world.color_at(ray)
    assert color == BLACK


def test_world_color_at_hit():
    world = World.default()
    ray = Ray(point(0, 0, -5), vector(0, 0, 1))
    color = world.color_at(ray)
    assert color == Color(0.38066, 0.47583, 0.2855)


def test_world_color_at_with_negative_intersection():
    world = World.default()
    world.children[0].material.ambient = 1
    world.children[1].material.ambient = 1
    ray = Ray(point(0, 0, 0.75), vector(0, 0, -1))
    color = world.color_at(ray)
    assert color == world.children[1].material.color


@mark.parametrize(
    "point, expected",
    [
        (point(0, 10, 0), False),
        (point(10, -10, 10), True),
        (point(-20, 20, -20), False),
        (point(-2, 2, -2), False)
    ]
)
def test_world_is_shadowed(point, expected):
    world = World.default()
    assert world.is_shadowed(point) == expected
