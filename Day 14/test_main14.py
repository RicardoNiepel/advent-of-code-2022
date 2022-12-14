import pytest


def parse_cave(cave_lines: list[str]) -> dict[int, dict[int, str]]:
    cave: dict[int, dict[int, str]] = {}

    for line in cave_lines:
        paths: list[str] = line.split(" -> ")
        for path_idx in range(len(paths) - 1):
            start: tuple[int, int] = parse_line(paths[path_idx])
            end: tuple[int, int] = parse_line(paths[path_idx + 1])
            put_rocks(cave, start, end)

    return cave


def parse_line(path: str) -> tuple[int, int]:
    parsed: list[str] = path.strip().split(",")
    return (int(parsed[0]), int(parsed[1]))


def put_rocks(cave: dict[int, dict[int, str]], start: tuple[int, int], end: tuple[int, int]) -> None:
    x_range: range = range(start[0], end[0] + 1) if start[0] <= end[0] else range(end[0], start[0] + 1)
    for x in x_range:
        y_range: range = range(start[1], end[1] + 1) if start[1] <= end[1] else range(end[1], start[1] + 1)
        for y in y_range:
            if x not in cave:
                cave[x] = {}
            cave[x][y] = "#"


def is_free(parsed_cave: dict[int, dict[int, str]], pos_x: int, pos_y: int) -> bool:
    return (pos_x not in parsed_cave) or (pos_y not in parsed_cave[pos_x])


def fall_one_unit_sand(parsed_cave: dict[int, dict[int, str]], sand_pouring: tuple[int, int]) -> bool:
    max_y: int = max(y for x in parsed_cave for y in parsed_cave[x])
    sand_pos_x: int = sand_pouring[0]
    sand_pos_y: int = sand_pouring[1]

    fall_possible: bool = False

    while sand_pos_y < max_y:
        if is_free(parsed_cave, sand_pos_x, sand_pos_y + 1):
            sand_pos_y += 1
            fall_possible = True
        elif is_free(parsed_cave, sand_pos_x - 1, sand_pos_y + 1):
            sand_pos_x -= 1
            sand_pos_y += 1
            fall_possible = True
        elif is_free(parsed_cave, sand_pos_x + 1, sand_pos_y + 1):
            sand_pos_x += 1
            sand_pos_y += 1
            fall_possible = True
        else:
            parsed_cave[sand_pos_x][sand_pos_y] = "o"
            return fall_possible  # blocked by rocks

    return False


def add_floor(cave: dict[int, dict[int, str]]) -> None:
    min_x: int = min(x for x in cave)
    max_x: int = max(x for x in cave)
    max_y: int = max(y for x in cave for y in cave[x])

    for x in range(min_x - max_y, max_x + max_y):
        if x not in cave:
            cave[x] = {}
        cave[x][max_y + 2] = "#"


def print_cave(cave: dict[int, dict[int, str]]) -> str:
    min_x: int = min(x for x in cave)
    max_x: int = max(x for x in cave)
    max_y: int = max(y for x in cave for y in cave[x])

    output: str = ""
    for y in range(0, max_y+1):
        for x in range(min_x, max_x+1):
            if is_free(cave, x, y):
                output += "."
            else:
                output += cave[x][y]
        output += "\n"
    return output


@ pytest.fixture(name="simple_input")
def simple_input_fixture() -> list[str]:
    return open('Day 14/input_simple.txt', encoding="utf-8").readlines()


@ pytest.fixture(name="complete_input")
def complete_input_fixture() -> list[str]:
    return open('Day 14/input.txt', encoding="utf-8").readlines()


def test_parse_cave(simple_input: list[str]) -> None:
    parsed_cave: dict[int, dict[int, str]] = parse_cave(simple_input)
    assert parsed_cave[498][4] == "#"
    assert parsed_cave[494][9] == "#"


def test_fall_sand_after_one_unit(simple_input: list[str]) -> None:
    parsed_cave: dict[int, dict[int, str]] = parse_cave(simple_input)
    fall_one_unit_sand(parsed_cave, (500, 0))
    assert parsed_cave[498][4] == "#"
    assert parsed_cave[494][9] == "#"
    assert parsed_cave[500][8] == "o"


def test_simple1_fall_until_not_possible(simple_input: list[str]) -> None:
    parsed_cave: dict[int, dict[int, str]] = parse_cave(simple_input)
    units: int = 0
    while fall_one_unit_sand(parsed_cave, (500, 0)):
        units += 1

    assert units == 24


def test_task1_fall_until_not_possible(complete_input: list[str]) -> None:
    parsed_cave: dict[int, dict[int, str]] = parse_cave(complete_input)
    units: int = 0
    while fall_one_unit_sand(parsed_cave, (500, 0)):
        units += 1

    assert units == 757


def test_simple2_fall_until_floor(simple_input: list[str]) -> None:
    parsed_cave: dict[int, dict[int, str]] = parse_cave(simple_input)
    open('Day 14/output_0_1.txt', 'w+', encoding="utf-8").write(print_cave(parsed_cave))

    add_floor(parsed_cave)

    units: int = 1
    while fall_one_unit_sand(parsed_cave, (500, 0)):
        units += 1
    parsed_cave[500][0] = "X"

    open('Day 14/output_0_2.txt', 'w+', encoding="utf-8").write(print_cave(parsed_cave))
    assert units == 93


def test_task2_fall_until_floor(complete_input: list[str]) -> None:
    parsed_cave: dict[int, dict[int, str]] = parse_cave(complete_input)
    open('Day 14/output_1_1.txt', 'w+', encoding="utf-8").write(print_cave(parsed_cave))

    add_floor(parsed_cave)

    units: int = 1
    while fall_one_unit_sand(parsed_cave, (500, 0)):
        units += 1
        parsed_cave[500][0] = "X"

    open('Day 14/output_1_2.txt', 'w+', encoding="utf-8").write(print_cave(parsed_cave))
    assert units == 24943
