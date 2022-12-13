import itertools
from typing import Generator, Iterable


def iter_2partitions(
    n: int, bounds: tuple[int | None, int | None] = (None, None)
) -> Generator[tuple[int, int], None, None]:
    i_bound, j_bound = (min(bound, n) if bound is not None else n for bound in bounds)
    for i in range(n - j_bound, i_bound + 1):
        yield i, n - i

def iter_consecutive_zeros(arr: Iterable) -> Generator[tuple[int, int], None, None]:
    idx = 0
    for key, sub in itertools.groupby(arr):
        ele = len(list(sub))
        if key == 0:
            yield (idx, idx + ele - 1)
        idx += ele
