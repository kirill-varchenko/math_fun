from dataclasses import dataclass
from enum import Enum
from typing import Any, Generator

import more_itertools

from table import Cell, Direction, Table, empty

OUTER: dict[Direction, Direction] = {
    Direction.RIGHT: Direction.UP,
    Direction.LEFT: Direction.DOWN,
    Direction.UP: Direction.RIGHT,
    Direction.DOWN: Direction.LEFT,
}


class WindowFrame(Enum):
    INNER = 0
    OUTER = 1


@dataclass
class Frame:
    direction: Direction
    start: Cell
    length: int
    factor: Any = None

    def get_cell(self, idx: int, frame: WindowFrame = WindowFrame.INNER) -> Cell:
        if idx < 0 or idx >= self.length:
            raise ValueError("Index out of range")
        outer = OUTER[self.direction]
        return self.start[self.direction, idx][outer, frame.value]

    def get_outer_index(self, cell: Cell) -> int:
        n = (
            ((cell.row - self.start.row) * self.direction.value[0])
            if self.direction.value[1] == 0
            else ((cell.col - self.start.col) * self.direction.value[1])
        )

        if self.get_cell(n, WindowFrame.OUTER) != cell:
            raise ValueError("Cell is not on the outer frame")
        return n

    @property
    def end(self) -> Cell:
        return self.get_cell(self.length - 1)

    def iter_cells(
        self, frame: WindowFrame = WindowFrame.INNER, exclude_corners: bool = False
    ) -> Generator[Cell, None, None]:
        for idx in range(exclude_corners, self.length - exclude_corners):
            yield self.get_cell(idx, frame)

    def calculate_factor(self, table: Table) -> None:
        for p1, p2 in more_itertools.pairwise(self.iter_cells()):
            if table[p1] == empty or table[p2] == empty:
                continue
            self.factor = table[p2] / table[p1]
            return
