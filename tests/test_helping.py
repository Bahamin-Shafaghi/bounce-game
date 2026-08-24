import pygame
import pytest

import helping
from ball import Ball
from consts import backColor1, winSize
from target import Target

COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]


@pytest.fixture
def scene():
    display = pygame.Surface(winSize)
    target = Target(COLORS, (400, 100), rotation=False)
    ball = Ball((400, 500), COLORS[0], 0, 0)
    font = pygame.font.Font(pygame.font.get_default_font(), 20)
    text = font.render("level 1", True, (0, 0, 0))
    score_image = pygame.Surface((helping.s, helping.s))
    return display, target, ball, text, score_image


def test_module_constants():
    assert helping.v == 5
    assert helping.s == round(winSize[1] / 24 + 10)


def test_exitAll_scrolls_the_scene_and_fades_in(scene):
    display, target, ball, text, score_image = scene
    steps = int((winSize[1] + 4 - target.y + target.r) / helping.v)

    alpha = helping.exitAll(display, backColor1, target, ball, text, 3, score_image)

    assert 0 < alpha <= 255
    assert ball.y == 500 + steps * helping.v
    assert ball.start == (400, 500 + steps * helping.v)
    assert target.y == 100 + steps * helping.v
    assert ball.backPos == [] and ball.backSize == []


def test_enterAll_scrolls_the_scene_back_and_fades_out(scene):
    display, target, ball, text, score_image = scene
    steps = int((winSize[1] - int(winSize[1] / 3.69) + ball.r) / helping.v)
    # both sprites are teleported above the screen, the target keeping its
    # distance to the ball mirrored around the ball's new position
    expected_ball_y = -ball.r + steps * helping.v
    expected_target_y = -ball.r - (target.y + ball.r) + steps * helping.v

    helping.enterAll(display, backColor1, ball, target, text, 3, 255, score_image)

    assert ball.y == expected_ball_y
    assert target.y == expected_target_y


def test_enterAll_keeps_alpha_within_bounds(scene):
    display, target, ball, text, score_image = scene
    # a zero starting alpha must not underflow while fading out
    helping.enterAll(display, backColor1, ball, target, text, 0, 0, score_image)
    assert display.get_at((0, 0))[:3] == backColor1
