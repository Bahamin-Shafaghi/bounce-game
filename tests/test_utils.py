import math

import pygame
import pytest

from consts import backColor1, backColor2, mainColor
from obstacle import Obstacle
from utils import (circlePart, color_diff, compatible_color, draw_circle,
                   getV, good_colors, inAngle, isInCircle, isInRect,
                   random_color, suitableObs, sumRange)


@pytest.fixture
def surface():
    return pygame.Surface((200, 200))


def test_inAngle_zero_degrees():
    x, y = inAngle(0, (10, 20), 5)
    assert (round(x, 6), round(y, 6)) == (15.0, 20.0)


def test_inAngle_ninety_degrees():
    x, y = inAngle(90, (10, 20), 5)
    assert (round(x, 6), round(y, 6)) == (10.0, 25.0)


def test_inAngle_length_zero_returns_start():
    assert inAngle(37, (3, 4), 0) == (3.0, 4.0)


@pytest.mark.parametrize("pos", [(0, 0), (10, 5), (5, 0), (0, 5), (10, 0)])
def test_isInRect_inside_and_on_border(pos):
    assert isInRect((0, 0, 10, 5), pos) is True


@pytest.mark.parametrize("pos", [(-1, 2), (11, 2), (5, -1), (5, 6)])
def test_isInRect_outside(pos):
    assert isInRect((0, 0, 10, 5), pos) is False


def test_isInRect_respects_offset():
    rect = (10, 20, 5, 5)
    assert isInRect(rect, (12, 22)) is True
    assert isInRect(rect, (9, 22)) is False


def test_isInCircle_center_border_and_outside():
    assert isInCircle((0, 0), 5, (0, 0)) is True
    assert isInCircle((0, 0), 5, (3, 4)) is True
    assert isInCircle((0, 0), 5, (3, 5)) is False


def test_isInCircle_zero_radius():
    assert isInCircle((7, 7), 0, (7, 7)) is True
    assert isInCircle((7, 7), 0, (7, 8)) is False


def test_random_color_components_in_expected_levels():
    levels = set(range(64, 256, 32))
    for _ in range(50):
        color = random_color()
        assert len(color) == 3
        assert set(color) <= levels


def test_getV_returns_zero_on_zero_length():
    assert getV(10, 1, [5, 5], [5, 5], 2) == (0, 0)


def test_getV_pulls_towards_rest_length():
    # points 10 apart vertically, spring rest length 5 -> first point is pulled
    # towards the second one (positive y direction).
    vx, vy = getV(5, 1, [0, 0], [0, 10], m=1)
    assert vx == 0
    assert vy > 0


def test_getV_pushes_apart_when_compressed():
    vx, vy = getV(20, 1, [0, 0], [0, 10], m=1)
    assert vx == 0
    assert vy < 0


def test_getV_scales_inversely_with_mass():
    _, vy_light = getV(5, 1, [0, 0], [0, 10], m=1)
    _, vy_heavy = getV(5, 1, [0, 0], [0, 10], m=10)
    assert math.isclose(vy_light, vy_heavy * 10)


def test_getV_is_symmetric_in_both_axes():
    vx, vy = getV(5, 1, [0, 10], [0, 10], m=1)
    assert math.isclose(vx, vy)


def test_sumRange():
    assert sumRange(1, 4) == 10
    assert sumRange(3, 3) == 3
    assert sumRange(4, 3) == 0
    assert sumRange(-2, 2) == 0


def test_color_diff_identical_colors_is_zero():
    assert color_diff((10, 20, 30), (10, 20, 30)) == 0


def test_color_diff_is_mean_absolute_difference():
    assert color_diff((0, 0, 0), (3, 6, 9)) == 6
    assert color_diff((3, 6, 9), (0, 0, 0)) == 6


def test_compatible_color_rejects_close_color():
    assert compatible_color([(100, 100, 100)], (105, 100, 100)) is False


def test_compatible_color_accepts_distant_color():
    assert compatible_color([(100, 100, 100)], (200, 200, 200)) is True


def test_compatible_color_with_empty_palette():
    assert compatible_color([], (1, 2, 3)) is True


def test_good_colors_count_and_distinctness():
    colors = good_colors(3)
    assert len(colors) == 3
    reserved = [mainColor, backColor1, backColor2]
    for i, color in enumerate(colors):
        for other in reserved + colors[:i]:
            assert color_diff(color, other) >= 20


def test_good_colors_zero_is_empty():
    assert good_colors(0) == []


def test_suitableObs_empty_list():
    assert suitableObs([], (10, 10)) is True


def test_suitableObs_detects_horizontal_overlap():
    obstacle = Obstacle((100, 100), length=50)
    assert suitableObs([obstacle], (120, 400)) is False
    assert suitableObs([obstacle], (120, 100)) is False


def test_suitableObs_allows_position_beside_obstacle():
    obstacle = Obstacle((100, 100), length=50)
    assert suitableObs([obstacle], (100 - obstacle.r - 1, 100)) is True
    assert suitableObs([obstacle], (100 + 50 + obstacle.r + 1, 100)) is True


def test_draw_circle_fills_pixels(surface):
    draw_circle(surface, 100, 100, 10, (255, 0, 0))
    assert surface.get_at((100, 100))[:3] == (255, 0, 0)
    assert surface.get_at((100, 80))[:3] == (0, 0, 0)


def test_draw_circle_accepts_float_arguments(surface):
    draw_circle(surface, 50.7, 50.2, 5.9, (0, 255, 0))
    assert surface.get_at((50, 50))[:3] == (0, 255, 0)


def test_circlePart_draws_only_along_its_arc(surface):
    circlePart(90, 90, surface, (0, 0, 255), 50, (100, 100), 3)
    # arc starts at 0 degrees (90 - 90) and spans 90 degrees clockwise
    assert surface.get_at((150, 100))[:3] == (0, 0, 255)
    assert surface.get_at((100, 150))[:3] == (0, 0, 255)
    assert surface.get_at((50, 100))[:3] == (0, 0, 0)


def test_circlePart_zero_angle_draws_nothing(surface):
    circlePart(90, 0, surface, (0, 0, 255), 50, (100, 100), 3)
    assert surface.get_at((150, 100))[:3] == (0, 0, 0)
    assert surface.get_at((100, 150))[:3] == (0, 0, 0)
