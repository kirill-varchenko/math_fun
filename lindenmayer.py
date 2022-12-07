import re
from typing import Generator, Optional


def lindenmayer(
    alphabet: str, axiom: str, rules: dict[str, str], iterations: Optional[int] = None
) -> Generator[str, None, None]:
    """Lindenmayer system iterator.

    Parameters
    ----------
    alphabet : str
        Alphabet
    axiom : str
        Initial state of the system
    rules : dict[str, str]
        Production rules
    iterations : Optional[int], optional
        Number of iterations, None for endless

    Yields
    ------
    Generator[str, None, None]
        String of current state
    """

    def repl(m: re.Match) -> str:
        return rules.get(m.group(0), m.group(0))

    re_obj = re.compile(f"[{alphabet}]")

    i = 1
    S = axiom
    yield S

    while iterations is None or i <= iterations:
        S = re_obj.sub(repl, S)
        yield S
        i += 1


if __name__ == "__main__":
    print("Algae system:")
    for i, l in enumerate(lindenmayer("AB", "A", {"A": "AB", "B": "A"}, 5)):
        print(i, l)
