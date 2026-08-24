from utils import *
from consts import *
import helping
from ball import Ball
from level import new_level, spawn_obstacles


def aim_ball(ball, start, tar, v, obs, divisor):
    ball.setPos((start[0] + (pygame.mouse.get_pos()[0] - ball.x) / divisor,
                 start[1] + (pygame.mouse.get_pos()[1] - ball.y) / divisor), tar, v, obs)


start, colors, color, tar, ball = new_level(2, (10, -15))

font = pygame.font.Font(pygame.font.get_default_font(), round(winSize[1] / 24))

backColor = backColor1

bounce = pygame.mixer.Sound("media/bounce.mp3")
startSound = pygame.mixer.Sound("media/start.mp3")
lose = pygame.mixer.Sound("media/lose.mp3")
win = pygame.mixer.Sound("media/win.mp3")
score1 = pygame.image.load("media/score1.png")
score2 = pygame.image.load("media/score2.png")
s = round(winSize[1] / 24 + 10)
score1 = pygame.transform.scale(score1, (s, s))
score2 = pygame.transform.scale(score2, (s, s))

level = 1
rand, obs = spawn_obstacles(level)

done = False
pygame.mixer.init()

score = 0
highScore = 0
count = 0
numberToGO = 2
fps = 100

while not done:
    st = False
    clicked = False
    trans = 0
    vx = 0
    vy = 0
    pygame.mixer.music.load("media/before.mp3")
    pygame.mixer.music.play(loops=-1, fade_ms=1000)
    text = font.render(str(score), True, backColor)
    if backColor == backColor1:
        scoreImage = score1
    else:
        scoreImage = score2

    while not st:
        dis.fill(backColor)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                st = True
                done = True
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONUP:
                trans = 0
                if not isInCircle(start, round(winSize[1] / 24), pygame.mouse.get_pos()) and clicked:
                    st = True
                else:
                    ball.setPos(start, tar, (vx, vy), obs)
                    ball.clear()
                clicked = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if isInCircle(start, 15, pygame.mouse.get_pos()):
                    clicked = True
                    aim_ball(ball, start, tar, (vx, vy), obs, 4)
            if event.type == pygame.MOUSEMOTION:
                if bool(pygame.mouse.get_pressed()[0]):
                    if isInCircle(start, 15, pygame.mouse.get_pos()):
                        clicked = True
                        aim_ball(ball, start, tar, (vx, vy), obs, 4)
                    elif clicked:
                        trans = int((((pygame.mouse.get_pos()[0] - start[0]) ** 2 + (
                                    pygame.mouse.get_pos()[1] - start[1]) ** 2) ** 0.5) / 4 * 4.25)
                        if trans > 255:
                            trans = 255
                            scale = ((pygame.mouse.get_pos()[0] - start[0]) ** 2 + (
                                    pygame.mouse.get_pos()[1] - start[1]) ** 2) ** 0.5 / 60
                            aim_ball(ball, start, tar, (vx, vy), obs, scale)
                        else:
                            aim_ball(ball, start, tar, (vx, vy), obs, 4)

        vx, vy = getV(0, 5, [ball.x, start[0]], [ball.y, start[1]], ball.r - 3)
        pygame.draw.circle(dis, mainColor, start, round(winSize[1] / 41.7))
        surf = pygame.Surface((winSize[1] / 8, winSize[1] / 8), pygame.SRCALPHA)
        surf.set_alpha(trans)
        pygame.draw.circle(surf, (mainColor[0], mainColor[1], mainColor[2], trans), (winSize[1] / 16, winSize[1] / 16), winSize[1] / 16, width=3)
        tar.update()
        dis.blit(surf, (start[0] - winSize[1] / 16, start[1] - winSize[1] / 16))
        ball.draw(dis)
        tar.draw(dis)
        draw_score_hud(dis, text, scoreImage, s)
        if rand == 1:
            for ob in obs:
                ob.update(ball)
                ob.draw(dis)
        pygame.display.update()
        pygame.time.delay(13)
    pygame.mixer.music.fadeout(1000)
    startSound.play()
    ball = Ball((ball.x, ball.y), ball.color, ball.vx, ball.vy)
    ball.st = True
    st = False
    happen = "nothing"
    scoreRound = 1

    while not st:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                st = True
                done = True
        dis.fill(backColor)
        re = ball.update(tar, bounce, startSound)
        happen = re[0]
        reflected = re[1]
        tar.update()
        ball.draw(dis)
        if distance((ball.x, ball.y), ball.start) < ball.r + round(winSize[1] / 41.7)\
                and ball.released:
            ball.x, ball.y = ball.start
            ball = Ball(start, color, 10, -15)
            st = True
        if reflected:
            scoreRound += 1
        if happen == "lose":
            st = True
            done = True
        if happen == "win":
            st = True
        tar.draw(dis)
        pygame.draw.circle(dis, mainColor, start, round(winSize[1] / 41.7))
        draw_score_hud(dis, text, scoreImage, s)
        if rand == 1:
            for ob in obs:
                ha = ob.update(ball)
                if ha == "reflected":
                    scoreRound += 1
                    bounce.play()
                ob.draw(dis)
        pygame.display.update()
        pygame.time.delay(13)
    if happen == "win":
        win.play()
        score += scoreRound
        text = font.render(str(score), True, backColor)
        ball.x, ball.y = ball.start
        level += 1
        if ((level - 1) // 4) % 2 == 1:
            backColor = backColor2
        else:
            backColor = backColor1
        count += 1
        if count == numberToGO and numberToGO < 7:
            numberToGO += 1
            count = 1
        rand, obs = spawn_obstacles(level)
        alpha = helping.exitAll(dis, backColor, tar, ball, text, scoreRound, scoreImage)
        start, colors, color, tar, ball = new_level(numberToGO, (0, 0))
        helping.enterAll(dis, backColor, ball, tar, text, scoreRound, alpha, scoreImage)
    if happen == "lose":
        if level > 1:
            if score > highScore:
                highScore = score
            font = pygame.font.Font(pygame.font.get_default_font(), int(winSize[1] / 16))
            text = font.render("Game Over!", True, (255, 0, 0))
            text2 = font.render("Score: " + str(score), True, (255, 125, 0))
            text4 = font.render("High Score: " + str(highScore), True, (255, 125, 0))
            text3 = font.render("Retry!", True, (157, 0, 255))
            end = False
            passed = 0
            pygame.mixer.music.load("media/lose.mp3")
            pygame.mixer.music.play(start=2)
            while passed * 0.013 <= lose.get_length() + 3:
                dis.fill(backColor)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        end = True
                        done = True
                    elif event.type == pygame.MOUSEMOTION:
                        if isInRect(text3.get_rect(center=(winSize[0] / 2, winSize[1] - int(winSize[1] / 1.28))), event.pos):
                            text3 = font.render("Retry!", True, (206, 128, 255))
                        else:
                            text3 = font.render("Retry!", True, (157, 0, 255))
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        end = True
                        if not isInRect(text3.get_rect(center=(winSize[0] / 2, winSize[1] - int(winSize[1] / 1.28))), event.pos):
                            done = True
                        else:
                            done = False
                if end:
                    start, colors, color, tar, ball = new_level(2, (10, -15))

                    backColor = backColor1

                    level = 1
                    rand, obs = spawn_obstacles(level)
                    score = 0
                    count = 0
                    numberToGO = 2
                    font = pygame.font.Font(pygame.font.get_default_font(), int(winSize[1] / 24))
                    break

                change = int(winSize[1] / 13.7)
                text5 = font.render(str(round(lose.get_length() + 3 - passed * 0.013) + 1), True, (161, 184, 33))
                blit_center_x(dis, text, winSize[1] - int(winSize[1] / 1.88) - change)
                blit_center_x(dis, text2, winSize[1] - int(winSize[1] / 2.4) - change)
                blit_center_x(dis, text4, winSize[1] - int(winSize[1] / 3.3) - change)
                blit_center_x(dis, text5, winSize[1] - int(winSize[1] / 9.6) - change)
                blit_center_x(dis, text3, winSize[1] - int(winSize[1] / 1.37) - change)
                pygame.display.update()
                pygame.time.delay(13)
                passed += 1
        else:
            done = False
            ball = Ball(start, color, 10, -15)
            level = 1
pygame.quit()
exit()
