import pygame

import consts
from consts import suitableSize, winSize


def test_suitableSize_accepts_width_smaller_than_height():
    assert suitableSize("100", "200") == "good"


def test_suitableSize_rejects_width_greater_or_equal_height():
    assert suitableSize("200", "100") == "width should be less than height!"
    assert suitableSize("100", "100") == "width should be less than height!"


def test_suitableSize_rejects_non_numeric_input():
    assert suitableSize("abc", "def") == "You should give integers!"
    assert suitableSize("10a", "20b") == "You should give integers!"


def test_suitableSize_rejects_negative_looking_input():
    assert suitableSize("-30", "20") == "You should give integers!"


def test_winSize_matches_display_surface():
    assert winSize == (consts.dis.get_rect()[2], consts.dis.get_rect()[3])
    assert winSize[0] > 0 and winSize[1] > 0


def test_colors_are_valid_rgb_triples():
    for color in (consts.PINK, consts.BLUE, consts.YELLOW, consts.backColor1,
                  consts.backColor2, consts.mainColor):
        assert len(color) == 3
        assert all(0 <= channel <= 255 for channel in color)


def test_pygame_is_initialised_on_import():
    assert pygame.get_init()
