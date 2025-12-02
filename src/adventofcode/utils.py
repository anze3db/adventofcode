PART_1_RETURN_STR = "return part1 result"
PART_2_RETURN_STR = "return part2 result"


def format_time(seconds: float) -> str:
    if seconds <= 0.0:
        return "-"
    if seconds < 1:
        return f"{seconds * 1000:.2f}ms"
    return f"{seconds:.2f}s"
