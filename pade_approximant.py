import math
from fractions import Fraction
from typing import Any

import gaussian_elimination as ge


def pade_approximant(
    taylor_coeffs: list[Any],
    num_degree: int,
    denom_degree: int,
    to_integer: bool = True,
) -> tuple[list, list]:
    """Calculate Padé approximant P/Q coefficients from Taylor series coefficients."""

    if num_degree + denom_degree > len(taylor_coeffs) - 1:
        raise ValueError(
            "Tailor series degree must be >= then sum of polynomial degrees"
        )

    T = [Fraction(t) for t in taylor_coeffs]

    A = [
        [
            -T[i - j + num_degree] if i - j + num_degree >= 0 else Fraction(0)
            for j in range(denom_degree)
        ]
        for i in range(denom_degree)
    ]
    t = [[T[i + num_degree + 1]] for i in range(denom_degree)]

    A_augmented = ge.augment(A, t)
    A_eliminated = ge.gaussian_elimination(A_augmented, jordan=True)

    Q = [row[-1] for row in A_eliminated]

    P = [T[i] for i in range(num_degree + 1)]

    for i in range(num_degree + 1):
        for j, q in enumerate(Q):
            P[i] += q * (T[i - j - 1] if i - j >= 1 else 0)

    if to_integer:
        lcm = math.lcm(*[p.denominator for p in P], *[q.denominator for q in Q])
        P = [(p * lcm).numerator for p in P]
        Q = [(q * lcm).numerator for q in Q]
    else:
        lcm = 1

    Q.insert(0, lcm)

    return P, Q


if __name__ == "__main__":
    T = [1, 1, "1/2", "1/6", "1/24"]
    P, Q = pade_approximant(T, 2, 2)
    print("Taylor for exp(x):", *T)
    print("P:", *P)
    print("Q:", *Q)
