from __future__ import annotations

import itertools
from typing import Generator, cast

from computational_dag import ComputationalDAG
from iter_helpers import iter_consecutive_zeros
from number_wall.frame import WindowFrame
from number_wall.rules import (AbstractRule, CrossRule, HorseshoeInnerRule,
                               HorseshoeOuterRule, LongCrossRule,
                               UncomputableRule, ZeroRule)
from number_wall.zero_window import ZeroWindow
from table import Cell, Direction, GetterFn, Table, empty


class NumberWall:
    def __init__(self, sequence) -> None:
        self.sequence = sequence
        self.cols = len(sequence)
        self.rows = (self.cols + 1) // 2 + 2

        self.table = Table(self.rows, self.cols, self.initial_filler)
        self.dag = ComputationalDAG(
            precomputed_nodes=[Cell(i, j) for i in range(3) for j in range(self.cols)]
        )
        self.rules: dict[Cell, AbstractRule] = {}
        self.zero_windows: list[ZeroWindow] = []

    def initial_filler(self, i: int, j: int, T: GetterFn):
        if i == 0:
            return 0
        if i == 1:
            return 1
        if i == 2:
            return self.sequence[j]
        return empty

    def is_inside_table(self, cell: Cell) -> bool:
        return (0 <= cell.row <= 2 and 0 <= cell.col < self.cols) or (
            2 < cell.row < self.rows
            and cell.row - 2 <= cell.col <= self.cols - cell.row + 1
        )

    def iter_row(self, row: int) -> Generator[Cell, None, None]:
        for j in range(row - 2, self.cols - row + 2):
            yield Cell(row, j)

    def set_rule(self, cell: Cell, rule: AbstractRule) -> None:
        if not self.is_inside_table(cell):
            return
        for dependence in rule.get_dependencies():
            if not self.is_inside_table(dependence):
                return
        if cell in self.rules:
            return
        self.rules[cell] = rule
        self.dag.add_node(cell, rule.get_dependencies())

    def init_new_zero_window(self, row: int, col_left: int, col_right: int) -> None:
        zero_window = ZeroWindow.from_top_row(
            row=row, col_left=col_left, col_right=col_right
        )
        self.zero_windows.append(zero_window)
        zero_window.calculate_factors(self.table)

        # set zero rules inside window
        for cell in zero_window.iter_inside_region():
            if cell.row > row:
                self.set_rule(cell, ZeroRule())

        # set bottom inner frame rule
        forward = (
            True
            if self.is_inside_table(zero_window.frame_bottom.start)
            else False
            if self.is_inside_table(zero_window.frame_bottom.end)
            else None
        )
        if forward is None:
            for cell in itertools.chain(
                zero_window.frame_bottom.iter_cells(exclude_corners=True),
                zero_window.frame_bottom.iter_cells(WindowFrame.OUTER),
            ):
                self.set_rule(cell, UncomputableRule())
            return

        for cell in zero_window.frame_bottom.iter_cells(exclude_corners=True):
            self.set_rule(
                cell,
                HorseshoeInnerRule(cell, zero_window, forward),
            )

        # set bottom outer frame rule
        for cell in zero_window.frame_bottom.iter_cells(WindowFrame.OUTER):
            self.set_rule(
                cell,
                HorseshoeOuterRule(cell, zero_window),
            )

    def setup_row(self, row: int) -> None:
        for zeros in iter_consecutive_zeros(self.table.get_row(row)):
            if zeros[0] == zeros[1]:
                # single zero
                cell = Cell(row, zeros[0])[Direction.DOWN, 2]
                self.set_rule(cell, LongCrossRule(cell))
            else:
                # zero window
                for zero_window in self.zero_windows:
                    if Cell(row, zeros[0]) in zero_window:
                        break
                else:
                    self.init_new_zero_window(row, *zeros)

        for cell in self.iter_row(row + 1):
            self.set_rule(cell, CrossRule(cell))

    def build(self) -> None:
        for row in range(2, self.rows):
            if self.table.all_in_row(row, lambda x: x == 0):
                break
            self.setup_row(row)

            for label in self.dag.iter_computable_nodes():
                cell = cast(Cell, label)
                value = self.rules[cell](self.table)
                # if hasattr(value, "cancel"):
                #     value = value.cancel()
                self.table[cell] = value
                self.dag.done(cell)

        self.table.truncate_zero_rows()
        self.rows = self.table.rows

    def get_constant_element(self):
        last_row = [self.table[item] for item in self.iter_row(self.rows - 1)]
        if all(item == last_row[0] or -item == last_row[0] for item in last_row):
            return last_row[0]
