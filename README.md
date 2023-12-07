# adventofcode

Helper utilities for solving Advent of Code puzzles

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

Alternatively, you can save your `AOC_SESSION=""` value in a `.env` file.

> [!NOTE]
> Setting AOC_SESSION will allow you to get your personal puzzle output (`aoc.get_input()`) and submit your answers with `aoc.submit_p1()` and `aoc.submit_p2()`.

### Use a template to solve puzzles

I use the following template to start solving puzzles, see my examples in [my repo for 2023](https://github.com/anze3db/adventofcode2023).

```python
from adventofcode import AoC

aoc = AoC()


def part1(inp):
    return None


def part2(inp):
    return None


# Call your function with sample p1 input:
assert part1("""""".splitlines()) == None
# Call your function with the real p1 input and submit the result:
aoc.submit_p1(part1(aoc.get_input()))

# Call your function with sample p1 input:
assert part2("""""".splitlines()) == None
# Call your function with the real p2 input and submit the result:
aoc.submit_p2(part2(aoc.get_input()))
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
