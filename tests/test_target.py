import pygame
import pytest

from consts import winSize
from target import Target

COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]


@pytest.fixture
def target():
    return Target(COLORS, (400, 200))


def test_init_geometry_and_defaults(target):
    assert (target.x, target.y) == (400, 200)
    assert target.colorCount == 3
    assert target.colorList == COLORS
    assert target.r == winSize[1] / 12
    assert target.rotation is True
    assert target.v == 2
    assert target.angle == 0
    assert target.inWay == 0


def test_init_without_moveTo_stays_in_place(target):
    assert target.moveTo == (400, 200)
    assert target.finish == (400, 200)


def test_init_finish_mirrors_moveTo():
    target = Target(COLORS, (100, 100), moveTo=(130, 120))
    assert target.finish == (70, 80)


def test_color_ranges_split_the_circle_with_gaps():
    target = Target(COLORS, (0, 0))
    assert target.length == 120
    assert target.colorRanges[0] == [0, 110]
    assert target.colorRanges[1] == [120, 230]
    assert target.colorRanges[2] == [240, 350]


def test_color_ranges_for_single_color():
    target = Target([(1, 2, 3)], (0, 0))
    assert target.colorRanges == [[0, 350]]


def test_getColorAngle_inside_first_slice(target):
    assert target.getColorAngle(0) is True
    assert target.getColorAngle(119) is True


def test_getColorAngle_outside_first_slice(target):
    assert target.getColorAngle(120) is False
    assert target.getColorAngle(200) is False


def test_getColorAngle_wraps_around_after_rotation(target):
    target.colorRanges[0][0] = 300
    assert target.getColorAngle(350) is True
    assert target.getColorAngle(30) is True
    assert target.getColorAngle(60) is False


def test_update_rotates_angle_and_ranges(target):
    before = [list(r) for r in target.colorRanges]
    target.update(move=False)
    assert target.angle == 2
    for old, new in zip(before, target.colorRanges):
        assert new == [old[0] + 2, old[1] + 2]


def test_update_without_rotation_keeps_ranges():
    target = Target(COLORS, (0, 0), rotation=False)
    before = [list(r) for r in target.colorRanges]
    target.update(move=False)
    assert target.angle == 0
    assert target.colorRanges == before


def test_update_move_false_keeps_position(target):
    target.update(move=False)
    assert (target.x, target.y) == (400, 200)


def test_update_moves_towards_finish_then_reverses():
    target = Target(COLORS, (200, 200), moveTo=(240, 220))
    for _ in range(400):
        target.update()
        if target.inWay == 1:
            break
    assert target.inWay == 1
    assert (round(target.x), round(target.y)) == target.finish

    for _ in range(400):
        target.update()
        if target.inWay == 0:
            break
    assert target.inWay == 0
    assert (round(target.x), round(target.y)) == target.moveTo


def test_update_stays_within_its_travel_range():
    target = Target(COLORS, (200, 200), moveTo=(240, 220))
    for _ in range(500):
        target.update()
        assert target.finish[0] - 20 <= target.x <= target.moveTo[0] + 20
        assert target.finish[1] - 20 <= target.y <= target.moveTo[1] + 20


def test_draw_paints_all_colors():
    surface = pygame.Surface(winSize)
    target = Target(COLORS, (400, 300))
    target.draw(surface)
    painted = {surface.get_at((x, y))[:3]
               for x in range(340, 460) for y in range(240, 360)}
    for color in COLORS:
        assert color in painted
