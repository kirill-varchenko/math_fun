from functools import lru_cache


@lru_cache
def stirlingI(n: int, k: int) -> int:
    """Stirling number of the first kind"""

    if n < 0 or k < 0:
        return 0
    if n == 0 and k == 0:
        return 1
    if k == 0:
        return 0
    if k > n:
        return 0

    return -(n - 1) * stirlingI(n - 1, k) + stirlingI(n - 1, k - 1)


@lru_cache
def factorial(n: int) -> int:
    """Factorial"""

    if n == 0:
        return 1

    res = 1
    for i in range(2, n + 1):
        res *= i

    return res


@lru_cache
def falling_factorial(n: int, k: int) -> int:
    """Falling factorial"""

    if n == 0:
        return 1
    if k > n:
        return 0

    res = 1
    for i in range(n, n - k, -1):
        res *= i

    return res
