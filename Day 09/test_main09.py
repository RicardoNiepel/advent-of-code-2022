from enum import Enum
import pytest
from parse import parse  # type: ignore # pylint: disable=redefined-builtin


class MotionDirection(Enum):
    U = 1
    D = 2
    R = 3
    L = 4


class Motion:
    def __init__(self, direction: str, steps: int) -> None:
        self.direction: MotionDirection = MotionDirection[direction]
        self.steps: int = steps

    def __repr__(self) -> str:
        return f"{self.direction} {self.steps}"


class Coords:
    def __init__(self, x: int, y: int) -> None:
        self.x: int = x
        self.y: int = y

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"


def parse_motions(motion_strings: list[str]) -> list[Motion]:
    motions: list[Motion] = []

    for motion_str in motion_strings:
        (direction, steps) = parse('{:w} {:d}', motion_str.strip())  # type: ignore
        motions.append(Motion(direction, steps))  # type: ignore

    return motions


def move_head(h_pos: Coords, motion: Motion) -> None:
    if motion.direction == MotionDirection.U:
        h_pos.x -= 1
    elif motion.direction == MotionDirection.D:
        h_pos.x += 1
    elif motion.direction == MotionDirection.L:
        h_pos.y -= 1
    elif motion.direction == MotionDirection.R:
        h_pos.y += 1


def delta_to_single_step(delta: int) -> int:
    if delta < 0:
        return -1
    elif delta > 0:
        return 1
    return 0


def move_tail(h_pos: Coords, t_pos: Coords) -> None:
    delta_x: int = h_pos.x - t_pos.x
    delta_y: int = h_pos.y - t_pos.y

    if abs(delta_x) > 1 or abs(delta_y) > 1:
        t_pos.x += delta_to_single_step(delta_x)
        t_pos.y += delta_to_single_step(delta_y)


def move(motions: list[Motion], count_of_tales: int) -> list[list[bool]]:
    field: list[list[bool]] = [[False] * 1000 for _ in range(1000)]  # TODO improvement: no fix size
    field[500][500] = True
    h_pos: Coords = Coords(500, 500)

    tails: list[Coords] = []
    for _ in range(count_of_tales):
        tails.append(Coords(500, 500))

    for motion in motions:
        for _ in range(motion.steps):
            # TODO improvement: ensure_field_is_big_enough(motion, field, h_pos, t_pos)
            move_head(h_pos, motion)

            last: Coords = h_pos
            for tail in tails:
                move_tail(last, tail)
                last = tail

            field[tails[-1].x][tails[-1].y] = True

    return field


def count_visited(field: list[list[bool]]) -> int:
    visited: int = 0
    for column in field:
        for cell in column:
            visited += cell
    return visited


@pytest.fixture(name="simple_motions")
def simple_motions_fixture() -> list[str]:
    return open('Day 09/input_simple.txt', encoding="utf-8").readlines()


@pytest.fixture(name="all_motions")
def all_motions_fixture() -> list[str]:
    return open('Day 09/input.txt', encoding="utf-8").readlines()


def test_day09_simple_parse(simple_motions: list[str]) -> None:
    motions: list[Motion] = parse_motions(simple_motions)
    assert motions[1].direction == MotionDirection.U
    assert motions[1].steps == 4


def test_day09_simple_count_visited_after_moves(simple_motions: list[str]) -> None:
    motions: list[Motion] = parse_motions(simple_motions)
    last_state: list[list[bool]] = move(motions, 1)
    visited: int = count_visited(last_state)
    assert visited == 13


def test_day09_task1_count_visited_after_moves(all_motions: list[str]) -> None:
    motions: list[Motion] = parse_motions(all_motions)
    last_state: list[list[bool]] = move(motions, 1)
    visited: int = count_visited(last_state)
    assert visited == 6044


def test_day09_task2_count_visited_after_moves(all_motions: list[str]) -> None:
    motions: list[Motion] = parse_motions(all_motions)
    last_state: list[list[bool]] = move(motions, 9)
    visited: int = count_visited(last_state)
    assert visited == 2384
