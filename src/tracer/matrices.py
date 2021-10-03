from collections import UserList


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
