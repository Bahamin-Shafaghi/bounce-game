import pygame
import pytest

from ball import Ball
from consts import winSize
from obstacle import Obstacle


@pytest.fixture
def obstacle():
    return Obstacle((100, 300), length=50)


def make_ball(pos, vx=0.0, vy=5.0):
    return Ball(pos, (255, 0, 0), vx, vy)


def test_init_stores_geometry():
    obstacle = Obstacle((10, 20), length=80)
    assert (obstacle.x, obstacle.y) == (10, 20)
    assert obstacle.pos == (10, 20)
    assert obstacle.length == 80
    assert obstacle.r == winSize[1] / 138


def test_init_default_length_is_50():
    assert Obstacle((0, 0)).length == 50


def test_update_reflects_vertically_on_top_hit(obstacle):
    ball = make_ball((125, 300), vx=3.0, vy=5.0)
    assert obstacle.update(ball) == "reflected"
    assert (ball.vx, ball.vy) == (3.0, -5.0)


def test_update_flips_upward_velocity_too(obstacle):
    ball = make_ball((125, 300), vy=-4.0)
    obstacle.update(ball)
    assert ball.vy == 4.0


def test_update_ignores_distant_ball(obstacle):
    ball = make_ball((600, 600), vx=1.0, vy=2.0)
    assert obstacle.update(ball) == "nothing"
    assert (ball.vx, ball.vy) == (1.0, 2.0)


def test_update_ignores_ball_just_above_the_bar(obstacle):
    ball = make_ball((125, 300 - obstacle.r - 1), vy=5.0)
    assert obstacle.update(ball) == "nothing"
    assert ball.vy == 5.0


def test_update_reflects_off_left_cap(obstacle):
    ball = make_ball((100 - obstacle.r, 300 - 2), vx=4.0, vy=1.0)
    assert obstacle.update(ball) == "reflected"


def test_update_reflects_off_right_cap(obstacle):
    ball = make_ball((100 + 50 + obstacle.r, 300 - 2), vx=-4.0, vy=1.0)
    assert obstacle.update(ball) == "reflected"


def test_cap_reflection_preserves_speed(obstacle):
    ball = make_ball((100 - obstacle.r, 300 - 3), vx=6.0, vy=-2.0)
    speed_before = pygame.math.Vector2(ball.vx, ball.vy).length()
    obstacle.update(ball)
    speed_after = pygame.math.Vector2(ball.vx, ball.vy).length()
    assert pytest.approx(speed_before, rel=1e-6) == speed_after


def test_update_is_stable_when_ball_sits_on_the_centre(obstacle):
    ball = make_ball((100, 300), vx=1.0, vy=1.0)
    # the bar check has priority over the left cap check
    assert obstacle.update(ball) == "reflected"
    assert (ball.vx, ball.vy) == (1.0, -1.0)


def test_draw_paints_the_bar(obstacle):
    surface = pygame.Surface(winSize)
    obstacle.draw(surface)
    assert surface.get_at((125, 300))[:3] != (0, 0, 0)
    assert surface.get_at((125, 100))[:3] == (0, 0, 0)
