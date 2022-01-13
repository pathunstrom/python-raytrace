from dataclasses import dataclass
from itertools import count
from typing import Union

from tracer import Vector

number = Union[float, int]
vector_tuple = tuple[number, number, number]


@dataclass
class Environment:
    gravity: Vector
    wind: Vector


@dataclass
class Projectile:
    position: Vector
    velocity: Vector


def tick(env: Environment, projectile: Projectile):
    position = projectile.position + projectile.velocity
    velocity = projectile.velocity + env.gravity + env.wind
    return Projectile(position, velocity)


def main(position: vector_tuple, velocity: vector_tuple, gravity: vector_tuple, wind: vector_tuple):
    projectile = Projectile(Vector.point(*position), Vector.vector(*velocity))
    environment = Environment(Vector.vector(*gravity), Vector.vector(*wind))
    frame = 0
    for frame in count():
        projectile = tick(environment, projectile)
        print(f"Current Height: {projectile.position.y}")
        if projectile.position.y <= 0:
            break
    print(f"Took {frame} ticks to hit the ground. Final position was {projectile.position}")


if __name__ == "__main__":
    main((0, 0.1, 0), (6, 9, 0), (0, -0.2, 0), (0, 0, 0))
