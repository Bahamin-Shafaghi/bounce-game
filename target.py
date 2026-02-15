import pygame

from consts import *
from utils import circlePart, draw_circle

pygame.init()


class Target:
    def __init__(self, color_list, pos, moveTo=None, rotation=True, v=2):
        self.colorCount = len(color_list)
        self.colorList = color_list
        self.x = pos[0]
        self.y = pos[1]
        self.pos = pos
        if moveTo is None:
            moveTo = pos
        self.moveTo = moveTo
        self.inWay = 0
        self.xvel = 0
        self.yvel = 0
        self.finish = (self.x - (self.moveTo[0] - self.x), self.y - (self.moveTo[1] - self.y))
        self.rotation = rotation
        self.angle = 0
        self.r = winSize[1] / 12
        self.colorRanges = []
        self.length = 360 / self.colorCount
        for i in range(self.colorCount):
            self.colorRanges.append([self.length * i, ((i + 1) * self.length) - 10])
        self.colorRanges[-1][-1] = 360 - 10
        self.v = v

    def getColorAngle(self, angle):
        for j in range(int(self.colorRanges[0][0]), int(self.colorRanges[0][0]) + int(360 / self.colorCount)):
            j = j % 360
            if j == int(angle):
                return True
        return False

    def update(self, move=True):
        if self.rotation:
            self.angle += self.v
            for i in range(len(self.colorRanges)):
                self.colorRanges[i][0] += self.v
                self.colorRanges[i][1] += self.v

        if move:
            if self.inWay == 1:
                self.xvel += (self.moveTo[0] - self.x) * 0.008
                self.yvel += (self.moveTo[1] - self.y) * 0.008
                self.xvel *= 0.8
                self.yvel *= 0.8
                self.x += self.xvel
                self.y += self.yvel
                if (round(self.x), round(self.y)) == self.moveTo:
                    self.inWay = 0
            else:
                self.xvel += (self.finish[0] - self.x) * 0.008
                self.yvel += (self.finish[1] - self.y) * 0.008
                self.xvel *= 0.8
                self.yvel *= 0.8
                self.x += self.xvel
                self.y += self.yvel
                if (round(self.x), round(self.y)) == self.finish:
                    self.inWay = 1

    def draw(self, screen):
        for i in range(len(self.colorRanges)):
            ra1 = self.colorRanges[i][0]
            ra2 = 360 / self.colorCount - 10
            circlePart(ra1, ra2, screen, self.colorList[i], self.r, (self.x, self.y), round(winSize[1] / 192))
        draw_circle(screen, int(self.x), int(self.y), round(winSize[1] / 32), mainColor)
