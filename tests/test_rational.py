from fractions import Fraction

import pytest

from functions.polynomial import Polynomial
from functions.rational import Rational


def test_zero_division():
    with pytest.raises(ZeroDivisionError):
        Rational(1, Polynomial(0))
        Rational(1, Polynomial(1)) / 0
        Rational(1, Polynomial(1)) / Polynomial(0)

    
@pytest.mark.parametrize(
    "A,B,P_coeffs,Q_coeffs",
    [
        (
            Rational(Polynomial(1, 2), Polynomial(1, 3, 4)),
            Rational(Polynomial(1, -1), Polynomial(1, 3, 4)),
            [2, 1],
            [1, 3, 4],
        ),
        (
            Rational(Polynomial(1, 2), Polynomial(1, 3)),
            Rational(Polynomial(1, -1), Polynomial(1, 3, 4)),
            [2, 7, 7, 8],
            [1, 6, 13, 12],
        ),
        (
            Rational(Polynomial(1, 2), Polynomial(1, 3)),
            10,
            [11, 32],
            [1, 3],
        ),
        (
            Rational(Polynomial(1, 2), Polynomial(1, 3)),
            Polynomial(1, -1),
            [2, 4, -3],
            [1, 3],
        ),
    ],
)
def test_add(A, B, P_coeffs, Q_coeffs):
    C = A + B
    assert C.numerator.coefficients == P_coeffs
    assert C.denominator.coefficients == Q_coeffs

    
@pytest.mark.parametrize(
    "A,B,P_coeffs,Q_coeffs",
    [
        (
            Rational(Polynomial(1, 2), Polynomial(1, 3, 4)),
            Rational(Polynomial(1, -1), Polynomial(1, 3, 4)),
            [0, 3],
            [1, 3, 4],
        ),
        (
            Rational(Polynomial(1, 2), Polynomial(1, 3)),
            Rational(Polynomial(1, -1), Polynomial(1, 3, 4)),
            [0, 3, 13, 8],
            [1, 6, 13, 12],
        ),
        (
            Rational(Polynomial(1, 2), Polynomial(1, 3)),
            10,
            [-9, -28],
            [1, 3],
        ),
        (
            10,
            Rational(Polynomial(1, 2), Polynomial(1, 3)),
            [9, 28],
            [1, 3],
        ),
        (
            Rational(Polynomial(1, 2), Polynomial(1, 3)),
            Polynomial(1, -1),
            [0, 0, 3],
            [1, 3],
        ),
    ],
)
def test_sub(A, B, P_coeffs, Q_coeffs):
    C = A - B
    assert C.numerator.coefficients == P_coeffs
    assert C.denominator.coefficients == Q_coeffs


@pytest.mark.parametrize(
    "A,B,P_coeffs,Q_coeffs",
    [
        (
            Rational(Polynomial(1, 2), Polynomial(1, 3, 4)),
            Rational(Polynomial(1, -1), Polynomial(1, 3, 4)),
            [1, 1, -2],
            [1, 6, 17, 24, 16],
        ),
        (
            Rational(Polynomial(1, 2), Polynomial(1, 3)),
            10,
            [10, 20],
            [1, 3],
        ),
        (
            Rational(Polynomial(1, 2), Polynomial(1, 3)),
            Polynomial(1, -1),
            [1, 1, -2],
            [1, 3],
        ),
    ],
)
def test_mul(A, B, P_coeffs, Q_coeffs):
    C = A * B
    assert C.numerator.coefficients == P_coeffs
    assert C.denominator.coefficients == Q_coeffs


@pytest.mark.parametrize(
    "A,B,P_coeffs,Q_coeffs",
    [
        (
            Rational(Polynomial(1, 2), Polynomial(1, 3)),
            Rational(Polynomial(1, -1), Polynomial(1, 3)),
            [1, 2],
            [1, -1],
        ),
        (
            Rational(Polynomial(10, 20), Polynomial(1, 3)),
            5,
            [2, 4],
            [1, 3],
        ),
        (
            5,
            Rational(Polynomial(1, 2), Polynomial(1, 3)),
            [5, 15],
            [1, 2],
        ),
        (
            Rational(Polynomial(1, 2), Polynomial(1, 3)),
            Polynomial(1, -1),
            [1, 2],
            [1, 2, -3],
        ),
    ],
)
def test_truediv(A, B, P_coeffs, Q_coeffs):
    C = A / B
    assert C.numerator.coefficients == P_coeffs
    assert C.denominator.coefficients == Q_coeffs


@pytest.mark.parametrize(
    "A,P_coeffs,Q_coeffs",
    [
        (
            Rational(Polynomial(1, 2), Polynomial(1, 3)),
            [1, 2],
            [1, 3],
        ),
        (
            Rational(Polynomial(Fraction(1, 3), 2), Polynomial(1, 3)),
            [1, 6],
            [3, 9],
        ),
        (
            Rational(Polynomial(Fraction(1, 3), 2), Polynomial(1, Fraction(3, 2))),
            [2, 12],
            [6, 9],
        ),
    ],
)
def test_to_integer(A, P_coeffs, Q_coeffs):
    B = A.to_integer()
    assert B.numerator.coefficients == P_coeffs
    assert B.denominator.coefficients == Q_coeffs
    assert all(isinstance(coeff, int) for coeff in B.numerator.coefficients)
    assert all(isinstance(coeff, int) for coeff in B.denominator.coefficients)


def test_eq_zero():
    assert Rational(Polynomial(0), Polynomial(1, 1)) == 0

