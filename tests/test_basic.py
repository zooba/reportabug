import pytest
import sys

from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
import reportabug

del sys.path[0]


def test_collect_from_sys():
    d = reportabug.collect_from_sys()
    assert isinstance(d, dict)
    assert len(d) > 0
