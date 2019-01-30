import pytest
import sys

from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
import reportabug


def test_collect_from_sys():
    d = reportabug.collect_from_sys()
    assert isinstance(d, dict)
    assert len(d) > 0
    assert isinstance(d["platform"], str)
    assert isinstance(d["prefix"], str)
    assert isinstance(d["executable"], str)


def test_collect_from_platform():
    d = reportabug.collect_from_platform()
    assert isinstance(d["version"], str)
    assert isinstance(d["os"], str)
    assert isinstance(d["architecture"], str)
    assert isinstance(d["machine"], str)


def test_example():
    d = reportabug.collect_from_module("example", "arg value")
    assert d["summary"] == "looks good"
    assert d["arg"] == "arg value"
    assert d["_error_type"] == "NameError"
