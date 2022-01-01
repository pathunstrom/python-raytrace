from tracer import Ray, Tuple


def test_create_ray():
    origin = Tuple.point(1, 2, 3)
    direction = Tuple.vector(4, 5, 6)
    ray = Ray(origin, direction)
    assert ray.origin == origin
    assert ray.direction == direction


def test_position():
    ray = Ray(Tuple.point(2, 3, 4), Tuple.vector(1, 0, 0))
    assert ray.position(0) == Tuple.point(2, 3, 4)
    assert ray.position(1) == Tuple.point(3, 3, 4)
    assert ray.position(-1) == Tuple.point(1, 3, 4)
    assert ray.position(2.5) == Tuple.point(4.5, 3, 4)
