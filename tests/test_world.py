from tracer import World


def test_world():
    world = World()
    assert len(world) == 0
    assert len(world.lights) == 0
