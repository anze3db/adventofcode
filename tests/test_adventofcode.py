import pytest

from src.adventofcode.cli import split_day_name


def test_version():
    from src.adventofcode.__about__ import __version__  # noqa: PLC0415

    assert __version__


@pytest.mark.parametrize(
    ("day_name", "expected"),
    [
        ("01", ("01", "")),
        ("01-alt", ("01", "alt")),
        ("03-numpy", ("03", "numpy")),
        ("03_numpy", ("03", "numpy")),
        ("fast-03", ("03", "fast")),
        ("maybe-03-fast", ("03", "maybe-fast")),
        ("fast03", ("03", "fast")),
        ("maybe03fast", ("03", "maybe-fast")),
        ("maybe_03_fast", ("03", "maybe-fast")),
        ("numpy03", ("03", "numpy")),
    ],
)
def test_split_day_name(day_name: str, expected: tuple[str, str]):
    assert split_day_name(day_name) == expected
