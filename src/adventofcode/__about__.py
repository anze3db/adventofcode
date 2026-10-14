from importlib import metadata as _metadata

try:
    __version__ = _metadata.version("adventofcode")
except _metadata.PackageNotFoundError:  # running from a source tree without install
    __version__ = "0+unknown"
