import math
from random import randint, choice

# Colors
color_theme = 0x2fd034


# External Functions
def rSym():
    return choice(['+', '-'])


def getAlgebra():  # ax + b = cx + d -> x = (d - b) / (a - c)

    a = randint(1, 20)
    s1 = rSym()
    b = randint(1, 20)
    c = randint(1, 20)
    s2 = rSym()
    d = randint(1, 20)

    if s1 == "-":
        s1 = ""
        b *= -1
    if s2 == "-":
        s2 = ""
        d *= -1
    question = f"{a}x{s1}{b} = {c}x{s2}{d}"
    numerator = d - b
    denominator = a - c

    hcf = math.gcd(numerator, denominator)
    if hcf:
        numerator = numerator // hcf
        denominator = denominator // hcf

    if denominator < 0:
        denominator *= -1
        numerator *= -1

    solution = f'{numerator}/{denominator}'

    if denominator == 0:
        return getAlgebra()
    elif denominator == 1:
        solution = numerator

    if numerator == 0:
        solution = 0

    return question, solution
