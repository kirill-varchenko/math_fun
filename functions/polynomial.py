from __future__ import annotations

import itertools
import math
import re
from fractions import Fraction

from iter_helpers import iter_2partitions
from number import stirlingI

Number = int | Fraction


class Polynomial:
    """Class for a polynomial with rational coefficients."""

    def __init__(self, *coefficients: Number) -> None:
        self.coefficients: list[Number] = [
            coefficient if isinstance(coefficient, int) else Fraction(coefficient)
            for coefficient in coefficients
        ]
        if not self.coefficients:
            self.coefficients.append(0)

    def __repr__(self) -> str:
        return "Polynomial(" + ",".join(str(coeff) for coeff in self.coefficients) + ")"

    def __str__(self) -> str:
        s = "".join(
            f"{'+' if coeff > 0 else '-'}{abs(coeff)}x^{power}"
            for power, coeff in enumerate(self.coefficients)
            if coeff != 0
        )
        s = re.sub(r"\^1(?!\d)", "", s, 1)  # Fix x^1
        s = re.sub(r"x\^0", "", s, 1)  # Fix x^0
        s = re.sub(r"(?<!\d)(1)x", "x", s)  # Remove 1 coeffs
        s = re.sub(r"(?<=.)([+-])", r" \g<1> ", s)  # Put spaces between signs
        s = re.sub(r"^\+", "", s, 1)  # Remove leading +
        if not s:
            return "0"
        return s

    def __getitem__(self, key: int) -> Number:
        return self.coefficients[key]

    def __iter__(self):
        return iter(self.coefficients)

    @property
    def degree(self) -> int:
        return len(self.coefficients) - 1

    def _truncate(self) -> Polynomial:
        """Remove leading zeros"""

        while len(self.coefficients) > 1 and self.coefficients[-1] == 0:
            self.coefficients.pop()

        return self

    def __call__(self, x: Number) -> Number:
        """Evaluate polynomial at a given point"""

        res = 0
        for coefficient in reversed(self.coefficients):
            res = coefficient + x * res
        return res

    def __add__(self, other: Polynomial | Number) -> Polynomial:
        if isinstance(other, Number):
            other = Polynomial(other)
        if isinstance(other, Polynomial):
            res = Polynomial(
                *[
                    coef1 + coef2
                    for coef1, coef2 in itertools.zip_longest(
                        self.coefficients, other.coefficients, fillvalue=0
                    )
                ]
            )
            res._truncate()
            return res
        return NotImplemented

    __radd__ = __add__

    def __neg__(self) -> Polynomial:
        return Polynomial(*[-coeff for coeff in self.coefficients])

    def __sub__(self, other: Polynomial | Number) -> Polynomial:
        if isinstance(other, Number):
            other = Polynomial(other)
        if isinstance(other, Polynomial):
            res = Polynomial(
                *[
                    coef1 - coef2
                    for coef1, coef2 in itertools.zip_longest(
                        self.coefficients, other.coefficients, fillvalue=0
                    )
                ]
            )
            res._truncate()
            return res
        return NotImplemented

    def __rsub__(self, other: Polynomial | Number) -> Polynomial:
        return (-1) * self + other

    def __mul__(self, other: Polynomial | Number) -> Polynomial:
        if other == 0:
            return Polynomial()
        if isinstance(other, Number):
            return Polynomial(*[other * coeff for coeff in self.coefficients])
        if isinstance(other, Polynomial):
            bounds = (self.degree, other.degree)
            return Polynomial(
                *[
                    sum(
                        self[i] * other[j]
                        for i, j in iter_2partitions(n, bounds=bounds)
                    )
                    for n in range(self.degree + other.degree + 1)
                ]
            )
        return NotImplemented

    __rmul__ = __mul__

    def __pow__(self, power: int) -> Polynomial:
        n = self.degree

        P = [self.coefficients[0] ** power]

        for k in range(1, power * n + 1):
            P.append(
                sum(
                    (power * (k - i) - i) * self.coefficients[k - i] * P[i]
                    for i in range(max(0, k - n), k)
                )
                / (k * self.coefficients[0])
            )

        if all(isinstance(coeff, int) for coeff in self.coefficients):
            P = [int(p) for p in P]

        return Polynomial(*P)

    def __truediv__(self, other: Number) -> Polynomial:
        if isinstance(other, Number):
            return Polynomial(
                *[Fraction(coefficient, other) for coefficient in self.coefficients]
            )
        return NotImplemented

    def __floordiv__(self, other: Polynomial) -> Polynomial:
        if not isinstance(other, Polynomial):
            return NotImplemented
        P, _ = divmod(self, other)
        return P

    def __mod__(self, other: Polynomial) -> Polynomial:
        if not isinstance(other, Polynomial):
            return NotImplemented
        _, Q = divmod(self, other)
        return Q

    def __divmod__(self, other: Polynomial) -> tuple[Polynomial, Polynomial]:
        dividend = self.coefficients.copy()
        quotient_degree = self.degree - other.degree
        if quotient_degree < 0:
            return Polynomial(), self

        quotient: list[Number] = [0] * (quotient_degree + 1)
        for k in range(quotient_degree + 1):
            d = Fraction(dividend[-k - 1], other.coefficients[-1])
            for i, c in enumerate(other.coefficients):
                dividend[quotient_degree - k + i] -= c * d
            quotient[-k - 1] = d

        Q = Polynomial(*quotient)
        D = Polynomial(*dividend)
        D._truncate()
        return Q, D

    def __eq__(self, other: Polynomial | Number) -> bool:
        if not isinstance(other, Polynomial):
            if self.degree != 0:
                return False
            return self.coefficients[0] == other

        if self.degree != other.degree:
            return False

        return all(
            coef1 == coef2
            for coef1, coef2 in zip(self.coefficients, other.coefficients)
        )

    def copy(self) -> Polynomial:
        return Polynomial(*self.coefficients.copy())

    def to_integer(self) -> Polynomial:
        denominators = [
            coeff.denominator
            for coeff in self.coefficients
            if isinstance(coeff, Fraction)
        ]
        factor = math.lcm(*denominators)
        return Polynomial(*[int(factor * coeff) for coeff in self.coefficients])

    def to_monic(self) -> Polynomial:
        factor = Fraction(1, self.coefficients[-1])
        return Polynomial(*[Fraction(coeff) * factor for coeff in self.coefficients])

    def gcd(self, other: Polynomial) -> Polynomial:
        a, b = self, other
        while b != 0:
            a, b = b, a % b
        return a.to_monic()

    def get_coprimes_and_gcd(
        self, other: Polynomial
    ) -> tuple[Polynomial, Polynomial, Polynomial]:
        gcd = self.gcd(other)
        return self // gcd, other // gcd, gcd

    def diff(self, order: int = 1) -> Polynomial:
        if order < 0:
            raise ValueError
        if order == 0:
            return self
        if order > self.degree:
            return Polynomial()

        falling_factorial = Polynomial.falling_factorial(order)
        return Polynomial(
            *[
                self.coefficients[k] * falling_factorial(k)
                for k in range(order, self.degree + 1)
            ]
        )

    def integral(
        self, order: int = 1, constants: list[Number] | None = None
    ) -> Polynomial:
        if order < 0:
            raise ValueError
        if order == 0:
            return self

        if constants is None:
            constants_part = [0] * order
        elif len(constants) != order:
            raise ValueError("Constants length must be equal to order")
        else:
            constants_part = []
            f = Fraction(1)
            for i, constant in enumerate(constants):
                f = f / i if i != 0 else f
                constants_part.append(f * constant)

        rising_factorial = Polynomial.rising_factorial(order)

        integral_part = [
            Fraction(coeff) / rising_factorial(k + 1)
            for k, coeff in enumerate(self.coefficients)
        ]
        return Polynomial(*constants_part, *integral_part)

    @classmethod
    def falling_factorial(cls, power: int) -> Polynomial:
        if power < 0:
            raise ValueError(power)
        return cls(*[stirlingI(power, k) for k in range(power + 1)])

    @classmethod
    def rising_factorial(cls, power: int) -> Polynomial:
        if power < 0:
            raise ValueError(power)
        return cls(*[abs(stirlingI(power, k)) for k in range(power + 1)])
