from .matrices import Matrix, number

__all__ = [
    "translation",
    "scaling",
    "rotation_x",
    "rotation_y",
    "rotation_z",
    "shearing"
]


def translation(x: number, y: number, z: number) -> Matrix:
    return Matrix.identity.translate(x, y, z)


def scaling(x: number, y: number, z: number) -> Matrix:
    return Matrix.identity.scale(x, y, z)


def rotation_x(radians: number) -> Matrix:
    return Matrix.identity.rotate_x(radians)


def rotation_y(radians: number) -> Matrix:
    return Matrix.identity.rotate_y(radians)


def rotation_z(radians: number) -> Matrix:
    return Matrix.identity.rotate_z(radians)


def shearing(xy: number, xz: number, yx: number, yz: number, zx: number, zy: number):
    return Matrix.identity.shear(xy, xz, yx, yz, zx, zy)
