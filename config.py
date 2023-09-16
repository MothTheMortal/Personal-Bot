import math
from io import BytesIO
from random import randint, choice
import numpy as np
import matplotlib.pyplot as plt
import random


# Initialization
with open("word_data.txt", "r") as file:
    data = file.read()
    words = data.split("\n")


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


def getLinear():
    m = random.randint(-10, 10)
    while m == 0:
        m = random.randint(-10, 10)

    if m == 1:
        m = ""

    b = random.randrange(-20, 20)
    while b == 0:
        b = random.randrange(-20, 20)



    if b < 0:
        solution = f'y={m}x{b}'
    else:
        solution = f'y={m}x+{b}'
    print(solution)
    xmin, xmax, ymin, ymax = -10, 10, -10, 10
    ticks_frequency = 1

    fig, ax = plt.subplots(figsize=(10, 10))

    ax.set(xlim=(xmin - 1, xmax + 1), ylim=(ymin - 1, ymax + 1), aspect='equal')

    ax.spines['bottom'].set_position('zero')
    ax.spines['left'].set_position('zero')

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.set_xlabel('x', size=14, labelpad=-24, x=1.03)
    ax.set_ylabel('y', size=14, labelpad=-21, y=1.02, rotation=0)

    x_ticks = np.arange(xmin, xmax + 1, ticks_frequency)
    y_ticks = np.arange(ymin, ymax + 1, ticks_frequency)
    ax.set_xticks(x_ticks[x_ticks != 0])
    ax.set_yticks(y_ticks[y_ticks != 0])

    ax.set_xticks(np.arange(xmin, xmax + 1), minor=True)
    ax.set_yticks(np.arange(ymin, ymax + 1), minor=True)

    ax.grid(which='both', color='grey', linewidth=1, linestyle='-', alpha=0.2)

    arrow_fmt = dict(markersize=4, color='black', clip_on=False)
    ax.plot((1), (0), marker='>', transform=ax.get_yaxis_transform(), **arrow_fmt)
    ax.plot((0), (1), marker='^', transform=ax.get_xaxis_transform(), **arrow_fmt)

    x_values = np.linspace(xmin, xmax, 100)

    y_values = m * x_values + b

    ax.plot(x_values, y_values, label='Find the Linear equation!', color='blue')
    plt.legend()
    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)

    return buffer, solution


def getQuadratic():
    # a = random.randint(-5, 5)
    # while a == 0:
    #     a = random.randint(-5, 5)
    # b = random.randint(-10, 10)
    # while b == 0:
    #     b = random.randint(-10, 10)
    # c = random.randint(-10, 10)
    # while c == 0:
    #     c = random.randint(-10, 10)
    h = random.randint(-5,5)
    k = random.randint(-5,5)
    a = random.randint(-5,5)
    while a == 0:
        a = random.randint(-5,5)

    b = -2*a*h
    c = a*(h**2) + k
    

    
    


    

    

    if a == 1:
        a = ""
    equation = f'y={a}x^2'
    if b < 0:
        equation += f'-{-b}x'
    elif b == 1:
        equation += f'+x'
    else:
        equation += f'+{b}x'

    if c < 0:
        equation += f'-{-c}'
    else:
        equation += f'+{c}'

    print(equation)

    xmin, xmax, ymin, ymax = -10, 10, -10, 10
    ticks_frequency = 1
    fig, ax = plt.subplots(figsize=(10, 10))

    ax.set(xlim=(xmin - 1, xmax + 1), ylim=(ymin - 1, ymax + 1), aspect='equal')

    ax.spines['bottom'].set_position('zero')
    ax.spines['left'].set_position('zero')

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.set_xlabel('x', size=14, labelpad=-24, x=1.03)
    ax.set_ylabel('y', size=14, labelpad=-21, y=1.02, rotation=0)

    x_ticks = np.arange(xmin, xmax + 1, ticks_frequency)
    y_ticks = np.arange(ymin, ymax + 1, ticks_frequency)
    ax.set_xticks(x_ticks[x_ticks != 0])
    ax.set_yticks(y_ticks[y_ticks != 0])

    ax.set_xticks(np.arange(xmin, xmax + 1), minor=True)
    ax.set_yticks(np.arange(ymin, ymax + 1), minor=True)

    ax.grid(which='both', color='grey', linewidth=1, linestyle='-', alpha=0.2)

    arrow_fmt = dict(markersize=4, color='black', clip_on=False)
    ax.plot((1), (0), marker='>', transform=ax.get_yaxis_transform(), **arrow_fmt)
    ax.plot((0), (1), marker='^', transform=ax.get_xaxis_transform(), **arrow_fmt)

    x_values = np.linspace(xmin, xmax, 100)
    y_values = a * x_values ** 2 + b * x_values + c

    ax.plot(x_values, y_values, label="Find the quadratic equation!", color='blue')
    plt.legend()
    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)

    return buffer, equation


def getRandomWord():
    word = random.choice(words)

    letters = list(word.title())
    random.shuffle(letters)
    scrambledWord = "".join(letters)

    return word, scrambledWord
