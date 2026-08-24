import os
import re

os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

import pygame
import pytest

from ball import Ball
from consts import suitableSize
from target import Target
from utils import ASSET_DIR, asset_path, getV, load_sound


def test_get_v_returns_zero_for_coincident_points():
    assert getV(0, 5, [10, 10], [20, 20], 1) == (0.0, 0.0)


def test_get_v_rejects_zero_mass():
    with pytest.raises(ValueError, match="Mass must not be zero"):
        getV(0, 5, [10, 20], [20, 30], 0)


def test_asset_path_is_absolute_and_missing_sound_names_path(monkeypatch):
    path = asset_path("missing.mp3")
    assert path == os.path.join(ASSET_DIR, "missing.mp3")
    assert os.path.isabs(path)

    pygame.mixer.init()
    with pytest.raises(RuntimeError, match=re.escape(path)):
        load_sound("missing.mp3")


def test_sound_load_is_independent_of_cwd(monkeypatch, tmp_path):
    pygame.mixer.init()
    monkeypatch.chdir(tmp_path)
    sound = load_sound("bounce.mp3")
    assert sound.get_length() > 0


def test_suitable_size_validates_and_compares_integer_values():
    with pytest.raises(ValueError, match="You should give integers!"):
        suitableSize("wide", "600")
    with pytest.raises(ValueError, match="width should be less than height!"):
        suitableSize("800", "600")
    assert suitableSize("600", "800") == "good"


def test_set_pos_keeps_back_buffers_in_sync():
    ball = Ball((100, 500), (255, 0, 0), 0, 0)
    target = Target([(255, 0, 0)], (100, 100), (120, 110))

    ball.setPos((100, 500), target, (0, 0), [])
    first_size = ball.backSize[0]
    ball.setPos((100, 500), target, (0, 0), [])

    assert len(ball.backPos) == len(ball.backSize)
    assert ball.backSize[0] < first_size
