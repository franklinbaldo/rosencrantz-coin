"""Tests for sampler.py: parse_mine_safe."""

from rosencrantz.sampler import parse_mine_safe


def test_parse_mine():
    assert parse_mine_safe("MINE") is True


def test_parse_safe():
    assert parse_mine_safe("SAFE") is False


def test_parse_lowercase_mine():
    assert parse_mine_safe("mine") is True


def test_parse_lowercase_safe():
    assert parse_mine_safe("safe") is False


def test_parse_with_whitespace():
    assert parse_mine_safe("  MINE  ") is True
    assert parse_mine_safe("  SAFE  ") is False


def test_parse_mine_in_sentence():
    assert parse_mine_safe("It is a MINE") is True


def test_parse_safe_in_sentence():
    assert parse_mine_safe("Cell is SAFE") is False


def test_parse_ambiguous_both():
    assert parse_mine_safe("MINE or SAFE") is None


def test_parse_empty():
    assert parse_mine_safe("") is None


def test_parse_garbage():
    assert parse_mine_safe("hello world") is None
