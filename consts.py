import pygame
pygame.init()

PINK = (255, 0, 255)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
backColor1 = (47, 44, 56)
backColor2 = (7, 61, 61)
mainColor = (168, 165, 165)


def suitableSize(x, y):
    if x >= y:
        return "width should be less than height!"
    if not str.isdigit(x) or not str.isdigit(y):
        return "You should give integers!"
    return "good"


'''width = input("Please enter a size for width of game window: ")
height = input("Please enter a size for height of game window: ")
while suitableSize(width, height) != "good":
    print(suitableSize(width, height))
    width = input("Please enter a size for width of game window: ")
    height = input("Please enter a size for height of game window: ")

winSize = (int(width), int(height))'''
dis = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
winSize = (dis.get_rect()[2], dis.get_rect()[3])
