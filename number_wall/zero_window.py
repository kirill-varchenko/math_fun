from __future__ import annotations

from dataclasses import dataclass
from typing import Generator

from number_wall.frame import Frame
from table import Cell, Direction, Table


@dataclass
class ZeroWindow:
    top_left: Cell
    bottom_right: Cell
    frame_top: Frame
    frame_left: Frame
    frame_right: Frame
    frame_bottom: Frame

    @classmethod
    def from_top_row(cls, row: int, col_left: int, col_right: int) -> ZeroWindow:
        col_delta = col_right - col_left
        top_left_frame_corner = Cell(row - 1, col_left - 1)
        bottom_right_frame_corder = Cell(row + col_delta + 1, col_right + 1)
        return cls(
            top_left=Cell(row, col_left),
            bottom_right=Cell(row + col_delta, col_right),
            frame_top=Frame(Direction.RIGHT, top_left_frame_corner, col_delta + 3),
            frame_left=Frame(Direction.DOWN, top_left_frame_corner, col_delta + 3),
            frame_right=Frame(Direction.UP, bottom_right_frame_corder, col_delta + 3),
            frame_bottom=Frame(
                Direction.LEFT, bottom_right_frame_corder, col_delta + 3
            ),
        )

    def __contains__(self, cell: Cell) -> bool:
        return (self.top_left.row <= cell.row <= self.bottom_right.row) and (
            self.top_left.col <= cell.col <= self.bottom_right.col
        )

    def iter_inside_region(self) -> Generator[Cell, None, None]:
        for i in range(self.top_left.row, self.bottom_right.row + 1):
            for j in range(self.top_left.col, self.bottom_right.col + 1):
                yield Cell(i, j)

    def calculate_factors(self, table: Table) -> None:
        self.frame_top.calculate_factor(table)
        self.frame_left.calculate_factor(table)
        self.frame_right.calculate_factor(table)

        if self.frame_top.factor and self.frame_left.factor and self.frame_right.factor:
            self.frame_bottom.factor = (
                self.frame_left.factor * self.frame_right.factor / self.frame_top.factor
            )
