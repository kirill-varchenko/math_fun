from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable


class Direction(Enum):
    RIGHT = (0, 1)
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)


@dataclass(unsafe_hash=True, slots=True)
class Cell:
    row: int
    col: int

    def __getitem__(self, key: tuple[Direction, int] | Direction) -> Cell:
        n = key[1] if isinstance(key, tuple) else 1
        direction = key[0] if isinstance(key, tuple) else key
        return Cell(
            self.row + n * direction.value[0], self.col + n * direction.value[1]
        )

    def __add__(self, other: Cell | tuple[int, int]) -> Cell:
        if isinstance(other, Cell):
            return Cell(self.row + other.row, self.col + other.col)
        elif isinstance(other, tuple):
            return Cell(self.row + other[0], self.col + other[1])
        else:
            raise TypeError(other)

    def __rmul__(self, other: int) -> Cell:
        return Cell(other * self.row, other * self.col)


GetterFn = Callable[[tuple[int, int]], Any]
FillerFn = Callable[[int, int, GetterFn], Any]


class Empty:
    def __len__(self) -> int:
        return 0

    def __str__(self) -> str:
        return ""

    def __repr__(self) -> str:
        return "<empty>"

    def __format__(self, __format_spec: str) -> str:
        return "".__format__(__format_spec)

    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Empty)

    def _binary_op(self, __o: Any) -> Empty:
        return self

    __mul__ = _binary_op
    __truediv__ = _binary_op
    __pow__ = _binary_op
    __sub__ = _binary_op
    __add__ = _binary_op


empty = Empty()


class Table:
    def __init__(self, rows: int, cols: int, filler: FillerFn | None = None) -> None:
        self.rows = rows
        self.cols = cols
        self._table = [[empty for _ in range(cols)] for _ in range(rows)]

        if filler:
            for i in range(self.rows):
                for j in range(self.cols):
                    self._table[i][j] = filler(i, j, self.__getitem__)

    def __getitem__(self, key: tuple[int, int] | Cell):
        if isinstance(key, Cell):
            return self._table[key.row][key.col]
        return self._table[key[0]][key[1]]

    def __setitem__(self, key: tuple[int, int] | Cell, value):
        if isinstance(key, Cell):
            self._table[key.row][key.col] = value
            return
        self._table[key[0]][key[1]] = value

    def get_row(self, row):
        return self._table[row]

    def get_col(self, col):
        return [row[col] for row in self._table]

    def add_row(self, filler: FillerFn | None = None) -> None:
        self._table.append(
            [
                filler(self.rows, j, self.__getitem__) if filler else empty
                for j in range(self.cols)
            ]
        )
        self.rows += 1

    def truncate_rows(self, row: int) -> None:
        if row > self.rows or row < 0:
            return

        self._table = self._table[:row]
        self.rows = row

    def all_in_row(self, row: int, predicate: Callable[[Any], bool]) -> bool:
        return all(value == empty or predicate(value) for value in self._table[row])

    def truncate_zero_rows(self) -> None:
        all_zeros = [
            (i, self.all_in_row(i, lambda x: x == 0)) for i in range(self.rows)
        ]
        for i, is_zeros in reversed(all_zeros):
            if not is_zeros:
                self.truncate_rows(i + 1)
                break

    def __str__(self) -> str:
        if self.rows == 0 or self.cols == 0:
            return "<empty>"

        max_len_per_col = [
            max(len(str(self._table[i][j])) for i in range(self.rows))
            for j in range(self.cols)
        ]

        lines = []
        for row in self._table:
            lines.append(
                " ".join(
                    f"{str(value):>{max_len_per_col[j]}}" for j, value in enumerate(row)
                )
            )

        return "\n".join(lines)

    def to_tsv(self, filename: str) -> None:
        with open(filename, "w") as fo:
            for row in self._table:
                fo.write("\t".join(str(value) for value in row) + "\n")


# T = Table(5, 10, lambda i, j, _: i + j)
# T.add_row(lambda i, j, fn: fn((i - 1, j)) + 1)

# print(T)
