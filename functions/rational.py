from __future__ import annotations

import itertools
import math
from fractions import Fraction

from functions.polynomial import Number, Polynomial


class Rational:
    """Rational function with rational coefficients."""

    def __init__(
        self,
        numerator: Polynomial | Number,
        denominator: Polynomial | None = None,
        cancel: bool = True,
    ) -> None:
        if denominator == 0:
            raise ZeroDivisionError

        if isinstance(numerator, Polynomial):
            self.numerator = numerator.copy()
        else:
            self.numerator = Polynomial(numerator)

        self.denominator = (
            denominator.copy()._truncate()
            if denominator is not None and self.numerator != 0
            else Polynomial(1)
        )

        if not cancel:
            return

        if self.numerator.degree > 0 and self.denominator.degree > 0:
            self.numerator, self.denominator, _ = self.numerator.get_coprimes_and_gcd(
                self.denominator
            )
        if self.denominator.degree == 0:
            factor = Fraction(1, self.denominator[0])
            self.numerator = Polynomial(*[factor * coeff for coeff in self.numerator])
            self.denominator = Polynomial(1)
        gcd = math.gcd(
            *[
                coeff.numerator if isinstance(coeff, Fraction) else coeff
                for coeff in itertools.chain(self.numerator, self.denominator)
            ]
        )
        if gcd != 1:
            self.numerator /= gcd
            self.denominator /= gcd

    def __repr__(self) -> str:
        return f"Rational({self.numerator!r},{self.denominator!r})"

    def __str__(self) -> str:
        if self.numerator == 0:
            return "0"
        if self.denominator == 1:
            return str(self.numerator)
        return f"({self.numerator})/({self.denominator})"

    @property
    def degree(self) -> tuple[int, int]:
        return self.numerator.degree, self.denominator.degree

    def to_integer(self) -> Rational:
        denominators = [
            coeff.denominator
            for coeff in itertools.chain(self.numerator, self.denominator)
            if isinstance(coeff, Fraction)
        ]
        factor = math.lcm(*denominators)
        return Rational(
            Polynomial(*[int(factor * coeff) for coeff in self.numerator]),
            Polynomial(*[int(factor * coeff) for coeff in self.denominator]),
            cancel=False,
        )

    def __mul__(self, other: Rational | Polynomial | Number) -> Rational:
        if isinstance(other, Number | Polynomial):
            other = Rational(other)
        if isinstance(other, Rational):
            return Rational(
                self.numerator * other.numerator, self.denominator * other.denominator
            )
        return NotImplemented

    __rmul__ = __mul__

    def __truediv__(self, other: Rational | Polynomial | Number) -> Rational:
        if other == 0:
            raise ZeroDivisionError
        if isinstance(other, Number | Polynomial):
            return Rational(self.numerator, self.denominator * other)
        if isinstance(other, Rational):
            return Rational(
                self.numerator * other.denominator, self.denominator * other.numerator
            )
        return NotImplemented

    def __rtruediv__(self, other: Rational | Polynomial | Number) -> Rational:
        return Rational(self.denominator, self.numerator, cancel=False) * other

    def __add__(self, other: Rational | Polynomial | Number) -> Rational:
        if isinstance(other, Number | Polynomial):
            other = Rational(other)
        if isinstance(other, Rational):
            if self.denominator == other.denominator:
                return Rational(self.numerator + other.numerator, self.denominator)
            Q1, Q2, gcd = self.denominator.get_coprimes_and_gcd(other.denominator)
            return Rational(self.numerator * Q2 + other.numerator * Q1, Q1 * Q2 * gcd)
        return NotImplemented

    __radd__ = __add__

    def __neg__(self) -> Rational:
        return Rational(-self.numerator, self.denominator, cancel=False)

    def __sub__(self, other: Rational | Polynomial | Number) -> Rational:
        if isinstance(other, Number | Polynomial):
            other = Rational(other)
        if isinstance(other, Rational):
            if self.denominator == other.denominator:
                return Rational(self.numerator - other.numerator, self.denominator)
            Q1, Q2, gcd = self.denominator.get_coprimes_and_gcd(other.denominator)
            return Rational(self.numerator * Q2 - other.numerator * Q1, Q1 * Q2 * gcd)
        return NotImplemented

    def __rsub__(self, other: Rational | Polynomial | Number) -> Rational:
        return (-1) * self + other

    def __pow__(self, order: int) -> Rational:
        return Rational(self.numerator**order, self.denominator**order)

    def __eq__(self, other: Rational | Polynomial | Number) -> bool:
        if isinstance(other, Rational):
            return (
                self.numerator == other.numerator
                and self.denominator == other.denominator
            )
        if self.denominator == 1:
            return self.numerator == other
        return False
