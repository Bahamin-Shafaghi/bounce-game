import math
import random

import pygame
import pygame.gfxdraw

from consts import *


def circlePart(start_angle, angle, screen, color, r, pos, width):
    for i in range(int(start_angle - 90), int(start_angle - 90) + int(angle)):
        i = i % 360
        draw_circle(screen, int(r * math.cos(math.radians(i)) + pos[0]), int(r * math.sin(math.radians(i)) + pos[1]),
                    width, color)


def inAngle(angle, start, length):
    x = start[0] + math.cos(math.radians(angle)) * length
    y = start[1] + math.sin(math.radians(angle)) * length

    return x, y


def draw_circle(surface, x, y, radius, color):
    pygame.gfxdraw.aacircle(surface, int(x), int(y), int(radius), color)
    pygame.gfxdraw.filled_circle(surface, int(x), int(y), int(radius), color)


def isInRect(rect, pos):
    if rect[0] <= pos[0] <= rect[0] + rect[2] and rect[1] <= pos[1] <= rect[1] + rect[3]:
        return True
    return False


def random_color():
    levels = range(64, 256, 32)
    return tuple(random.choice(levels) for _ in range(3))


def isInCircle(pos, r, isIn):
    if math.sqrt((isIn[0] - pos[0]) ** 2 + (isIn[1] - pos[1]) ** 2) <= r:
        return True
    return False


def getV(l0, k, arr_x, arr_y, m):
    arr_fy = [0, 0]
    arr_fx = [0, 0]
    try:
        l = math.sqrt((arr_y[1] - arr_y[0]) ** 2 + (arr_x[1] - arr_x[0]) ** 2)
        f = -k * (arr_y[1] - arr_y[0] - ((arr_y[1] - arr_y[0]) * (l0 / l)))
        f1 = -k * (arr_x[1] - arr_x[0] - ((arr_x[1] - arr_x[0]) * (l0 / l)))
        arr_fy[1] += f
        arr_fy[0] += -f
        arr_fx[1] += f1
        arr_fx[0] += -f1
        ay = arr_fy[0] / m
        vy = ay
        ax = arr_fx[0] / m
        vx = ax
        return vx, vy
    except ZeroDivisionError:
        return 0, 0


def sumRange(x, y):
    re = 0
    for i in range(x, y + 1):
        re += i
    return re


def color_diff(color1, color2):
    s = 0
    for i in range(3):
        s += abs(color1[i] - color2[i])
    return s / 3


def compatible_color(colors, color):
    for i in colors:
        if color_diff(i, color) < 20:
            return False
    return True


def good_colors(n):
    colors = [mainColor, backColor1, backColor2]
    for i in range(n):
        color = random_color()
        while not compatible_color(colors, color):
            color = random_color()
        colors.append(color)
    return colors[3:]


def suitableObs(obs, xy):
    for i in obs:
        if i.x - i.r <= xy[0] <= i.x + i.length + i.r:
            return False
    return True
