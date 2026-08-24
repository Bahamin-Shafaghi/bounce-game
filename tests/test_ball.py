import math

import pygame
import pytest

from ball import Ball
from consts import winSize
from obstacle import Obstacle
from target import Target

COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
CENTER_R = round(winSize[1] / 32)
RING_TOLERANCE = round(winSize[1] / 192)


@pytest.fixture
def target():
    return Target(COLORS, (400, 300), rotation=False)


def make_ball(pos=(400, 600), vx=0.0, vy=0.0, start=None):
    return Ball(pos, COLORS[0], vx, vy, start=start)


def update(ball, target):
    return ball.update(target, play=False)


def test_init_defaults():
    ball = make_ball((100, 200), vx=3, vy=-4)
    assert (ball.x, ball.y) == (100, 200)
    assert (ball.vx, ball.vy) == (3, -4)
    assert ball.color == COLORS[0]
    assert ball.r == int(winSize[1] / 64)
    assert ball.m == 10
    assert ball.start == (100, 200)
    assert ball.released is False
    assert ball.st is False
    assert ball.attention is False
    assert ball.passed is False
    assert ball.backPos == [] and ball.backSize == [] and ball.wayBall == []


def test_init_with_explicit_start():
    ball = make_ball((100, 200), start=(10, 20))
    assert ball.start == (10, 20)


def test_setV_replaces_velocity():
    ball = make_ball()
    ball.setV(7, -8)
    assert (ball.vx, ball.vy) == (7, -8)


def test_clear_empties_predicted_way():
    ball = make_ball()
    ball.wayBall = [(1, 2)]
    ball.clear()
    assert ball.wayBall == []


def test_clearBack_empties_trail():
    ball = make_ball()
    ball.backPos = [(1, 2)]
    ball.backSize = [3]
    ball.clearBack()
    assert ball.backPos == [] and ball.backSize == []


def test_update_applies_velocity_then_gravity(target):
    ball = make_ball((400, 500), vx=3, vy=-5)
    assert update(ball, target) == ("nothing", False)
    assert (ball.x, ball.y) == (403, 495)
    assert ball.vy == pytest.approx(-4.8)
    assert ball.vx == 3


def test_update_grows_and_shrinks_the_trail(target):
    ball = make_ball((400, 500), vy=-5)
    update(ball, target)
    update(ball, target)
    assert len(ball.backPos) == len(ball.backSize) == 2
    assert ball.backSize[0] == pytest.approx(ball.r / 2 - 0.2)
    assert ball.backSize[1] == pytest.approx(ball.r / 2)


def test_update_trail_positions_stay_near_the_ball(target):
    ball = make_ball((400, 500), vy=-5)
    for _ in range(5):
        update(ball, target)
    for (x, y) in ball.backPos:
        assert abs(x - ball.x) <= 5 * abs(ball.vy) + ball.r
        assert abs(y - ball.y) <= 5 * abs(ball.vy) + ball.r


def test_update_bounces_off_right_wall(target):
    ball = make_ball((winSize[0] - 15, 400), vx=10, vy=-5)
    result, reflect = update(ball, target)
    assert (result, reflect) == ("nothing", True)
    assert ball.x == winSize[0] - ball.r
    assert ball.vx == -10


def test_update_bounces_off_left_wall(target):
    ball = make_ball((15, 400), vx=-10, vy=-5)
    result, reflect = update(ball, target)
    assert (result, reflect) == ("nothing", True)
    assert ball.x == ball.r
    assert ball.vx == 10


def test_update_bounces_off_ceiling(target):
    ball = make_ball((400, 15), vy=-10)
    result, reflect = update(ball, target)
    assert (result, reflect) == ("nothing", True)
    assert ball.y == ball.r
    assert ball.vy == pytest.approx(9.8)


def test_update_returns_lose_at_the_floor(target):
    ball = make_ball((400, winSize[1] - 20), vy=10)
    result, _ = update(ball, target)
    assert result == "lose"


def test_update_returns_win_when_hitting_the_center(target):
    ball = make_ball((target.x + CENTER_R + 5, target.y))
    result, _ = update(ball, target)
    assert result == "win"


def test_update_returns_win_through_matching_color(target):
    # 90 degrees (right of the target) lies inside the first color slice
    ball = make_ball((target.x + target.r + 12 + RING_TOLERANCE, target.y))
    assert update(ball, target) == ("win", False)
    assert ball.passed is True


def test_update_reflects_off_non_matching_color(target):
    target.colorRanges[0][0] = 120
    ball = make_ball((target.x + target.r + 12 + RING_TOLERANCE, target.y),
                     vx=-6, vy=0)
    result, _ = update(ball, target)
    assert result == "reflected"
    assert ball.vx > 0


def test_ring_reflection_preserves_speed(target):
    target.colorRanges[0][0] = 120
    ball = make_ball((target.x + target.r + 12 + RING_TOLERANCE, target.y),
                     vx=-6, vy=2)
    before = math.hypot(ball.vx, ball.vy + 0.2)
    update(ball, target)
    assert math.hypot(ball.vx, ball.vy) == pytest.approx(before, rel=1e-6)


def test_update_does_not_recheck_the_ring_once_passed(target):
    target.colorRanges[0][0] = 120
    ball = make_ball((target.x + target.r + 12 + RING_TOLERANCE, target.y))
    ball.passed = True
    assert update(ball, target) == ("nothing", False)


def test_wall_bounce_resets_passed(target):
    ball = make_ball((winSize[0] - 15, 400), vx=10)
    ball.passed = True
    update(ball, target)
    assert ball.passed is False


def test_leaving_the_launch_pad_sets_attention(target):
    ball = make_ball((400, 500), start=(400, 700))
    update(ball, target)
    assert ball.attention is True
    assert ball.released is False


def test_returning_to_the_launch_pad_resets_the_ball(target):
    start = (400, 500)
    ball = make_ball(start, start=start)
    ball.st = True

    ball.x, ball.y = 400, 300
    update(ball, target)
    assert ball.attention is True

    ball.x, ball.y = start
    update(ball, target)
    assert ball.released is True

    ball.x, ball.y = 401, 501
    update(ball, target)
    assert (ball.x, ball.y) == start


def test_release_is_suppressed_while_not_started(target):
    start = (400, 500)
    ball = make_ball(start, start=start)
    ball.attention = True
    update(ball, target)
    assert ball.released is False


def test_setPos_updates_state_and_predicts_a_path(target):
    ball = make_ball((400, 600))
    obstacles = [Obstacle((200, 400))]
    ball.setPos((300, 650), target, (5, -12), obstacles)
    assert (ball.x, ball.y) == (300, 650)
    assert (ball.vx, ball.vy) == (5, -12)
    assert len(ball.wayBall) == 10
    assert len(ball.backPos) == 1


def test_setPos_prediction_follows_the_initial_direction(target):
    ball = make_ball((400, 600))
    ball.setPos((400, 600), target, (5, -12), [])
    first_x, first_y = ball.wayBall[0]
    assert first_x > 400
    assert first_y < 600


def test_setPos_does_not_move_the_real_ball_along_the_prediction(target):
    ball = make_ball((400, 600))
    ball.setPos((400, 600), target, (0, -10), [])
    assert (ball.x, ball.y) == (400, 600)


@pytest.mark.xfail(raises=TypeError, strict=True,
                   reason="setPos indexes the trail tuples incorrectly")
def test_setPos_with_existing_trail(target):
    ball = make_ball((400, 600))
    update(ball, target)
    ball.setPos((300, 650), target, (5, -12), [])


def test_draw_paints_ball_and_trail(target):
    surface = pygame.Surface(winSize)
    ball = make_ball((400, 500), vy=-5)
    update(ball, target)
    ball.wayBall = [(400, 480), (400, 460)]
    ball.draw(surface)
    assert surface.get_at((400, 500))[:3] == COLORS[0]
    assert surface.get_at((400, 480))[:3] != (0, 0, 0)
