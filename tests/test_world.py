from tracer import (
    Color,
    Intersection,
    Light,
    Material,
    point,
    Ray,
    Sphere,
    transforms,
    vector,
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
    world.lights[0].position = point(0, 0.25, 0)
    ray = Ray(point(0, 0, 0), vector(0, 0, 1))
    shape = world.children[1]
    intersection = Intersection(0.5, shape)
    computations = intersection.prepare_computations(ray)
    color = world.shade_hit(computations)
    assert color == Color(0.90498, 0.90498, 0.90498)
