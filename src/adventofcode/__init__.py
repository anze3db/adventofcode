import datetime
import os
import re
import sys
import time
from collections.abc import Callable
from contextlib import contextmanager
from pathlib import Path
from typing import Any

import percache
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from rich.console import Console

load_dotenv(Path(".env").absolute().as_posix())
cache = percache.Cache(".cache", livesync=True)
console = Console()

AOC_URL = "https://adventofcode.com"


AOC_SESSION = os.getenv("AOC_SESSION")
est = datetime.timezone(datetime.timedelta(hours=-5))
today_est = datetime.datetime.now(tz=est).date()

AOC_YEAR = int(os.getenv("AOC_YEAR", str(today_est.year)))

AOC_NOT_SET_MSG = (
    "Set AOC_SESSION to your `session` cookie on adventofcode.com. You can add it to your .env file or "
    "export it in your shell (export AOC_SESSION='your session cookie')"
)


@contextmanager
def print_perf(typ=""):
    t0 = time.perf_counter()
    yield
    diff = time.perf_counter() - t0
    console.log(f"{diff:.5f}s for {typ}")


class AoC:
    def __init__(
        self,
        part_1: Callable[[str], str | int | None],
        part_2: Callable[[str], str | int | None],
        *,
        day: int | None = None,
        year: int | None = None,
    ):
        if day is None:
            current_filename = Path(sys.argv[0]).stem
            current_filename_numbers = re.sub(r"[^0-9.]", "", current_filename)
            day = int(current_filename_numbers)
        if year is None:
            year = AOC_YEAR

        console.log(f"Solving {day=} {year=}")
        self.day = day
        self.year = year
        self.part_1 = part_1
        self.part_2 = part_2

    def print_p1(self):
        console.log(get_puzzle(self.day, self.year, part=1))

    def print_p2(self):
        console.log(get_puzzle(self.day, self.year, part=2))

    def get_input(self):
        return get_input(year=self.year, day=self.day)

    def assert_p1(self, inp: str, expected: Any):
        res = None
        with print_perf("assert_p1"):
            res = self.part_1(inp)

        assert res is not None, "Result of part_1 should not be None"
        assert res == expected, f"{res} != {expected}"

    def assert_p2(self, inp: str, expected: Any):
        res = None
        with print_perf("assert_p2"):
            res = self.part_2(inp)

        assert res is not None, "Result of part_2 should not be None"
        assert res == expected, f"{res} != {expected}"

    def submit_p1(self, answer: Any | None = None):
        with print_perf("submit_p1"):
            answer = self.part_1(self.get_input())

        submit(year=self.year, day=self.day, level=1, answer=answer)

    def submit_p2(self, answer: Any | None = None):
        with print_perf("submit_p2"):
            answer = self.part_2(self.get_input())

        submit(year=self.year, day=self.day, level=2, answer=answer)


@cache
def get_puzzle(day: int, year: int, part: int) -> str:
    console.log("Fetching puzzle text from server")
    result = requests.get(
        f"{AOC_URL}/{year}/day/{day}",
        cookies={"session": AOC_SESSION} if AOC_SESSION else None,
        timeout=10,
    )
    assert result.status_code == 200, result.text

    soup = BeautifulSoup(result.text, features="html.parser")

    index = part - 1
    if len(soup.body.main.findAll("article")) < index:
        return f"Part {part} Not yet available"

    return soup.body.main.findAll("article")[part - 1].get_text()


@cache
def get_input(year: int, day: int) -> str:
    assert AOC_SESSION, AOC_NOT_SET_MSG
    console.log("Fetching from server")
    result = requests.get(
        f"{AOC_URL}/{year}/day/{day}/input",
        cookies={"session": AOC_SESSION},
        timeout=10,
    )
    assert result.status_code == 200, (f"{AOC_URL}/{year}/day/{day}/input", result.text)

    return result.text


@cache
def submit(year: int, day: int, level: int, answer: Any):
    assert AOC_SESSION, AOC_NOT_SET_MSG
    console.log(f"Posting [bold]{answer}[/bold] for {day=} {level=}")
    if not answer:
        console.log("Skipping submission", answer)
        return
    result = requests.post(
        f"{AOC_URL}/{year}/day/{day}/answer",
        {"level": level, "answer": answer},
        cookies={"session": AOC_SESSION},
        timeout=10,
    )
    assert result.status_code == 200, result.text
    soup = BeautifulSoup(result.text, features="html.parser")
    console.log(soup.body.main.article.get_text())
