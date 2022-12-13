from fractions import Fraction

import pytest

from functions.polynomial import Polynomial


def test_create():
    P = Polynomial(1, 2, 3)
    assert P.coefficients == [1, 2, 3]
    assert P.degree == 2


def test_truncate():
    P = Polynomial(1, 2, 3, 0, 0)
    P._truncate()
    assert P.coefficients == [1, 2, 3]
    assert P.degree == 2


@pytest.mark.parametrize(
    "A,B,coeffs",
    [
        (Polynomial(1, 2), Polynomial(0, 3, 4), [1, 5, 4]),
        (Polynomial(1, 2), Polynomial(0, -2), [1]),
        (Polynomial(1, 2), Polynomial(-1, -2), [0]),
        (Polynomial(1, 2), 5, [6, 2]),
        (5, Polynomial(1, 2), [6, 2]),
    ],
)
def test_add(A, B, coeffs):
    C = A + B
    assert C.coefficients == coeffs


@pytest.mark.parametrize(
    "A,B,coeffs",
    [
        (Polynomial(1, 2), Polynomial(0, 3, 4), [1, -1, -4]),
        (Polynomial(1, 2), Polynomial(0, 2), [1]),
        (Polynomial(1, 2), Polynomial(1, 2), [0]),
        (Polynomial(1, 2), 5, [-4, 2]),
        (5, Polynomial(1, 2), [4, -2]),
    ],
)
def test_sub(A, B, coeffs):
    C = A - B
    assert C.coefficients == coeffs


@pytest.mark.parametrize(
    "A,B,coeffs",
    [
        (Polynomial(1, 2), Polynomial(0, 3, 4), [0, 3, 10, 8]),
        (Polynomial(1, 2), Polynomial(0, 2), [0, 2, 4]),
        (Polynomial(1, 2), 5, [5, 10]),
        (5, Polynomial(1, 2), [5, 10]),
        (0, Polynomial(1, 2), [0])
    ],
)
def test_mul(A, B, coeffs):
    C = A * B
    assert C.coefficients == coeffs

@pytest.mark.parametrize(
    "A,order,coeffs",
    [
        (Polynomial(1, 2), 2, [1, 4, 4]),
        (Polynomial(1, 2), 3, [1, 6, 12, 8]),
    ],
)
def test_pow(A, order, coeffs):
    B = A ** order
    assert B.coefficients == coeffs

@pytest.mark.parametrize(
    "A,coeffs",
    [
        (Polynomial(1, 2), [1, 2]),
        (Polynomial(1), [1]),
        (Polynomial(Fraction(2,3), Fraction(5,6)), [4, 5]),
        (Polynomial(Fraction(2,3), Fraction(5,4)), [8, 15]),
        (Polynomial(Fraction(2,3), 1), [2, 3]),
    ],
)
def test_to_integer(A, coeffs):
    B = A.to_integer()
    assert B.coefficients == coeffs
    assert all(isinstance(coeff, int) for coeff in B.coefficients)

@pytest.mark.parametrize(
    "A,B,coeffs",
    [
        (Polynomial(1, 2, 1), Polynomial(-1, 0, 1), [1, 1]),
    ],
)
def test_gcd(A, B, coeffs):
    C = A.gcd(B)
    assert C.coefficients == coeffs

def test_eq_zero():
    assert Polynomial(0) == 0
