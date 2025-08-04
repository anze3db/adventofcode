def test_version():
    from src.adventofcode.__about__ import __version__  # noqa: PLC0415

    assert __version__
