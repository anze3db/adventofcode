# adventofcode

Helper utilities for solving Advent of Code puzzles.

* Project scaffolding with `adventofcode init`
* Benchmark all the days with `adventofcode benchmark`
* No copy-pasting puzzle inputs into files.
* No need to use low-level file APIs to read your inputs.
* Performance reports for example inputs and puzzle inputs.
* Submit the answer immediately when your code returns the result 🏅

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

All the py files look like this:

```python
from adventofcode import AoC


def part1(inp: str):
    return None


def part2(inp: str):
    return None


aoc = AoC(part_1=part1, part_2=part2)
inp = """sample input"""
expected_result = None
aoc.assert_p1(inp, expected_result)
aoc.submit_p1()

expected_result = None
aoc.assert_p2(inp, expected_result)
aoc.submit_p2()
```

You write your solution in part1 and part2 functions.

`aoc.assert_p1(inp, expected_result)` will call your part1 function with inp and assert that the return matches expected_result.

`aoc.submit_p1()` will fetch your puzzle input from the adventofcode.com, cache it locally and call `part1` with your puzzle input. If `part1` returns a value that isn't `None` that value will be submitted as your puzzle answer.


### Set your session cookie

Add the [adventofcode.com](https://adventofcode.com) session cookie value to your `.env` file or to your active session:

```bash
export AOC_SESSION="..."
```

> [!NOTE]
> Setting AOC_SESSION will allow you to get your personal puzzle output (`aoc.get_input()`) and submit your answers with `aoc.submit_p1()` and `aoc.submit_p2()`.

### Benchmarks

You can benchmark your solutions with

```shell
uv run adventofcode benchmark
```

This run each day and parse the timing results from the output. It will print the results in the console and in your README.

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


### Or build your workflow using the AoC class

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
