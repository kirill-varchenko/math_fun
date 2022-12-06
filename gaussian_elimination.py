import copy
import itertools
from fractions import Fraction
from typing import Optional, TypeVar, Union

T = TypeVar("T", int, float, Fraction)


def augment(A: list[list[T]], B: list[list[T]]) -> list[list[T]]:
    return [list(itertools.chain(a_row, b_row)) for a_row, b_row in zip(A, B)]


def gaussian_elimination(
    M: list[list[T]], jordan: bool = False
) -> list[list[T]]:
    A = copy.deepcopy(M)
    n_rows = len(A)
    n_cols = len(A[0])

    def swap_rows(i: int, j: int) -> None:
        A[i], A[j] = A[j], A[i]

    def divide_row_by(i: int, by: T, j_from: int = 0) -> None:
        for j in range(j_from, n_cols):
            A[i][j] /= by

    def substract_row(
        i: int, i_from: int, mul: T = 1, j_from: int = 0
    ) -> None:
        for j in range(j_from, n_cols):
            A[i_from][j] -= A[i][j] * mul

    def find_pivot(i: int, j: int) -> tuple[T, int]:
        a_max = A[i][j]
        i_max = i
        for k in range(i, len(A)):
            if A[k][j] > a_max:
                a_max = A[k][j]
                i_max = k
        return a_max, i_max

    def find_leading(i: int) -> tuple[Optional[T], Optional[int]]:
        for j, a in enumerate(A[i]):
            if a != 0:
                return a, j
        return None, None

    pivot_row: int = 0
    pivot_col: int = 0

    while pivot_row < n_rows and pivot_col < n_cols:
        a_max, i_max = find_pivot(pivot_row, pivot_col)
        if a_max == 0:
            pivot_col += 1
            continue
        swap_rows(pivot_row, i_max)
        for i in range(pivot_row + 1, n_rows):
            f = A[i][pivot_col] / a_max
            A[i][pivot_col] = 0
            substract_row(pivot_row, i, mul=f, j_from=pivot_col + 1)
        pivot_row += 1
        pivot_col += 1

    if not jordan:
        return A

    if pivot_row >= n_rows:
        pivot_row = n_rows - 1
    while pivot_row >= 0:
        lead, j_lead = find_leading(pivot_row)

        if lead is not None and j_lead is not None:
            divide_row_by(pivot_row, lead, j_from=j_lead)
            for i in range(pivot_row):
                f = A[i][j_lead]
                substract_row(pivot_row, i, mul=f, j_from=j_lead)

        pivot_row -= 1

    return A
