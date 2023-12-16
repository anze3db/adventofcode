# adventofcode

Helper utilities for solving Advent of Code puzzles.

* No copy-pasting puzzle inputs into files.
* No need to use low-level file APIs to read your inputs.
* Performance reports for example inputs and puzzle inputs.
* Submit the answer immediately when your code returns the result 🏎️

## Usage

### Install the package

Install the package with pip:
```bash
pip install adventofcode
```

### Set your session cookie

Add the [adventofcode.com](https://adventofcode.com) session cookie value to your env:

```bash
export AOC_SESSION="..."
```

Alternatively, you can save your `AOC_SESSION="******"` value in a `.env` file.

> [!NOTE]
> Setting AOC_SESSION will allow you to get your personal puzzle output (`aoc.get_input()`) and submit your answers with `aoc.submit_p1()` and `aoc.submit_p2()`.

### Use a template to solve puzzles

I use the following template to start solving puzzles, see my examples in [my repo for 2023](https://github.com/anze3db/adventofcode2023).

```python
from adventofcode import AoC


def part1(inp):
    return None


def part2(inp):
    return None


aoc = AoC(part_1=part1, part_2=part2)
inp = """sample input"""
# Run your part1 function with sample input and assert the expected result:
aoc.assert_p1(inp, 42)
# Run your part1 function on puzzle input and submit the answer returned:
aoc.submit_p1()

# Run your part2 function with sample input and assert the expected result:
aoc.assert_p2(inp, 6*7)
# Run your part2 function on puzzle input and submit the answer returned:
aoc.submit_p2()
```

> [!NOTE]
> All submissions and fetched results are cached locally in the `.cache.db` file so that we don't spam the AoC servers or resubmit the same answer multiple times.

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
