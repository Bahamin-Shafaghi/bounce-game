import math

from ball import Ball
import pygame

from consts import *


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
        elif math.sqrt((self.x - ball.x) ** 2 + (self.y - ball.y) ** 2) <= ball.r + self.r:
            v1 = pygame.math.Vector2(self.x, self.y)
            v2 = pygame.math.Vector2(ball.x, ball.y)
            nv = v2 - v1
            m1 = pygame.math.Vector2(ball.vx, ball.vy).reflect(nv)
            ball.vx, ball.vy = m1.x, m1.y
            re = "reflected"
        elif math.sqrt((self.x + self.length - ball.x) ** 2 + (self.y - ball.y) ** 2) <= ball.r + self.r:
            v1 = pygame.math.Vector2(self.x + self.length, self.y)
            v2 = pygame.math.Vector2(ball.x, ball.y)
            nv = v2 - v1
            m1 = pygame.math.Vector2(ball.vx, ball.vy).reflect(nv)
            ball.vx, ball.vy = m1.x, m1.y
            re = "reflected"

        return re
