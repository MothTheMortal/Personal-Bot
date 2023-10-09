import math
from io import BytesIO
from random import randint, choice
import numpy as np
import matplotlib.pyplot as plt
import random
from PIL import Image


# Initialization
with open("word_data.txt", "r") as file:
    data = file.read()
    words = data.split("\n")


# Colors
color_theme = 0x2fd034
SkinColor = (185, 195)
Shade = (430, 250)
EarShade = (90, 130)
EyeColorLeft = (144, 198)
EyeColorRight = (283, 197)


# Channel Names
snipeName = "snipe_save"
introName = "member-introduction"


# External Functions


def concatenateIMG(Image1, Image2):
    emptyIMG = Image.new("RGB", (Image1.width + Image2.width, Image1.height))
    emptyIMG.paste(Image1, (0, 0))
    emptyIMG.paste(Image2, (Image1.width, 0))

    return emptyIMG


def IMGtoFile(Image, filename=None):

    if not filename:
        filename = "generated_image"

    IOFile = BytesIO()
    Image.save(IOFile, format="PNG")
    IOFile.seek(0)
    return discord.File(fp=IOFile, filename=filename + ".png")


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
    h = random.randint(-5, 5)
    k = random.randint(-5, 5)
    a = random.randint(-5, 5)
    while a == 0:
        a = random.randint(-5, 5)

    b = -2 * a * h
    c = a * (h ** 2) + k

    if a == 1:
        equation = f'y=x^2'
    else:
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


def RGBtoHSV(R, G, B):
    r = R / 255
    g = G / 255
    b = B / 255

    Cmax = max(r, g, b)
    Cmin = min(r, g, b)

    Cdelta = Cmax - Cmin

    V = Cmax

    if Cmax == Cmin:
        H = 0
    elif Cmax == r:
        H = 60 * (((g - b) / Cdelta) % 6)
    elif Cmax == g:
        H = 60 * (((b - r) / Cdelta) + 2)
    else:
        H = 60 * (((r - g) / Cdelta) + 4)

    if Cmax == 0:
        S = 0
    else:
        S = Cdelta / Cmax

    return H, S * 100, V * 100


def getRandomColor():
    # return randomcolor.RandomColor().generate()[0][1:].upper()
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)


def _HSVtoRGB(h, s, v):
    h /= 360
    s /= 100
    v /= 100

    if s == 0.0:
        return v, v, v
    i = int(h * 6.0)
    f = (h * 6.0) - i
    p = v * (1.0 - s)
    q = v * (1.0 - s * f)
    t = v * (1.0 - s * (1.0 - f))
    i = i % 6
    if i == 0:
        return v, t, p
    if i == 1:
        return q, v, p
    if i == 2:
        return p, v, t
    if i == 3:
        return p, q, v
    if i == 4:
        return t, p, v
    if i == 5:
        return v, p, q


def HSVtoRGB(h, s, v):
    R, G, B = _HSVtoRGB(h, s, v)
    return int(R * 255), int(G * 255), int(B * 255)


def getShade(H, S, V):
    if H >= 240:
        H -= 10

    elif H >= 60:
        H += 15

    elif H >= 0:
        H -= 10

    S += 10
    V -= 10

    if S > 90:
        S = 100

    if V == 0:
        H = 238
        S = 83
        V = 21
    return H, S if S <= 100 else 100, V if V >= 0 else 0


def getRandomEye(H):
    H = int(H)
    newH = random.randint(H - 40, H + 40)
    if newH < 0:
        newH = 360 + newH
    elif newH > 360:
        newH = newH - 360

    R, G, B = HSVtoRGB(newH, 59, 35)
    R, G, B = int(R), int(G), int(B)

    Eye = Image.open("sphealeye.png")

    ImageDraw.floodfill(Eye, EyeColorLeft, [R, G, B], thresh=50)
    ImageDraw.floodfill(Eye, EyeColorRight, [R, G, B], thresh=50)

    return Eye




def getShadeFromRGB(R, G, B):
    H, S, V = RGBtoHSV(R, G, B)

    H2, S2, V2 = getShade(H, S, V)

    R2, G2, B2 = HSVtoRGB(H2, S2, V2)
    return int(R2), int(G2), int(B2)


def RGBtoHex(rgb):
    r, g, b = rgb
    r = max(0, min(255, r))
    g = max(0, min(255, g))
    b = max(0, min(255, b))

    hex_color = f"#{r:02X}{g:02X}{b:02X}"

    return hex_color



def getRandomSpot(color=None):
    spots = ["spot_heart.png", "spot_circle.png", "spot_square.png", "spot_star.png"]
    spot = Image.open(random.choice(spots))

    if color:

        spot_color = HSVtoRGB(color[0], color[1], color[2])

        colored_spot = Image.new("RGBA", spot.size)
        for x in range(spot.width):
            for y in range(spot.height):

                pixel_color = spot.getpixel((x, y))
                alpha = pixel_color[3]

                if alpha > 0:
                    new_pixel_color = spot_color + (alpha,)
                    colored_spot.putpixel((x, y), new_pixel_color)
        return colored_spot
    else:
        return spot