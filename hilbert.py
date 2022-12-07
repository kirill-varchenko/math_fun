from enum import Enum
from typing import Generator, Union

import more_itertools

from lindenmayer import lindenmayer


class Move(Enum):
    LEFT = 1, 0
    RIGHT = -1, 0
    UP = 0, 1
    DOWN = 0, -1


def last2bits(value: int) -> int:
    return value & 3


def index2xy(idx: int, order: int) -> tuple[int, int]:
    x, y = ((0, 0), (0, 1), (1, 1), (1, 0))[last2bits(idx)]
    idx = idx >> 2

    n = 2
    n2 = 2
    while n <= order:
        l2b = last2bits(idx)
        if l2b == 0:
            x, y = y, x
        elif l2b == 1:
            y += n2
        elif l2b == 2:
            x += n2
            y += n2
        elif l2b == 3:
            x, y = 2 * n2 - 1 - y, n2 - 1 - x

        idx = idx >> 2
        n += 1
        n2 *= 2

    return x, y


def xy2index(x: int, y: int, order: int) -> int:
    n2 = 2 ** (order - 1)
    res = 0
    while n2 > 0:
        r = (int(x >= n2), int(y >= n2))
        res = res << 2
        if r == (0, 0):
            x, y = y, x
        elif r == (0, 1):
            res += 1
            y -= n2
        elif r == (1, 1):
            res += 2
            x -= n2
            y -= n2
        elif r == (1, 0):
            res += 3
            x -= n2
            x, y = n2 - y - 1, n2 - x - 1
        n2 //= 2

    return res


def iter_hilbert(max_order: int) -> Generator[list[tuple[int, int]], None, None]:
    """Iterate Hilbert curve coordinates by order via Lindenmayer system."""

    L_element_moves: dict[Union[str, tuple[str, str]], list[Move]] = {
        "A": [Move.UP, Move.RIGHT, Move.DOWN],
        "B": [Move.LEFT, Move.DOWN, Move.RIGHT],
        "C": [Move.RIGHT, Move.UP, Move.LEFT],
        "D": [Move.DOWN, Move.LEFT, Move.UP],
        ("A", "A"): [Move.RIGHT],
        ("A", "B"): [Move.DOWN],
        ("A", "C"): [Move.RIGHT],
        ("A", "D"): [Move.DOWN],
        ("B", "A"): [Move.RIGHT],
        ("B", "B"): [Move.DOWN],
        ("B", "C"): [Move.RIGHT],
        ("B", "D"): [Move.DOWN],
        ("C", "A"): [Move.UP],
        ("C", "B"): [Move.LEFT],
        ("C", "C"): [Move.UP],
        ("C", "D"): [Move.LEFT],
        ("D", "A"): [Move.UP],
        ("D", "B"): [Move.LEFT],
        ("D", "C"): [Move.UP],
        ("D", "D"): [Move.LEFT],
    }

    L_system = {
        "alphabet": "ABCD",
        "axiom": "A",
        "rules": {"A": "CAAB", "B": "DBBA", "C": "ACCD", "D": "BDDC"},
        "iterations": max_order - 1,
    }

    def move_coords(x: int, y: int, m: Move) -> tuple[int, int]:
        return x + m.value[0], y + m.value[1]

    def L2coords(L: str) -> list[tuple[int, int]]:
        x, y = 0, 0
        coords: list[tuple[int, int]] = [(x, y)]
        for el in more_itertools.interleave_longest(L, more_itertools.pairwise(L)):
            for move in L_element_moves[el]:
                x, y = move_coords(x, y, move)
                coords.append((x, y))

        return coords

    for L in lindenmayer(**L_system):
        yield L2coords(L)


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import numpy as np

    fig, axes = plt.subplots(2, 3)
    for i, H in enumerate(iter_hilbert(6)):
        row, col = divmod(i, 3)
        ax = axes[row][col]
        points = np.array(H)
        ax.plot(points[:, 0], points[:, 1], "-")
        ax.axis("equal")
        ax.axis("off")
    fig.tight_layout()
    plt.show()
