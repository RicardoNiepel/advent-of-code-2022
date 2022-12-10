import pytest


def sum_signal_strengths(instructions_strings: list[str]) -> int:
    register_x: int = 1
    cycle: int = 0
    signal_strength: int = 0
    signal_strength_calc_cycles: list[int] = [20, 60, 100, 140, 180, 220]

    def cycle_increase_and_signal_strength_calc() -> None:
        nonlocal cycle, signal_strength
        cycle += 1
        signal_strength += cycle * register_x if cycle in signal_strength_calc_cycles else 0

    for instruction_str in instructions_strings:
        instruction_str: str = instruction_str.strip()

        cycle_increase_and_signal_strength_calc()
        match (instruction_str[:4]):
            case "addx":
                cycle_increase_and_signal_strength_calc()
                register_x += int(instruction_str[5:])
            case "noop":
                continue
            case unsupported:
                raise Exception("Not supported: " + unsupported)

    return signal_strength


def get_crt_screen(instructions_strings: list[str]) -> str:
    register_x: int = 1
    cycle: int = 0
    crt_screen: str = ""

    def cycle_increase_and_crt_screen_draw() -> None:
        nonlocal cycle, crt_screen
        cycle += 1
        crt_screen += "#" if sprite_and_crtdraw_overlap(register_x, cycle) else "."

    for instruction_str in instructions_strings:
        instruction_str: str = instruction_str.strip()

        cycle_increase_and_crt_screen_draw()
        match (instruction_str[:4]):
            case "addx":
                cycle_increase_and_crt_screen_draw()
                register_x += int(instruction_str[5:])
            case "noop":
                continue
            case unsupported:
                raise Exception("Not supported: " + unsupported)

    for row_end in [40, 81, 122, 163, 204, 245]:
        crt_screen = crt_screen[:row_end] + "\n" + crt_screen[row_end:]

    return crt_screen


def sprite_and_crtdraw_overlap(register_x: int, cycle: int) -> bool:  # type: ignore
    cycle: int = (cycle-1) % 40
    return register_x - 1 <= cycle <= register_x + 1


@pytest.fixture(name="simple_programm")
def simple_programm_fixture() -> list[str]:
    return open('Day 10/input_simple.txt', encoding="utf-8").readlines()


@pytest.fixture(name="complete_programm")
def complete_programm_fixture() -> list[str]:
    return open('Day 10/input.txt', encoding="utf-8").readlines()


def test_simple1_sum_signal_strengths(simple_programm: list[str]) -> None:
    assert sum_signal_strengths(simple_programm) == 13140


def test_task1_sum_signal_strengths(complete_programm: list[str]) -> None:
    assert sum_signal_strengths(complete_programm) == 11960


def test_simple2_get_crt_screen(simple_programm: list[str]) -> None:
    screen: list[str] = get_crt_screen(simple_programm).splitlines()
    print(screen)
    assert screen[0] == "##..##..##..##..##..##..##..##..##..##.."
    assert screen[1] == "###...###...###...###...###...###...###."
    assert screen[2] == "####....####....####....####....####...."
    assert screen[3] == "#####.....#####.....#####.....#####....."
    assert screen[4] == "######......######......######......####"
    assert screen[5] == "#######.......#######.......#######....."


def test_task2_get_crt_screen(complete_programm: list[str]) -> None:
    screen: list[str] = get_crt_screen(complete_programm).splitlines()
    print(screen)
    assert screen[0] == "####...##..##..####.###...##..#....#..#."
    assert screen[1] == "#.......#.#..#.#....#..#.#..#.#....#..#."
    assert screen[2] == "###.....#.#....###..#..#.#....#....####."
    assert screen[3] == "#.......#.#....#....###..#.##.#....#..#."
    assert screen[4] == "#....#..#.#..#.#....#....#..#.#....#..#."
    assert screen[5] == "####..##...##..#....#.....###.####.#..#."
