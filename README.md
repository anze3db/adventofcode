# adventofcode - a framework for solving Advent of Code puzzles 🎄

* Project scaffolding with `uv run adventofcode init`.
* Assert and submit your solutions with `uv run adventofcode run`.
* Benchmark all your solutions with `uv run adventofcode benchmark`.
* No copy-pasting puzzle inputs or loading inputs from files.
* Submit the answer immediately when your code returns the result. 🏅

## Usage

### Setup

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

Implement your solution in `part1` and `part2` functions and run

```bash
uv run adventofcode run 01.py
```

This will:

* Run your day 1, `part1` function with the inputs provided in the `part1_asserts` iterable and compare them with the expected values. If the function's return value doesn't match the expected answer, the command will stop. *Hint*: Each puzzle usually contains example input and an expected answer—these make for great asserts!
* If all the `part1_asserts` pass, `part1` will be called with your puzzle input fetched from adventofcode.com using your session cookie.
* If `part1` returns a non-None value for your puzzle input, that value will be submitted to adventofcode.com as your part 1 answer using your session cookie. All answer submissions are cached, so each unique answer will only be submitted once.
* If your answer was correct the same process repeats for `part2`.

### Set your session cookie

Add the [adventofcode.com](https://adventofcode.com) session cookie value to your `.env` file:

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

> [!NOTE]
> You can find the session cookie by going to adventofcode.com in your browser. Make sure you are logged in, then open your browser's developer tools and navigate to Application → Storage → Cookies. Look for the cookie named `session` and copy its value.

### Benchmarks

You can benchmark your solutions with

```shell
uv run adventofcode benchmark
```

This will run each day's solution and parse the timing results from the output. The results will be printed to the console as well as added to your README.md.

Example README:

| Day | Status | Part 1 Time | Part 2 Time | Total Time |
|:---:|:------:|------------:|------------:|-----------:|
| 01 | ✅ | 2.1ms 🟢 | 0.6ms 🟢 | 2.6ms 🟢 |
| 02 | ✅ | 1.9ms 🟢 | 1.2ms 🟢 | 3.1ms 🟢 |
| 03 | ✅ | 1.5ms 🟢 | 0.5ms 🟢 | 2.0ms 🟢 |
| 04 | ✅ | 22.5ms 🟢 | 5.2ms 🟢 | 27.8ms 🟢 |
| 05 | ✅ | 3.6ms 🟢 | 4.1ms 🟢 | 7.7ms 🟢 |
| 06 | ✅ | 3.6ms 🟢 | 4.14s 🔴 | 4.14s 🔴 |
| 07 | ✅ | 33.8ms 🟢 | 1.07s 🔴 | 1.11s 🔴 |
| 08 | ✅ | 1.0ms 🟢 | 0.7ms 🟢 | 1.7ms 🟢 |
| 09 | ✅ | 6.3ms 🟢 | 1.08s 🔴 | 1.09s 🔴 |
| 10 | ✅ | 3.2ms 🟢 | 3.2ms 🟢 | 6.4ms 🟢 |
| 11 | ✅ | 1.7ms 🟢 | 45.0ms 🟢 | 46.7ms 🟢 |
| 12 | ✅ | 33.3ms 🟢 | 31.0ms 🟢 | 64.4ms 🟢 |
| 13 | ✅ | 118.1ms 🟡 | 360.8ms 🟡 | 478.9ms 🟡 |
| 14 | ✅ | 3.7ms 🟢 | 411.4ms 🟡 | 415.1ms 🟡 |
| 15 | ✅ | 3.5ms 🟢 | 5.0ms 🟢 | 8.4ms 🟢 |
| 16 | ✅ | 87.1ms 🟢 | 133.9ms 🟡 | 221.1ms 🟡 |
| 17 | ✅ | 0.7ms 🟢 | 21.0ms 🟢 | 21.7ms 🟢 |
| 18 | ✅ | 7.2ms 🟢 | 7.49s 🔴 | 7.50s 🔴 |
| 19 | ✅ | 9.7ms 🟢 | 111.7ms 🟡 | 121.4ms 🟡 |
| 20 | ✅ | 50.54s 🔴 | 4.46s 🔴 | 54.99s 🔴 |
| 21 | ✅ | 0.4ms 🟢 | 0.3ms 🟢 | 0.8ms 🟢 |
| 22 | ✅ | 603.7ms 🟡 | 1.90s 🔴 | 2.50s 🔴 |
| 23 | ✅ | 255.0ms 🟡 | 263.4ms 🟡 | 518.4ms 🟡 |
| 24 | ⚠️ | 1.4ms 🟢 | - | 1.4ms 🟢 |
| 25 | ✅ | 7.2ms 🟢 | - | 7.2ms 🟢 |
| **Total** | | 51.75s 🔴 | 21.53s 🔴 | 73.28s 🔴 |

Legend:
 * 🟢 < 100ms
 * 🟡 100ms - 1s
 * 🔴 > 1s

### Alternatively, you can build your own workflow using the lower level AoC class

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
