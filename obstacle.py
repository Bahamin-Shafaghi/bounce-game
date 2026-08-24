from ball import Ball
import pygame

from consts import *
from utils import distance, reflect_off


class Obstacle:
    def __init__(self, pos, length=50):
        self.length = length
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
        self.r = winSize[1] / 138

    def draw(self, dis):
        for i in range(self.x, self.x + self.length + 1):
            pygame.draw.circle(dis, mainColor, (i, self.y), self.r)

    def update(self, ball: Ball):
        re = "nothing"
        if self.x <= ball.x <= self.x + self.length and self.y - self.r <= ball.y <= self.y + self.r:
            ball.vy *= -1
            re = "reflected"
        elif distance((self.x, self.y), (ball.x, ball.y)) <= ball.r + self.r:
            ball.vx, ball.vy = reflect_off(ball, (self.x, self.y))
            re = "reflected"
        elif distance((self.x + self.length, self.y), (ball.x, ball.y)) <= ball.r + self.r:
            ball.vx, ball.vy = reflect_off(ball, (self.x + self.length, self.y))
            re = "reflected"

        return re
