# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Calendar Versioning](https://calver.org).

## [23.0b1]

### Added

 * `assert_p1` and `assert_p2` methods to `AoC` class, used for easily asserting your solutions against sample inputs.
 * `part_1`, `part_2` are now optional arguments to `AoC` class, so you can use `assert_p1` and `assert_p2` without defining your own functions as well as call `submit_p1` and `submit_p2` without calling `get_input()` manucall.
 * `part_1_no_splitlines` and `part_2_no_splitlines` are now optional arguments to `AoC` class, used inplace of `part_1` and `part_2` when the rare cases where the input should not be split into lines.


## [2023.0b0] - 2023-12-07

Initial release
