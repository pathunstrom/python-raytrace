from collections import UserList
from itertools import product
from math import isclose

from .constants import EPSILON


class Matrix(UserList):
    _size_map = {
        4: 2,
        9: 3,
        16: 4
    }

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

    def row(self, row):
        for y in range(self.size):
            yield self[row, y]

    def column(self, column):
        for x in range(self.size):
            yield self[x, column]
