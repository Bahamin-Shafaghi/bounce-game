import random

from ball import Ball
from consts import *
from obstacle import Obstacle
from target import Target
from utils import good_colors, random_play_x, suitableObs


def spawn_obstacles(level):
    rand = random.randint(1, 11 - min(10, level))
    if rand == 1:
        num = random.randint(1, 3)
        obs = []
        for i in range(num):
            xy = (random_play_x(), round(winSize[1] - winSize[1] / 1.95))
            while not suitableObs(obs, xy):
                xy = (random_play_x(), round(winSize[1] - winSize[1] / 1.95))
            obs.append(Obstacle(xy))
    else:
        obs = [Obstacle((1000, 1000))]
    return rand, obs


def new_level(color_count, ball_velocity):
    start = (random_play_x(), winSize[1] - round(winSize[1] / 3.7))
    colors = good_colors(color_count)
    color = colors[0]
    movement = random.randint(15, 25)
    xy = (random_play_x(), random.randint(int(winSize[1] / 6.4), int(winSize[1] / 3.2)))
    tar = Target(colors, xy, (xy[0] + movement * 2, xy[1] + movement))
    ball = Ball(start, color, *ball_velocity)
    return start, colors, color, tar, ball
