from __future__ import annotations

from collections import UserList
from itertools import chain, product
from math import isclose

from .constants import EPSILON
from .tuples import Tuple


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

    def __mul__(self, _tuple: Tuple):
        return Tuple(*(_tuple.dot(row) for row in self.rows))

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
        a, b, c, d = self.data
        return a * d - b * c

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


Matrix.identity = Matrix(
    1, 0, 0, 0,
    0, 1, 0, 0,
    0, 0, 1, 0,
    0, 0, 0, 1
)
