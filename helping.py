from ball import Ball
from consts import *
from target import Target

v = 5
s = round(winSize[1] / 24 + 10)


def _draw_transition_frame(dis, back, ball, tar, text, score, alpha, scoreImage, pad_before_fill):
    if pad_before_fill:
        pygame.draw.circle(dis, mainColor, (ball.x, ball.y), round(winSize[1] / 41.7))
    dis.fill(back)
    if not pad_before_fill:
        pygame.draw.circle(dis, mainColor, (ball.x, ball.y), round(winSize[1] / 41.7))
    ball.draw(dis)
    tar.update(False)
    tar.draw(dis)
    f = pygame.font.Font(pygame.font.get_default_font(), int(winSize[1] / 16))
    t = f.render("+ " + str(score), True, (255, 255, 255, alpha))
    surf = pygame.Surface((winSize[0], t.get_rect()[3]), pygame.SRCALPHA)
    surf.set_alpha(alpha)
    pygame.draw.rect(surf, (72, 217, 50, alpha), (0, 0, winSize[0], t.get_rect()[3]), border_radius=15)
    surf.blit(t, ((winSize[0] / 2) - t.get_rect()[2] / 2, 0))
    dis.blit(surf, (0, (winSize[1] / 2) - t.get_rect()[3] / 2))
    draw_score_hud(dis, text, scoreImage, s)
    pygame.display.update()
    pygame.time.Clock().tick(100000)


def _advance_transition(ball, tar, v):
    tar.y += v
    ball.y += v
    ball.start = (ball.start[0], ball.start[1] + v)


def exitAll(dis: pygame.Surface, back, tar: Target, ball: Ball, text: pygame.Surface, score, scoreImage):
    ball.clearBack()
    repeat = round(int((winSize[1] + 4 - tar.y + tar.r) / v) / 255)
    alpha = 0
    for i in range(int((winSize[1] + 4 - tar.y + tar.r) / v)):
        _draw_transition_frame(dis, back, ball, tar, text, score, alpha, scoreImage, True)
        _advance_transition(ball, tar, v)
        if i % repeat == 0:
            alpha += 1
            if alpha > 255:
                alpha = 255
    return alpha


def enterAll(dis: pygame.Surface, back, ball: Ball, tar: Target, text: pygame.Surface, score, alpha, scoreImage):
    ball.y = -ball.r
    tar.y = ball.y - (tar.y - ball.y)
    repeat = round(int((winSize[1] + 1 - tar.y + tar.r) / v) / 255)
    for i in range(int((winSize[1] - int(winSize[1] / 3.69) + ball.r) / v)):
        _draw_transition_frame(dis, back, ball, tar, text, score, alpha, scoreImage, False)
        _advance_transition(ball, tar, v)
        if i % repeat == 0:
            alpha -= 1
            if alpha < 0:
                alpha = 0
