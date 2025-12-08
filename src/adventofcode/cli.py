import argparse
import datetime
import importlib.util
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from textwrap import dedent
from typing import Literal

from dotenv import load_dotenv
from rich.console import Console
from rich.live import Live
from rich.table import Table

from adventofcode import AoC
from adventofcode.utils import PART_1_RETURN_STR, PART_2_RETURN_STR, format_time

load_dotenv(Path(".env").absolute().as_posix())

est = datetime.timezone(datetime.timedelta(hours=-5))
today_est = datetime.datetime.now(tz=est).date()

AOC_YEAR = int(os.getenv("AOC_YEAR", str(today_est.year)))

console = Console(log_path=False)
TEMPLATE = dedent('''\
    """🎄 Solution for Day {day} of Advent of Code {year} 🎄

    Usage:

    uv run adventofcode run {day:02d}.py
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
    ''')


def init_templates(year: int, output_dir: Path, num_days: int) -> None:
    """Generate template files for the specified year."""
    output_dir.mkdir(parents=True, exist_ok=True)

    console.log(f"Generating templates for Advent of Code {year}")

    for day in range(1, num_days + 1):
        filename = f"{day:02d}.py"
        filepath = output_dir / filename

        if filepath.exists():
            console.log(f"Skipping {filename} (already exists)")
            continue

        filepath.write_text(TEMPLATE.format(day=day, year=year), encoding="utf-8")
        console.log(f"Created {filename}")

    gitignore_path = output_dir / ".gitignore"
    if gitignore_path.exists():
        gitignore_content = gitignore_path.read_text()
        if ".cache" not in gitignore_content:
            with gitignore_path.open("a") as f:
                if not gitignore_content.endswith("\n"):
                    f.write("\n")
                f.write(".cache\n")
            console.log("Added .cache to .gitignore")
        if ".env" not in gitignore_content:
            with gitignore_path.open("a") as f:
                if not gitignore_content.endswith("\n"):
                    f.write("\n")
                f.write(".env\n")
            console.log("Added .env to .gitignore")

    env_path = output_dir / ".env"
    if not env_path.exists():
        env_path.write_text(
            "# Set your Advent of Code session cookie below\n"
            "# You can find it in your browser's developer tools after logging in to adventofcode.com.  \n"
            "# The name of the cookie is `session`.\n"
            'AOC_SESSION=""\n'
            f"AOC_YEAR={year}\n",
            encoding="utf-8",
        )
        console.log("Created .env file (remember to set your AOC_SESSION)")


def parse_timing_output(output: str) -> tuple[float, float]:
    """Parse timing information from the AoC class output.

    The AoC class outputs lines like:
    - "0.12ms to return part1 result: "
    - "1.45s to return part2 result: "
    """
    part1_time = part2_time = 0.0

    for line in output.split("\n"):
        match = re.search(r"(\d+\.\d+)m?s to " + PART_1_RETURN_STR, line)
        if match:
            part1_time = float(match.group(1))
            if "ms" in line:
                part1_time /= 1000.0

        match = re.search(r"(\d+\.\d+)m?s to " + PART_2_RETURN_STR, line)
        if match:
            part2_time = float(match.group(1))
            if "ms" in line:
                part2_time /= 1000.0

    return part1_time, part2_time


Color = Literal["green", "yellow", "red", "white"]


@dataclass
class DayResult:
    day: str
    day_num: str = ""
    variant: str = ""
    part1_time: float = 0.0
    part2_time: float = 0.0
    total_time: float = 0.0

    status: str = ""
    error: str | None = None
    in_total: bool = True


def time_to_color(seconds: float) -> Color:
    if seconds <= 0.0:
        return "white"
    elif seconds < 0.1:
        return "green"
    elif seconds < 1:
        return "yellow"
    else:
        return "red"


def split_day_name(day_name: str) -> tuple[str, str]:
    """Split a day name into (day_number, variant).

    Examples:
        '01' -> ('01', '')
        '01-alt' -> ('01', 'alt')
        '03-numpy' -> ('03', 'numpy')
        '03_numpy' -> ('03', 'numpy')
        'numpy03' -> ('03', 'numpy')
        'fast03numpy' -> ('03', 'fast-numpy')
    """
    match = re.search(r"(\d\d)", day_name)
    if match:
        day_num = match.group(1)
        # Extract parts before and after the day number
        before = day_name[: match.start()].rstrip("-_")
        after = day_name[match.end() :].lstrip("-_")
        # Combine before and after parts with a hyphen if both exist
        if before and after:
            variant = f"{before}-{after}"
        else:
            variant = before or after
        return day_num, variant

    return day_name, ""


def run_day(filepath: Path) -> DayResult:
    match = re.match(r"(\d\d)", filepath.stem)
    day_num = int(match.group(1)) if match else 0
    day_num_str, variant = split_day_name(filepath.stem)
    if datetime.date(AOC_YEAR, 12, day_num) > today_est:
        return DayResult(day=filepath.stem, day_num=day_num_str, variant=variant, status="🕑")

    result = DayResult(day=filepath.stem, day_num=day_num_str, variant=variant)

    if "adventofcode run" in filepath.read_text():
        command = ["adventofcode", "run", str(filepath), "--benchmark"]
    else:
        command = [sys.executable, str(filepath)]
    try:
        proc = subprocess.run(  # noqa: S603
            command,
            cwd=filepath.parent,
            capture_output=True,
            text=True,
            timeout=300,  # 300 second timeout
            check=False,
        )
    except subprocess.TimeoutExpired:
        result.error = "Timeout (>5m)"
        result.status = "⏰"
        return result
    except Exception as e:
        result.error = str(e)
        result.status = "❌"
        return result

    output = proc.stdout + proc.stderr

    if proc.returncode != 0:
        result.error = output.strip()[-200:] if output else "Unknown error"
        result.status = "❌"
        return result

    part1_time, part2_time = parse_timing_output(output)
    result.part1_time = part1_time
    result.part2_time = part2_time
    result.total_time = part1_time + part2_time

    if part1_time > 0.0 and part2_time > 0.0:
        result.status = "✅"
    elif part1_time > 0.0 or part2_time > 0.0:
        if AOC_YEAR < 2025 and day_num == 25:
            result.status = "✅"
        elif AOC_YEAR >= 2025 and day_num == 12:
            result.status = "✅"
        else:
            result.status = "⚠️"
    else:
        result.status = "✏️"

    return result


def build_markdown_table(results: list[DayResult], total_time: float, total_part_1: float, total_part_2: float) -> str:
    """Generate a markdown table from benchmark results."""
    # Check if any result has a variant
    has_variants = any(r.variant for r in results)

    if has_variants:
        lines = [
            "| Day | Variant | Status | Part 1 Time | Part 2 Time | Total Time | ",
            "|----:|:--------|:------:|------------:|------------:|-----------:| ",
        ]
    else:
        lines = [
            "| Day | Status | Part 1 Time | Part 2 Time | Total Time | ",
            "|----:|:------:|------------:|------------:|-----------:| ",
        ]

    for r in results:
        if not r.in_total and r.total_time > 0:
            p1_time = f"{format_time(r.part1_time)} ⚪"
            p2_time = f"{format_time(r.part2_time)} ⚪"
            total = f"{format_time(r.total_time)} ⚪"
            day_display = f"~~{r.day_num}~~"
            variant_display = f"~~{r.variant}~~" if r.variant else ""
        else:
            p1_time = markdown_color(format_time(r.part1_time), time_to_color(r.part1_time))
            p2_time = markdown_color(format_time(r.part2_time), time_to_color(r.part2_time))
            total = markdown_color(format_time(r.total_time), time_to_color(r.total_time))
            day_display = r.day_num
            variant_display = r.variant

        if has_variants:
            lines.append(f"| {day_display} | {variant_display} | {r.status} | {p1_time} | {p2_time} | {total} |")
        else:
            lines.append(f"| {day_display} | {r.status} | {p1_time} | {p2_time} | {total} |")

    p1_total = markdown_color(format_time(total_part_1), time_to_color(total_part_1))
    p2_total = markdown_color(format_time(total_part_2), time_to_color(total_part_2))
    total = markdown_color(format_time(total_time), time_to_color(total_time))
    # Add total row
    if has_variants:
        lines.append(f"| **Total** | | | {p1_total} | {p2_total} | {total} |")
    else:
        lines.append(f"| **Total** | | {p1_total} | {p2_total} | {total} |")
    lines.append("")
    lines.append("Legend:")
    lines.append(" * 🟢 < 100ms")
    lines.append(" * 🟡 100ms - 1s")
    lines.append(" * 🔴 > 1s")
    lines.append(" * ⚪ Not included in total")
    return "\n".join(lines)


def get_result_row(table: str, pattern: str) -> str | None:
    table_match = re.search(pattern, table, flags=re.MULTILINE)
    return None if table_match is None else table_match.group(0)


def get_time_diff(old_day_row: str, new_day_row: str) -> list[float]:
    pattern = r"(\d+\.\d+)(ms|s)"

    def parse_time(match: tuple[str, str]) -> float:
        val = float(match[0])
        return val * 1000 if match[1] == "s" else val

    matches_old = re.findall(pattern, old_day_row)
    matches_new = re.findall(pattern, new_day_row)

    if len(matches_old) >= 2 and len(matches_new) >= 2:
        part_1_time_old = parse_time(matches_old[0])
        part_2_time_old = parse_time(matches_old[1])

        part_1_time_new = parse_time(matches_new[0])
        part_2_time_new = parse_time(matches_new[1])
        return [part_1_time_new - part_1_time_old, part_2_time_new - part_2_time_old]
    if len(matches_new) >= 2:
        return [parse_time(matches_new[0]), parse_time(matches_new[1])]
    return [0.0, 0.0]


def update_readme(readme_path: Path, results_table: str, path: Path) -> None:
    """Update the README.md with benchmark results."""
    marker_start = "<!-- BENCHMARK_RESULTS_START -->"
    marker_end = "<!-- BENCHMARK_RESULTS_END -->"
    if not readme_path.exists():
        # Create a new README with results
        content = dedent("""\
            # Advent of Code {AOC_YEAR} 🎄

            ## Solution Benchmarks

            {marker_start}
            {results_table}
            {marker_end}
            """).format(
            AOC_YEAR=AOC_YEAR,
            marker_start=marker_start,
            marker_end=marker_end,
            results_table=results_table,
        )
        readme_path.write_text(content, encoding="utf-8")
        console.log(f"Created {readme_path} with benchmark results")
        return

    content = readme_path.read_text()
    if marker_start in content and marker_end in content:
        if path.is_dir():
            # Replace entire existing results table
            pattern = re.compile(re.escape(marker_start) + r".*?" + re.escape(marker_end), re.DOTALL)
            new_section = f"{marker_start}\n{results_table}\n{marker_end}"
            content = pattern.sub(new_section, content)
        else:
            # strip .py from path
            stem = path.stem

            # substitute the old day row with the new day row
            day_row_pattern = rf"^(\|\s*{stem}\s*\|).*?(\n)"
            old_day_row = get_result_row(content, day_row_pattern)
            if old_day_row is None:
                console.log(f"[red]Could not extract existing row for path {stem} in README[/red]")
                return
            new_day_row = get_result_row(results_table, day_row_pattern)
            if new_day_row is None:
                console.log(f"[red]Could not find new row for path {stem} in results table[/red]")
                return
            content = re.sub(day_row_pattern, new_day_row, content, flags=re.MULTILINE)

            # substitute the total day row with new time
            totals_pattern = r"^(\|\s*\*\*Total\*\*\s*\|).*?(\n)"
            old_totals = re.search(totals_pattern, content, flags=re.MULTILINE)

            time_pattern = r"(\d+\.\d+)(ms|s)"
            matches = re.findall(time_pattern, old_totals.group(0)) if old_totals else []

            if len(matches) < 3:
                console.log("[red]Could not extract existing totals in README[/red]")
                return

            def parse_to_ms(val_str: str, unit_str: str) -> float:
                val = float(val_str)
                return val * 1000 if unit_str == "s" else val

            current_p1_ms = parse_to_ms(matches[0][0], matches[0][1])
            current_p2_ms = parse_to_ms(matches[1][0], matches[1][1])
            current_total_ms = parse_to_ms(matches[2][0], matches[2][1])

            [part_1_diff_ms, part_2_diff_ms] = get_time_diff(old_day_row, new_day_row)

            new_p1_ms = current_p1_ms + part_1_diff_ms
            new_p2_ms = current_p2_ms + part_2_diff_ms
            new_total_ms = current_total_ms + part_1_diff_ms + part_2_diff_ms

            p1_seconds = new_p1_ms / 1000.0
            p2_seconds = new_p2_ms / 1000.0
            total_seconds = new_total_ms / 1000.0

            p1_str = markdown_color(format_time(p1_seconds), time_to_color(p1_seconds))
            p2_str = markdown_color(format_time(p2_seconds), time_to_color(p2_seconds))
            total_str = markdown_color(format_time(total_seconds), time_to_color(total_seconds))

            new_totals = f"| **Total** | | {p1_str} | {p2_str} | {total_str} |\n"
            content = re.sub(totals_pattern, new_totals, content, flags=re.MULTILINE)
    else:
        # Append results section
        content += f"\n## Benchmark Results\n\n{marker_start}\n{results_table}\n{marker_end}\n"

    readme_path.write_text(content, encoding="utf-8")
    console.log(f"Updated {readme_path} with benchmark results")


def console_color(formatted_time: str, color: Color) -> str:
    return f"[{color}]{formatted_time}[/{color}]"


def markdown_color(formatted_time: str, color: Color) -> str:
    if color == "white":
        return formatted_time
    elif color == "green":
        return f"{formatted_time} 🟢"
    elif color == "yellow":
        return f"{formatted_time} 🟡"
    else:
        return f"{formatted_time} 🔴"


def build_console_table(
    results: list[DayResult], current_running: str | None, total_part_1: float, total_part_2: float, total_time: float
) -> Table:
    # Check if any result has a variant
    has_variants = any(r.variant for r in results)
    # Also check if current_running has a variant
    if current_running:
        _, current_variant = split_day_name(current_running)
        if current_variant:
            has_variants = True

    table = Table(title=f"Advent of Code {AOC_YEAR} Benchmark")
    table.add_column("Day", style="cyan", justify="right")
    if has_variants:
        table.add_column("Variant", style="cyan", justify="left")
    table.add_column("Status", justify="center")
    table.add_column("Part 1", justify="right")
    table.add_column("Part 2", justify="right")
    table.add_column("Total", justify="right")

    for r in results:
        p1_time = console_color(format_time(r.part1_time), time_to_color(r.part1_time))
        p2_time = console_color(format_time(r.part2_time), time_to_color(r.part2_time))
        total = console_color(format_time(r.total_time), time_to_color(r.total_time))
        status = r.status
        if not r.in_total and r.total_time > 0:
            if has_variants:
                table.add_row(
                    f"[dim strike]{r.day_num}[/dim strike]",
                    f"[dim strike]{r.variant}[/dim strike]",
                    f"[dim]{status}[/dim]",
                    f"[dim]{format_time(r.part1_time)}[/dim]",
                    f"[dim]{format_time(r.part2_time)}[/dim]",
                    f"[dim]{format_time(r.total_time)}[/dim]",
                )
            else:
                table.add_row(
                    f"[dim strike]{r.day_num}[/dim strike]",
                    f"[dim]{status}[/dim]",
                    f"[dim]{format_time(r.part1_time)}[/dim]",
                    f"[dim]{format_time(r.part2_time)}[/dim]",
                    f"[dim]{format_time(r.total_time)}[/dim]",
                )
        elif has_variants:
            table.add_row(r.day_num, r.variant, status, p1_time, p2_time, total)
        else:
            table.add_row(r.day_num, status, p1_time, p2_time, total)

    if current_running is not None:
        day_num, variant = split_day_name(current_running)
        if has_variants:
            table.add_row(day_num, variant, "⏳", "...", "...", "...")
        else:
            table.add_row(day_num, "⏳", "...", "...", "...")

    if has_variants:
        table.add_row(
            "Total",
            "",
            "",
            console_color(format_time(total_part_1), time_to_color(total_part_1)),
            console_color(format_time(total_part_2), time_to_color(total_part_2)),
            console_color(format_time(total_time), time_to_color(total_time)),
        )
    else:
        table.add_row(
            "Total",
            "",
            console_color(format_time(total_part_1), time_to_color(total_part_1)),
            console_color(format_time(total_part_2), time_to_color(total_part_2)),
            console_color(format_time(total_time), time_to_color(total_time)),
        )
    return table


def get_day_number(day_name: str) -> str:
    """Extract the day number from a filename like '01.py' or '01-alternative.py'."""
    match = re.match(r"(\d\d)", day_name)
    return match.group(1) if match else day_name


def select_best_per_day(results: list[DayResult]) -> tuple[list[DayResult], float, float, float]:
    """Mark the best (fastest) solution for each day as in_total, others as not.

    Returns updated results and the totals based only on best solutions.
    """
    day_groups: dict[str, list[DayResult]] = {}
    for r in results:
        day_num = get_day_number(r.day)
        if day_num not in day_groups:
            day_groups[day_num] = []
        day_groups[day_num].append(r)

    total_time = 0.0
    total_part_1 = 0.0
    total_part_2 = 0.0

    for group in day_groups.values():
        completed = [r for r in group if r.total_time > 0]
        if completed:
            best = min(completed, key=lambda r: r.total_time)
            for r in group:
                r.in_total = r is best
            total_time += best.total_time
            total_part_1 += best.part1_time
            total_part_2 += best.part2_time
        else:
            for r in group:
                r.in_total = False

    return results, total_time, total_part_1, total_part_2


def benchmark(path: Path) -> None:
    console.log("[bold]Running benchmarks for Advent of Code[/bold]\n")
    if path.is_dir():
        day_files = sorted(path.glob("[0-9][0-9]*.py"))
    else:
        day_files = [Path(path)] if path.exists() else []
    if not day_files:
        console.log("[yellow]No day files found[/yellow]")
        return

    results: list[DayResult] = []
    total_time = 0.0
    total_part_1 = 0.0
    total_part_2 = 0.0

    with Live(
        build_console_table(
            results=[],
            current_running=None,
            total_part_1=0.0,
            total_part_2=0.0,
            total_time=0.0,
        ),
        console=console,
        refresh_per_second=4,
    ) as live:
        for filepath in day_files:
            live.update(
                build_console_table(
                    results=results,
                    current_running=filepath.stem,
                    total_part_1=total_part_1,
                    total_part_2=total_part_2,
                    total_time=total_time,
                )
            )
            result = run_day(filepath)
            results.append(result)

            _, total_time, total_part_1, total_part_2 = select_best_per_day(results)

            live.update(
                build_console_table(
                    results=results,
                    current_running=None,
                    total_part_1=total_part_1,
                    total_part_2=total_part_2,
                    total_time=total_time,
                )
            )

    if path.is_dir():
        readme_path = path / "README.md"
    else:
        readme_path = path.parent / "README.md"
    results_table = build_markdown_table(
        results, total_time=total_time, total_part_1=total_part_1, total_part_2=total_part_2
    )
    update_readme(readme_path, results_table, path)


def run(filepath: Path, benchmark: bool = False) -> None:  # noqa: FBT001, FBT002
    # Import the python module on path
    if not filepath.exists():
        console.log(f"[red]File {filepath} does not exist[/red]")
        return

    console.log(f"[bold]Running {filepath}[/bold]\n")
    spec = importlib.util.spec_from_file_location(filepath.stem, filepath)
    if not spec or not spec.loader:
        console.log(f"[red]Could not load module from {filepath}[/red]")
        return
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # Match the first two digits and use them as the day number
    # Assuming the files are named like 01.py, 02-alternative.py, 02-alternative2.py, etc.
    match = re.match(r"(\d\d)", filepath.stem)
    if not match:
        return
    aoc = AoC(
        part_1=module.part1,
        part_2=module.part2,
        day=int(match.group(1)),
        year=AOC_YEAR,
    )
    if hasattr(module, "part1_asserts"):
        for test_input, expected in module.part1_asserts:
            aoc.assert_p1(test_input, expected)
    else:
        console.log("[yellow]No part 1 assertions found[/yellow]\n")

    if benchmark:
        aoc.submit_p1_benchmark()
    else:
        aoc.submit_p1()
    if hasattr(module, "part2_asserts"):
        for test_input, expected in module.part2_asserts:
            aoc.assert_p2(test_input, expected)
    else:
        console.log("[yellow]No part 2 assertions found[/yellow]\n")

    if benchmark:
        aoc.submit_p2_benchmark()
    else:
        aoc.submit_p2()


def main() -> None:
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        prog="adventofcode",
        description="Helper utilities for solving Advent of Code puzzles",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Init command
    init_parser = subparsers.add_parser(
        "init",
        help="Initialize template files for Advent of Code",
        description=(
            "Initialize all template files for a given year. "
            "Creates one Python file per day with boilerplate code for solving puzzles."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=dedent("""\
            Examples:
                adventofcode init                    # Initialize templates for the current year in current directory
                adventofcode init --year 2023        # Initialize templates for 2023 in the current directory
                adventofcode init --year 2024 ./2024 # Initialize templates for 2024 in the ./2024 directory
            """),
    )
    init_parser.add_argument(
        "directory",
        type=Path,
        nargs="?",
        default=Path("."),
        help="Directory for generated files (default: current directory)",
    )
    init_parser.add_argument(
        "-y",
        "--year",
        type=int,
        default=AOC_YEAR,
        help="Year to generate templates for (default: AOC_YEAR env variable or current year)",
    )

    # Benchmark command
    benchmark_parser = subparsers.add_parser(
        "benchmark",
        help="Run all days and generate benchmark results",
        description=("Run all day solutions, measure execution times, and update the README with a benchmark table."),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=dedent("""\
            Examples:
                adventofcode benchmark                  # Run benchmarks in current directory
                adventofcode benchmark ./2024           # Run benchmarks in the ./2024 directory
                adventofcode benchmark 02.py            # Run benchmarks for day 2 only
                adventofcode benchmark ./2024/02.py     # Run benchmarks in the ./2024 directory for day 2 only

            The benchmark will:
            1. Find selected day files (01.py, 02.py, etc.)
            2. Run each day script (python 01.py, etc.)
            3. Parse execution times from the output
            4. Display a live-updating table in the console
            5. Update README.md with a benchmark results table

            Note: Each day script must complete successfully (exit code 0)
            to be marked as passing. The timing is parsed from the AoC
            class output (e.g., "0.00123s for submit_p1").
            """),
    )
    benchmark_parser.add_argument(
        "path",
        type=Path,
        nargs="?",
        default=Path("."),
        help="Path where benchmarked file(s) are located (default: current directory)",
    )

    # Run Command
    run_parser = subparsers.add_parser(
        "run",
        help="Run a specific day's solution",
        description="Run the solution for a specific day and display the output.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=dedent("""\
            Examples:
                adventofcode run 01.py # Run day 1 solution in current directory
            """),
    )
    run_parser.add_argument(
        "-b",
        "--benchmark",
        action="store_true",
        help="Benchmark each part with Time.autorange()",
        default=False,
    )
    run_parser.add_argument(
        "filepath",
        type=Path,
        help="Path to the day file to run (e.g., 01.py)",
    )

    args = parser.parse_args()

    match args.command:
        case "init":
            init_templates(args.year, args.directory, 12 if args.year >= 2025 else 25)
        case "benchmark":
            benchmark(args.path)
        case "run":
            run(args.filepath, benchmark=args.benchmark)
        case _:
            parser.print_help()


if __name__ == "__main__":
    main()
