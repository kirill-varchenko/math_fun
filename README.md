# Math fun

## akiyama_tanigawa.py

Akiyama Tanigawa Transform (and inverse)
```
Sequence: 1 1/2 1/3 1/4 1/5 1/6 1/7 1/8 1/9
Akiyama Tanigawa transform (Bernoulli numbers): 1 1/2 1/6 0 -1/30 0 1/42 0 -1/30
Inverse Transform: 1 1/2 1/3 1/4 1/5 1/6 1/7 1/8 1/9
```

## gaussian_elimination.py

Gaussian(-Jordan) Elimination

## hilbert.py
`iter_hilbert` iterate Hilbert curve coordinates by order, `xy2index` gets index of a curve point from its coordinates, `index2xy` coordinates from index.

![Hilbert](hilbert.png)

## lindenmayer.py
Lindenmayer system iterator

```
Algae system:
0 A
1 AB
2 ABA
3 ABAAB
4 ABAABABA
5 ABAABABAABAAB
```

## pade_approximant.py

Calculate Padé approximant P/Q coefficients from Taylor series coefficients.

```
Taylor for exp(x): 1 1 1/2 1/6 1/24
P: 12 6 1
Q: 12 -6 1
```
