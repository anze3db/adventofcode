# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Calendar Versioning](https://calver.org).

## [23.0b1]

### Added

 * `assert_p1` and `assert_p2` methods to `AoC` class. Used for easily asserting your solutions against sample inputs.
 * `part_1`, `part_2` optional arguments to the `AoC` class. Used to pass in a Callable that will return the correct result for the given input. The callable will be called by `assert_p1`, `assert_p2`, `submit_p1` and `submit_p2` methods.
 * `part_1_no_splitlines` and `part_2_no_splitlines` optional arguments to `AoC` class. Used as an alternative to `part_1` and `part_2` for the rare cases when the input should not be split into lines.


## [2023.0b0] - 2023-12-07

Initial release
