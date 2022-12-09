import pytest
from parse import parse  # type: ignore # pylint: disable=redefined-builtin
from enum import Enum


class Motion_Direction(Enum):
    U = 1
    D = 2
    R = 3
    L = 4


class Motion:
    def __init__(self, direction: str, steps: int) -> None:
        self.direction: Motion_Direction = Motion_Direction[direction]
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


def reduce_distance_froma_tob(a: int, b: int, max_dis: int) -> int:
    if a > b+max_dis:
        return a - 1
    elif a < b-max_dis:
        return a + 1
    else:
        return a


def move_t(h_pos: Coords, t_pos: Coords) -> None:
    if t_pos.x == h_pos.x:
        t_pos.y = reduce_distance_froma_tob(t_pos.y, h_pos.y, 1)
    elif t_pos.y == h_pos.y:
        t_pos.x = reduce_distance_froma_tob(t_pos.x, h_pos.x, 1)
    elif abs(t_pos.x-h_pos.x) == 2 or abs(t_pos.y-h_pos.y) == 2:
        t_pos.x = reduce_distance_froma_tob(t_pos.x, h_pos.x, 0)
        t_pos.y = reduce_distance_froma_tob(t_pos.y, h_pos.y, 0)


def move(motions: list[Motion]) -> list[list[bool]]:
    field: list[list[bool]] = [[False] * 1000 for _ in range(1000)]  # TODO improvement: no fix size
    field[500][500] = True
    h_pos: Coords = Coords(500, 500)
    t_pos: Coords = Coords(500, 500)

    for motion in motions:
        for _ in range(motion.steps):
            # TODO improvement: ensure_field_is_big_enough(motion, field, h_pos, t_pos)
            if motion.direction == Motion_Direction.U:
                h_pos.x -= 1
            elif motion.direction == Motion_Direction.D:
                h_pos.x += 1
            elif motion.direction == Motion_Direction.L:
                h_pos.y -= 1
            elif motion.direction == Motion_Direction.R:
                h_pos.y += 1

            move_t(h_pos, t_pos)
            field[t_pos.x][t_pos.y] = True

    return field


def move_v2(motions: list[Motion]) -> list[list[bool]]:
    field: list[list[bool]] = [[False] * 1000 for _ in range(1000)]  # TODO improvement: no fix size
    field[500][500] = True
    h_pos: Coords = Coords(500, 500)
    t1_pos: Coords = Coords(500, 500)
    t2_pos: Coords = Coords(500, 500)
    t3_pos: Coords = Coords(500, 500)
    t4_pos: Coords = Coords(500, 500)
    t5_pos: Coords = Coords(500, 500)
    t6_pos: Coords = Coords(500, 500)
    t7_pos: Coords = Coords(500, 500)
    t8_pos: Coords = Coords(500, 500)
    t9_pos: Coords = Coords(500, 500)

    for motion in motions:
        for _ in range(motion.steps):
            # TODO improvement: ensure_field_is_big_enough(motion, field, h_pos, t_pos)
            if motion.direction == Motion_Direction.U:
                h_pos.x -= 1
            elif motion.direction == Motion_Direction.D:
                h_pos.x += 1
            elif motion.direction == Motion_Direction.L:
                h_pos.y -= 1
            elif motion.direction == Motion_Direction.R:
                h_pos.y += 1

            move_t(h_pos, t1_pos)
            move_t(t1_pos, t2_pos)
            move_t(t2_pos, t3_pos)
            move_t(t3_pos, t4_pos)
            move_t(t4_pos, t5_pos)
            move_t(t5_pos, t6_pos)
            move_t(t6_pos, t7_pos)
            move_t(t7_pos, t8_pos)
            move_t(t8_pos, t9_pos)
            field[t9_pos.x][t9_pos.y] = True

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
    assert motions[1].direction == Motion_Direction.U
    assert motions[1].steps == 4


def test_day09_simple_count_visited_after_moves(simple_motions: list[str]) -> None:
    motions: list[Motion] = parse_motions(simple_motions)
    last_state: list[list[bool]] = move(motions)
    visited: int = count_visited(last_state)
    assert visited == 13


def test_day09_task1_count_visited_after_moves(all_motions: list[str]) -> None:
    motions: list[Motion] = parse_motions(all_motions)
    last_state: list[list[bool]] = move(motions)
    visited: int = count_visited(last_state)
    assert visited == 6044


def test_day09_task2_count_visited_after_moves(all_motions: list[str]) -> None:
    motions: list[Motion] = parse_motions(all_motions)
    last_state: list[list[bool]] = move_v2(motions)
    visited: int = count_visited(last_state)
    assert visited == 2384
