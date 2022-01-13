from __future__ import annotations

from collections import UserList
from itertools import chain, product
from math import isclose, cos, sin

from .shared import EPSILON, number
from .tuples import Vector


__all__ = [
    "Matrix"
]


class Matrix(UserList):

    _size_map = {
        4: 2,
        9: 3,
        16: 4
    }

    identity: Matrix

    def __init__(self, *items):
        super().__init__(items)
        if not len(self) in self._size_map.keys():
            raise ValueError("Only supports square matrices.")
        self.size = self._size_map[len(self)]
        self._invertible = None

    def __getitem__(self, item):
        y, x = item
        return super().__getitem__(x + (y * self.size))

    def __eq__(self, other):
        if len(self) != len(other):
            return False
        return all(isclose(l, r, abs_tol=EPSILON) for l, r in zip(self, other))

    def __iter__(self):
        yield from self.data

    def __matmul__(self, other):
        if self.size != other.size:
            raise ValueError("Does not support multiplying different sized matrices.")
        values = []
        for x, y in product(range(self.size), range(self.size)):
            values.append(sum(v1 * v2 for v1, v2 in zip(self.row(x), other.column(y))))
        return Matrix(*values)

    def __mul__(self, _tuple: Vector):
        if self.size == 4:
            return Vector(*(_tuple.dot(row) for row in self.rows))
        else:
            return Vector(*(_tuple.dot(row) for row in self.rows), 0)

    @property
    def rows(self):
        for x in range(self.size):
            yield [*self.row(x)]

    def row(self, row):
        for y in range(self.size):
            yield self[row, y]

    @property
    def columns(self):
        for y in range(self.size):
            yield [*self.column(y)]

    def column(self, column):
        for x in range(self.size):
            yield self[x, column]

    def transpose(self) -> Matrix:
        return Matrix(*chain(*self.columns))

    def determinant(self):
        if self.size == 2:
            a, b, c, d = self.data
            return a * d - b * c
        return sum(v * self.cofactor(0, y) for y, v in enumerate(self.row(0)))

    def submatrix(self, row_index, column_index):
        return Matrix(
            *chain(
                *(
                    (
                        v
                        for i, v
                        in enumerate(row)
                        if i != column_index
                    )
                    for j, row
                    in enumerate(self.rows)
                    if j != row_index
                )
            )
        )

    def minor(self, row, column):
        return self.submatrix(row, column).determinant()

    def cofactor(self, row, column):
        return self.minor(row, column) * [1, -1][(row + column) % 2]

    @property
    def invertible(self):
        if self._invertible is None:
            self._invertible = bool(self.determinant())
        return self._invertible

    def inverse(self):
        cofactor_matrix = Matrix(*(
            self.cofactor(row, column)
            for row, column
            in product(range(self.size), range(self.size))
        ))
        determinate = self.determinant()
        return Matrix(*(v / determinate for v in cofactor_matrix.transpose()))

    def translate(self, x: number, y: number, z:number) -> Matrix:
        transform = Matrix(
            1, 0, 0, x,
            0, 1, 0, y,
            0, 0, 1, z,
            0, 0, 0, 1
        )
        return transform @ self

    def scale(self, x: number, y: number, z: number) -> Matrix:
        transform = Matrix(
            x, 0, 0, 0,
            0, y, 0, 0,
            0, 0, z, 0,
            0, 0, 0, 1
        )
        return transform @ self

    def rotate_x(self, radians: number) -> Matrix:
        transform = Matrix(
            1, 0, 0, 0,
            0, cos(radians), -sin(radians), 0,
            0, sin(radians), cos(radians), 0,
            0, 0, 0, 1
        )
        return transform @ self

    def rotate_y(self, radians: number) -> Matrix:
        transform = Matrix(
            cos(radians), 0, sin(radians), 0,
            0, 1, 0, 0,
            -sin(radians), 0, cos(radians), 0,
            0, 0, 0, 1
        )
        return transform @ self

    def rotate_z(self, radians: number) -> Matrix:
        transform = Matrix(
            cos(radians), -sin(radians), 0, 0,
            sin(radians), cos(radians), 0, 0,
            0, 0, 1, 0,
            0, 0, 0, 1
        )
        return transform @ self

    def shear(self, xy: number, xz: number, yx: number, yz: number, zx: number, zy: number) -> Matrix:
        transform = Matrix(
            1, xy, xz, 0,
            yx, 1, yz, 0,
            zx, zy, 1, 0,
            0, 0, 0, 1
        )
        return transform @ self

    @staticmethod
    def view(from_point: Vector, to_point: Vector, up_vector: Vector) -> Matrix:
        forward = (to_point - from_point).normalize()
        left = forward.cross(up_vector.normalize())
        true_up = left.cross(forward)
        orientation = Matrix(
            left.x, left.y, left.z, 0,
            true_up.x, true_up.y, true_up.z, 0,
            -forward.x, -forward.y, -forward.z, 0,
            0, 0, 0, 1
        )

        return orientation @ Matrix.identity.translate(-from_point.x, -from_point.y, -from_point.z)


Matrix.identity = Matrix(
    1, 0, 0, 0,
    0, 1, 0, 0,
    0, 0, 1, 0,
    0, 0, 0, 1
)
