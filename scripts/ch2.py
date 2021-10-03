from dataclasses import dataclass
from itertools import count
from pathlib import Path
from typing import Union

from tracer import Tuple, Canvas, Color


number = Union[float, int]
vector_tuple = tuple[number, number, number]


@dataclass
class Environment:
    gravity: Tuple
    wind: Tuple


@dataclass
class Projectile:
    position: Tuple
    velocity: Tuple


def tick(env: Environment, projectile: Projectile):
    position = projectile.position + projectile.velocity
    velocity = projectile.velocity + env.gravity + env.wind
    return Projectile(position, velocity)


def main(canvas: Canvas, environment: Environment, projectile: Projectile, color: Color = Color(.8, .2, .2)):
    frame = 0
    for frame in count():
        projectile = tick(environment, projectile)
        try:
            canvas[int(projectile.position.x), int(canvas.height - projectile.position.y)] = color
        except IndexError:
            pass
        if projectile.position.y <= 0 or projectile.position.x >= canvas.width:
            break
    canvas.save(Path("projectile2.ppm"))
    print(f"Took {frame} ticks to hit the ground. Final position was {projectile.position}")


if __name__ == "__main__":
    main(
        Canvas(900, 550),
        Environment(
            Tuple.vector(0, -0.1, 0),
            Tuple.vector(-0.01, 0, 0)
        ),
        Projectile(
            Tuple.point(0, 1, 0),
            Tuple.vector(1, 1.6, 0) * 5.45
        )
    )
