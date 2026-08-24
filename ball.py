import pygame.mixer

from utils import *

from target import Target


class Ball:
    def __init__(self, pos, color, vx, vy, start=None):
        if start is None:
            start = pos
        self.x = pos[0]
        self.y = pos[1]
        self.color = color
        self.vx = vx
        self.vy = vy
        self.a = 2
        self.r = int(winSize[1] / 64)
        self.backPos = []
        self.backSize = []
        self.wayBall = []
        self.m = 10
        self.start = start
        self.released = False
        self.st = False
        self.attention = False
        self.passed = False

    def setV(self, vx, vy):
        self.vx = vx
        self.vy = vy

    def clear(self):
        self.wayBall = []

    def clearBack(self):
        self.backSize = []
        self.backPos = []

    def start(self):
        self.st = True

    def update(self, tar: Target, bounce=pygame.mixer.Sound("media/bounce.mp3"), start=pygame.mixer.Sound("media/start.mp3"),
               play=True) -> tuple:
        reflect = False
        self.x += self.vx
        self.y += self.vy

        for i in range(len(self.backSize)):
            self.backSize[i] -= 0.2
        self.backPos.append(
            (random.randint(int(self.x) - self.r, int(self.x) + self.r), random.randint(int(self.y) - self.r,
                                                                                        int(self.y) + self.r)))
        self.backSize.append(self.r / 2)
        self.vy += 0.2
        if not math.sqrt((self.x - self.start[0]) ** 2 + (self.y - self.start[1]) ** 2) < self.r + int(
                winSize[1] / 41.7):
            if not self.released:
                self.attention = True
            self.passed = False
        else:
            if self.released:
                self.released = False
                (self.x, self.y) = self.start
            if self.attention:
                self.released = True
        if not self.st:
            self.released = False

        self.wayBall = []

        if self.x >= winSize[0] - self.r:
            self.x = winSize[0] - self.r
            self.vx *= -1
            self.passed = False
            reflect = True
            if play:
                bounce.play()
        if self.x <= self.r:
            self.x = self.r
            self.vx *= -1
            self.passed = False
            reflect = True
            if play:
                bounce.play()
        if self.y >= winSize[1] - self.r:
            if play:
                start.play()
            return "lose", reflect
        if self.y <= self.r:
            self.y = self.r
            self.vy *= -1
            self.passed = False
            reflect = True
            if play:
                bounce.play()
        if math.sqrt((self.x - tar.x) ** 2 + (self.y - tar.y) ** 2) <= round(winSize[1] / 32) + self.r:
            return "win", reflect

        if not self.passed:
            dx = self.x - tar.x
            dy = self.y - tar.y

            if (dx ** 2 + dy ** 2) ** 0.5 <= tar.r + self.r + round(winSize[1] / 192):
                angle = math.degrees(math.atan(abs(dy) / abs(dx)))
                if dx >= 0:
                    if dy >= 0:
                        angle += 90
                    else:
                        angle = 90 - angle
                else:
                    if dy >= 0:
                        angle = 270 - angle
                    else:
                        angle += 270
                if tar.getColorAngle(angle):
                    self.passed = True
                    return "win", reflect
                else:

                    if play:
                        bounce.play()
                    v1 = pygame.math.Vector2(self.x, self.y)
                    v2 = pygame.math.Vector2(tar.x, tar.y)
                    nv = v2 - v1
                    m1 = pygame.math.Vector2(self.vx, self.vy).reflect(nv)
                    self.vx, self.vy = m1.x, m1.y
                    return "reflected", reflect
        return "nothing", reflect

    def setPos(self, pos, tar, v, obs):
        self.x = pos[0]
        self.y = pos[1]
        self.vx = v[0]
        self.vy = v[1]
        for i in range(len(self.backSize)):
            self.backSize[i] -= 0.2
            self.backPos[i][0] = (self.backPos[0] - 0.1, self.backPos[1])
            self.backPos[i][1] = (self.backPos[0], self.backPos[1] - 1)
        self.backPos.append(
            (random.randint(int(self.x) - self.r, int(self.x) + self.r), random.randint(int(self.y) - self.r,
                                                                                        int(self.y) + self.r)))
        testBall = Ball(pos, self.color, self.vx, self.vy)
        self.wayBall = []
        for i in range(10):
            for j in range(2):
                for ob in obs:
                    ob.update(testBall)
                testBall.update(tar, play=False)
            self.wayBall.append((testBall.x, testBall.y))

    def draw(self, screen):
        for i in self.wayBall:
            pygame.draw.circle(screen, (168, 165, 165, 128), i, winSize[1] / 300)
        for i in range(len(self.backSize)):
            pygame.draw.circle(screen, (self.color[0], self.color[1], self.color[2], int(winSize[1] / 28)),
                               self.backPos[i], self.backSize[i])
        draw_circle(screen, int(self.x), int(self.y), self.r, self.color)
