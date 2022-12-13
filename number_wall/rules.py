from abc import ABC, abstractmethod
from typing import Any

from number_wall.frame import WindowFrame
from number_wall.zero_window import ZeroWindow
from table import Cell, Direction, Table, empty


class AbstractRule(ABC):
    @abstractmethod
    def __call__(self, table: Table) -> Any:
        """Evaluates cell value."""

    @abstractmethod
    def get_dependencies(self) -> list[Cell]:
        """List of cells to be evaluated before this rule."""


class CrossRule(AbstractRule):
    def __init__(self, cell: Cell) -> None:
        self.cell = cell
        self.center = self.cell[Direction.UP]

    def __repr__(self) -> str:
        return f"CrossRule({self.cell!r})"

    def __call__(self, table: Table) -> Any:
        return (
            table[self.center] ** 2
            - table[self.center[Direction.LEFT]] * table[self.center[Direction.RIGHT]]
        ) / table[self.center[Direction.UP]]

    def get_dependencies(self) -> list[Cell]:
        return [
            self.center,
            self.center[Direction.LEFT],
            self.center[Direction.RIGHT],
            self.center[Direction.UP],
        ]


class LongCrossRule(AbstractRule):
    def __init__(self, cell: Cell) -> None:
        self.cell = cell
        self.center = cell[Direction.UP, 2]

    def __repr__(self) -> str:
        return f"LongCrossRule({self.cell!r})"

    def __call__(self, table: Table) -> Any:
        return (
            table[self.center[Direction.RIGHT, 2]]
            * table[self.center[Direction.LEFT]] ** 2
            + table[self.center[Direction.LEFT, 2]]
            * table[self.center[Direction.RIGHT]] ** 2
            - table[self.center[Direction.UP, 2]]
            * table[self.center[Direction.DOWN]] ** 2
        ) / table[self.center[Direction.UP]] ** 2

    def get_dependencies(self) -> list[Cell]:
        return [
            self.center[Direction.RIGHT, 2],
            self.center[Direction.LEFT],
            self.center[Direction.LEFT, 2],
            self.center[Direction.RIGHT],
            self.center[Direction.UP, 2],
            self.center[Direction.DOWN],
            self.center[Direction.UP],
        ]


class ZeroRule(AbstractRule):
    def __repr__(self) -> str:
        return f"ZeroRule()"

    def __call__(self, table: Table) -> Any:
        return 0

    def get_dependencies(self) -> list[Cell]:
        return []


class UncomputableRule(AbstractRule):
    def __repr__(self) -> str:
        return f"UncomputableRule()"

    def __call__(self, table: Table) -> Any:
        return empty

    def get_dependencies(self) -> list[Cell]:
        return []


class HorseshoeInnerRule(AbstractRule):
    def __init__(
        self, cell: Cell, zero_window: ZeroWindow, forward: bool = True
    ) -> None:
        self.cell = cell
        self.forward = forward
        self.zero_window = zero_window

    def __repr__(self) -> str:
        return f"HorseshoeInnerRule({self.cell!r}, {self.forward})"

    def __call__(self, table: Table) -> Any:
        if self.forward:
            return (
                table[self.cell[Direction.RIGHT]] * self.zero_window.frame_bottom.factor
            )
        else:
            return (
                table[self.cell[Direction.LEFT]] / self.zero_window.frame_bottom.factor
            )

    def get_dependencies(self) -> list[Cell]:
        if self.forward:
            return [self.cell[Direction.RIGHT]]
        else:
            return [self.cell[Direction.LEFT]]


class HorseshoeOuterRule(AbstractRule):
    def __init__(self, cell: Cell, zero_window: ZeroWindow) -> None:
        self.cell = cell
        self.zero_window = zero_window
        self.n = zero_window.frame_bottom.get_outer_index(cell)

    def __repr__(self) -> str:
        return f"HorseshoeOuterRule({self.cell!r}, {self.n})"

    def __call__(self, table: Table) -> Any:
        return (
            (
                table[self.zero_window.frame_top.get_cell(self.n, WindowFrame.OUTER)]
                / table[self.zero_window.frame_top.get_cell(self.n)]
                * self.zero_window.frame_left.factor
                + (-1) ** self.n
                * table[self.zero_window.frame_left.get_cell(self.n, WindowFrame.OUTER)]
                / table[self.zero_window.frame_left.get_cell(self.n)]
                * self.zero_window.frame_top.factor
                - (-1) ** self.n
                * table[
                    self.zero_window.frame_right.get_cell(self.n, WindowFrame.OUTER)
                ]
                / table[self.zero_window.frame_right.get_cell(self.n)]
                * self.zero_window.frame_bottom.factor
            )
            * table[self.zero_window.frame_bottom.get_cell(self.n)]
            / self.zero_window.frame_right.factor
        )

    def get_dependencies(self) -> list[Cell]:
        return [
            self.zero_window.frame_top.get_cell(self.n, WindowFrame.OUTER),
            self.zero_window.frame_top.get_cell(self.n),
            self.zero_window.frame_left.get_cell(self.n, WindowFrame.OUTER),
            self.zero_window.frame_left.get_cell(self.n),
            self.zero_window.frame_right.get_cell(self.n, WindowFrame.OUTER),
            self.zero_window.frame_right.get_cell(self.n),
            self.zero_window.frame_bottom.get_cell(self.n),
        ]
