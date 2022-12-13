from fractions import Fraction
from itertools import pairwise

from functions.polynomial import Polynomial
from functions.rational import Rational
from number_wall.number_wall import NumberWall

if __name__ == "__main__":
    seq = [1, 1, 2, 4, 7, 13, 24, 44, 81, 149, 274, 504, 927, 1705]
    frac_seq = [Fraction(s) for s in seq]
    nw1 = NumberWall(frac_seq)
    nw1.build()
    print("Number wall")
    print(nw1.table)
    print()

    poly_seq = [
        Rational(Polynomial(Fraction(p[1]), Fraction(-p[0]))) for p in pairwise(seq)
    ]

    nw2 = NumberWall(poly_seq)
    nw2.build()
    print("Characteristic polynomial")
    print(nw2.get_constant_element().numerator)
