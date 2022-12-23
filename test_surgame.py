import surgame
from unittest.mock import MagicMock
import pytest


@pytest.fixture()
def patch_surgame(monkeypatch):
    mock = MagicMock()
    mock_window = MagicMock()
    monkeypatch.setattr(surgame, "pygame", mock)
    monkeypatch.setattr(surgame, "wind", mock_window)
    return mock, mock_window


def test_draw_window(patch_surgame):
    mock, mock_window = patch_surgame
    surgame.drawWindow()
    assert mock_window.blit.call_count == 2
    assert mock.display.update.call_count == 1







def test_ghostprinter(patch_surgame):
    mock, mock_window = patch_surgame
    surgame.drawWindow()
    assert mock_window.blit.call_count == 2
    assert mock.display.update.call_count == 1







def test_bulletsprinter(patch_surgame):
    mock, mock_window = patch_surgame
    surgame.drawWindow()
    assert mock_window.blit.call_count == 2
    assert mock.display.update.call_count == 1


