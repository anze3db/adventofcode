# 🎄 adventofcode [![PyPI - Version](https://img.shields.io/pypi/v/adventofcode.svg)](https://pypi.org/project/adventofcode)  [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/adventofcode.svg)](https://pypi.org/project/adventofcode)

<p align="center">
  <img width="742" height="613" alt="Screenshot 2025-12-02 at 10 04 42" src="https://github.com/anze3db/adventofcode/blob/main/screenshot.png?raw=true" />
</p>


### Your framework for solving [Advent Of Code](https://adventofcode.com) puzzles 🧩 and benchmarking solutions 🚀

* Project scaffolding with `uv run adventofcode init`.
* Assert and submit your solutions with `uv run adventofcode run`.
* Benchmark all your solutions with `uv run adventofcode benchmark`.
* No copy-pasting puzzle inputs or loading inputs from files.
* Submit the answer immediately when your code returns the result. 🏅

------

**Table of Contents**

- [Setup](#setup)
- [Session cookie](#session-cookie)
- [Run and submit your solution](#run-and-submit-your-solution)
- [Benchmark all your solutions](#benchmark-all-your-solutions)
- [Using AoC class](#using-aoc-class)
- [Happy solving 🎄](#happy-solving-)
- [Similar projects](#similar-projects)




## Setup

```bash
uv init
uv add adventofcode
uv run adventofcode init
```

This will generate the scripts for each day:

```bash
.
├── 01.py
├── 02.py
├── 03.py
├── 04.py
├── 05.py
├── 06.py
├── 07.py
├── 08.py
├── 09.py
├── 10.py
├── 11.py
├── 12.py
├── main.py
├── pyproject.toml
├── README.md
└── uv.lock

1 directory, 16 files
```

All the generated Python files look like this:

```python
"""🎄 Solution for Day 1 of Advent of Code 2025 🎄

Usage:

uv run adventofcode run 01.py
"""

inp = """your input"""
part1_asserts = [
    (inp, None),
]
part2_asserts = [
    (inp, None),
]


def part1(inp: str) -> str | int | None:
    return None


def part2(inp: str) -> str | int | None:
    return None

```
## Session cookie

Before we can run these files we need to set up your session cookie. You can find the session cookie by going to [adventofcode.com] in your browser. Make sure you are logged in, then open your browser's developer tools and navigate to Application → Storage → Cookies. Look for the cookie named `session` and copy its value.


Then  add the [adventofcode.com](https://adventofcode.com) session cookie value to your `.env` file:

```
# Set your Advent of Code session cookie below
# You can find it in your browser's developer tools after logging in to adventofcode.com.
# The name of the cookie is `session`.
AOC_SESSION="YOUR_SESSION_COOKIE_HERE"
AOC_YEAR=2025

```

or to your environment variables:

```bash
export AOC_SESSION="..."
```

## Run and submit your solution

Implement your solution in `part1` and `part2` functions and run

```bash
uv run adventofcode run 01.py
```

This will:

* Run your day 1, `part1` function with the inputs provided in the `part1_asserts` iterable and compare them with the expected values. If the function's return value doesn't match the expected answer, the command will stop. *Hint*: Each puzzle usually contains example input and an expected answer—these make for great asserts!
* If all the `part1_asserts` pass, `part1` will be called with your puzzle input fetched from adventofcode.com using your session cookie.
* If `part1` returns a non-None value for your puzzle input, that value will be submitted to adventofcode.com as your part 1 answer using your session cookie. All answer submissions are cached, so each unique answer will only be submitted once.
* If your answer was correct the same process repeats for `part2`.

## Benchmark all your solutions

You can benchmark your solutions with

```shell
uv run adventofcode benchmark
```

This will run each day's solution and parse the timing results from the output. The results will be printed to the console as well as added to your README.md.

If you are in a hurry you can also benchmark a single day's solution with

```shell
uv run adventofcode benchmark 05.py
```

Example console output:

Example README:

<!-- BENCHMARK_RESULTS_START -->
| Day | Status | Part 1 Time | Part 2 Time | Total Time |
|:---:|:------:|------------:|------------:|-----------:|
| 01 | ✅ | 0.28ms 🟢 | 0.41ms 🟢 | 0.69ms 🟢 |
| 02 | ✅ | 0.76ms 🟢 | 1.13ms 🟢 | 1.89ms 🟢 |
| 03 | ✅ | 0.15ms 🟢 | 0.33ms 🟢 | 0.48ms 🟢 |
| 04 | ✅ | 21.43ms 🟢 | 4.79ms 🟢 | 26.22ms 🟢 |
| 05 | ✅ | 1.95ms 🟢 | 3.51ms 🟢 | 5.46ms 🟢 |
| 06 | ✅ | 3.04ms 🟢 | 3.91s 🔴 | 3.91s 🔴 |
| 07 | ✅ | 30.58ms 🟢 | 1.01s 🔴 | 1.04s 🔴 |
| 08 | ✅ | 0.42ms 🟢 | 0.60ms 🟢 | 1.02ms 🟢 |
| 09 | ✅ | 5.75ms 🟢 | 1.01s 🔴 | 1.02s 🔴 |
| 10 | ✅ | 2.85ms 🟢 | 3.05ms 🟢 | 5.90ms 🟢 |
| 11 | ✅ | 0.97ms 🟢 | 37.60ms 🟢 | 38.57ms 🟢 |
| 12 | ✅ | 30.75ms 🟢 | 31.96ms 🟢 | 62.71ms 🟢 |
| 13 | ✅ | 108.79ms 🟡 | 342.44ms 🟡 | 451.23ms 🟡 |
| 14 | ✅ | 3.03ms 🟢 | 380.22ms 🟡 | 383.25ms 🟡 |
| 15 | ✅ | 2.28ms 🟢 | 4.71ms 🟢 | 6.99ms 🟢 |
| 16 | ✅ | 80.55ms 🟢 | 124.54ms 🟡 | 205.09ms 🟡 |
| 17 | ✅ | 0.02ms 🟢 | 19.99ms 🟢 | 20.01ms 🟢 |
| 18 | ✅ | 5.66ms 🟢 | 6.98s 🔴 | 6.99s 🔴 |
| 19 | ✅ | 9.05ms 🟢 | 99.83ms 🟢 | 108.88ms 🟡 |
| 20 | ✅ | 47.46s 🔴 | 4.28s 🔴 | 51.74s 🔴 |
| 21 | ✅ | 0.22ms 🟢 | 0.25ms 🟢 | 0.47ms 🟢 |
| 22 | ✅ | 603.65ms 🟡 | 1.87s 🔴 | 2.47s 🔴 |
| 23 | ✅ | 223.80ms 🟡 | 222.87ms 🟡 | 446.67ms 🟡 |
| 24 | ⚠️ | 0.94ms 🟢 | - | 0.94ms 🟢 |
| 25 | ✅ | 6.02ms 🟢 | - | 6.02ms 🟢 |
| **Total** | | 48.60s 🔴 | 20.34s 🔴 | 68.94s 🔴 |

Legend:
 * 🟢 < 100ms
 * 🟡 100ms - 1s
 * 🔴 > 1s
<!-- BENCHMARK_RESULTS_END -->

## Using AoC class

Alternatively, you can build your own workflow using the lower level AoC class

```python
from adventofcode import AoC

aoc = AoC() # defaults to current year and parses the day from the filename (e.g. 01.py will be day 1)

aoc.print_p1() # prints the first part of the puzzle
inp = aoc.get_input() # returns the input as a string
# solve the puzzle here
...
aoc.submit_p1('part 1 answer') # submits the answer to the first part of the puzzle
aoc.print_p2() # prints the second part of the puzzle
# solve the puzzle here
...
aoc.submit_p2('part 2 answer') # submits the answer to the second part of the puzzle
```

### Happy solving 🎄

Enjoy and have fun!

### Similar projects

* [elf](https://pypi.org/project/elf/)
