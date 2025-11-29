# adventofcode

Helper utilities for solving Advent of Code puzzles.

* No copy-pasting puzzle inputs into files.
* No need to use low-level file APIs to read your inputs.
* Performance reports for example inputs and puzzle inputs.
* Submit the answer immediately when your code returns the result 🏎️

## Usage

### Setup 

```bash
uv init
uv add adventofcode
adventofcode init
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

All the xx.py files look like this:

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
