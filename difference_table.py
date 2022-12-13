from fractions import Fraction

from functions.polynomial import Polynomial
from number import factorial
from table import GetterFn, Table, empty


def build_difference_table(sequence: list) -> Table:
    def filler(i: int, j: int, T: GetterFn):
        if i == 0:
            return sequence[j]
        if j < n - i:
            return T((i - 1, j + 1)) - T((i - 1, j))
        return empty

    n = len(sequence)
    difference_table = Table(n, n, filler)
    difference_table.truncate_zero_rows()
    return difference_table

def make_newton_polynomial(differences) -> Polynomial:
    res = Polynomial()
    for i, difference in enumerate(differences):
        res += Fraction(difference, factorial(i)) * Polynomial.falling_factorial(i)

    return res

if __name__ == "__main__":
    DT = build_difference_table([i**2 for i in range(1, 10)])
    difference0 = DT.get_col(0)
    newton = make_newton_polynomial(difference0)
    continuation = [newton(i) for i in range(10, 15)]

    print(DT)
    print()
    print("Newton polynomial:", newton)
    print()
    print("Continuation:", *continuation)
