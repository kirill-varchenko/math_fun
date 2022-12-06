from fractions import Fraction


def akiyama_tanigawa(sequence: list) -> list[Fraction]:
    row = [Fraction(s) for s in sequence]
    first_col = [row[0]]
    for n in range(len(sequence), 1, -1):
        row = [(k + 1) * (row[k] - row[k + 1]) for k in range(n - 1)]
        first_col.append(row[0])

    return first_col


def akiyama_tanigawa_inv(sequence: list) -> list[Fraction]:
    row = [Fraction(s) for s in sequence]
    first_col = [row[0]]
    n = len(sequence) - 1
    for i in range(n):
        row = [row[k] - row[k + 1] * Fraction(1, i + 1) for k in range(n - i)]
        first_col.append(row[0])

    return first_col


if __name__ == "__main__":
    sequence = [Fraction(1, i) for i in range(1, 10)]
    at = akiyama_tanigawa(sequence)
    ati = akiyama_tanigawa_inv(at)
    
    print("Sequence:", *sequence)
    print("Akiyama Tanigawa transform (Bernoulli numbers):", *at)
    print("Inverse Transform:", *ati)
    