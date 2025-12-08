# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Calendar Versioning](https://calver.org).

## [25.11]

### Fixed

* Variant column not showing for certain file patterns

## [25.10]

### Added

* When you have alternative solutions only the fastest one is now counted in the totals row and the display in the table was improved:

| Day | Variant | Status | Part 1 Time | Part 2 Time | Total Time |
|----:|:--------|:------:|------------:|------------:|-----------:|
| 01 |  | ✅ | 0.54ms 🟢 | 0.63ms 🟢 | 1.17ms 🟢 |
| 02 |  | ✅ | 0.08ms 🟢 | 0.13ms 🟢 | 0.21ms 🟢 |
| 03 |  | ✅ | 0.38ms 🟢 | 0.98ms 🟢 | 1.36ms 🟢 |
| 04 | numpy | ✅ | 0.80ms 🟢 | 4.48ms 🟢 | 5.28ms 🟢 |
| ~~04~~ |  | ✅ | 5.87ms ⚪ | 14.37ms ⚪ | 20.24ms ⚪ |
| 05 |  | ✅ | 0.28ms 🟢 | 0.09ms 🟢 | 0.37ms 🟢 |
| 06 |  | ✅ | 0.79ms 🟢 | 1.25ms 🟢 | 2.04ms 🟢 |
| 07 |  | ✅ | 1.21ms 🟢 | 1.43ms 🟢 | 2.64ms 🟢 |
| 08 |  | 🕑 | - | - | - |
| 09 |  | 🕑 | - | - | - |
| 10 |  | 🕑 | - | - | - |
| 11 |  | 🕑 | - | - | - |
| 12 |  | 🕑 | - | - | - |
| **Total** | | | 4.08ms 🟢 | 8.99ms 🟢 | 13.07ms 🟢 |

Legend:
 * 🟢 < 100ms
 * 🟡 100ms - 1s
 * 🔴 > 1s
 * ⚪ Not included in total

## Fixed

* Fix benchmark help text (by @baloncek2662)

## [25.9]

### Added

* Ability to benchmark a single file. Thank you @baloncek2662 ❤️

### Fixed

* Crash on Windows. Thank you @tfs-sean-disanti ❤️

## [25.8]

### Added

* Ability to benchmark different solution for one day. Requested by @rodrigogiraoserrao ❤️
* More stable benchmarking (using [Timer.autorange](https://docs.python.org/3/library/timeit.html#timeit.Timer.autorange))

### Fixed

* Improved the README.md template

## [25.7]

### Fixed

* Image issue in README not showing on PyPI

## [25.6]

### Fixed

* Image issue in README

## [25.5]

### Fixed

* Readme improvements

## [25.4]

### Added

* New `uv run adventofcode run` command that removes the need for boilerplate in your solutions.

### Fixed

* Outputs are now cleaner and less verbose.
* Generated templates with `uv run adventofcode init` now include a docstring with instructions on how to run it. All the AoC class boilerplate has been removed.

## [25.3]

### Fixed

* Missing `uv run` commands in README. Thank you @baloncek2662! ❤️

## [25.2]

### Added

* Add `adventofcode benchmark` to the README.

## [25.1]

### Added

 * `adventofcode benchmark` command that generates benchmark results both in the console and in the README. Example README:


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

## [25.0]

### Added

 * Command line tool for scaffolding all the days (`adventofcode init`)
 * Support for Python 3.13 and 3.14

### Removed

 * `part_1_no_splitlines` and `part_2_no_splitlines` parameters. `part_1` and `part_2` now receive a `str` instead of `list[str]`. This was done to simplify the API.
 * Support for Python 3.8 and 3.9

## [23.0b1]

### Added

 * `assert_p1` and `assert_p2` methods to `AoC` class. Used for easily asserting your solutions against sample inputs.
 * `part_1`, `part_2` optional arguments to the `AoC` class. Used to pass in a Callable that will return the correct result for the given input. The callable will be called by `assert_p1`, `assert_p2`, `submit_p1` and `submit_p2` methods.
 * `part_1_no_splitlines` and `part_2_no_splitlines` optional arguments to `AoC` class. Used as an alternative to `part_1` and `part_2` for the rare cases when the input should not be split into lines.


## [2023.0b0] - 2023-12-07

Initial release
