import argparse
import datetime
from pathlib import Path
from textwrap import dedent

TEMPLATE = '''from adventofcode import AoC


def part1(inp: str) -> str | int | None:
    return None


def part2(inp: str) -> str | int | None:
    return None


aoc = AoC(part_1=part1, part_2=part2)
inp = """sample input"""
expected_result = None
aoc.assert_p1(inp, expected_result)
aoc.submit_p1()

expected_result = None
aoc.assert_p2(inp, expected_result)
aoc.submit_p2()
'''


def generate_templates(year: int, output_dir: Path, num_days: int) -> None:
    """Generate template files for the specified year."""
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Generating templates for Advent of Code {year}")  # noqa: T201

    for day in range(1, num_days + 1):
        filename = f"{day:02d}.py"
        filepath = output_dir / filename

        if filepath.exists():
            print(f"Skipping {filename} (already exists)")  # noqa: T201
            continue

        filepath.write_text(TEMPLATE)
        print(f"Created {filename}")  # noqa: T201

    gitignore_path = output_dir / ".gitignore"
    if gitignore_path.exists():
        gitignore_content = gitignore_path.read_text()
        if ".cache" not in gitignore_content:
            with gitignore_path.open("a") as f:
                if not gitignore_content.endswith("\n"):
                    f.write("\n")
                f.write(".cache\n")
            print("Added .cache to .gitignore")  # noqa: T201
        if ".env" not in gitignore_content:
            with gitignore_path.open("a") as f:
                if not gitignore_content.endswith("\n"):
                    f.write("\n")
                f.write(".env\n")
            print("Added .env to .gitignore")  # noqa: T201

    env_path = output_dir / ".env"
    if not env_path.exists():
        env_path.write_text(
            "# Set your Advent of Code session cookie below\n"
            "# You can find it in your browser's developer tools after logging in to adventofcode.com.  \n"
            "# The name of the cookie is `session`.\n"
            'AOC_SESSION=""\n'
        )
        print("Created .env file (remember to set your AOC_SESSION)")  # noqa: T201


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
        default=datetime.datetime.now(tz=datetime.timezone.utc).year,
        help="Year to generate templates for (default: current year)",
    )

    args = parser.parse_args()

    match args.command:
        case "init":
            generate_templates(args.year, args.directory, 12 if args.year >= 2025 else 25)
        case _:
            parser.print_help()


if __name__ == "__main__":
    main()
