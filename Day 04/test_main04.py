from collections.abc import Callable
import pytest

def range_contains(r1: range, r2: range) -> bool:
    return (r1[0] in r2 and r1[-1] in r2) or (r2[0] in r1 and r2[-1] in r1)

def range_overlaps(r1: range, r2: range) -> bool:
    return max(r1.start, r2.start) < min(r1.stop, r2.stop)

def create_range(elf_string: str) -> range:
    (start, end) = [int(x) for x in elf_string.split("-")]
    return range(start, end+1) # +1 because we need inclusive ranges

def check_assignment(assignment: str, range_check_func: Callable[[range, range], bool]) -> bool:
    (elf1, elf2) = assignment.split(",")
    return range_check_func(create_range(elf1), create_range(elf2))

def count_of_assignments(assignments: list[str], filter_func: Callable[[range, range], bool]) -> int:
    return sum([check_assignment(assignment, filter_func) for assignment in assignments])


@pytest.fixture
def input_simple() -> list[str]:
    return open('Day 04/input_simple.txt').readlines()

@pytest.fixture
def input_long() -> list[str]:
    return open('Day 04/input.txt').readlines()    

def test_day04_simple1(input_simple: list[str]) -> None:
    assert count_of_assignments(input_simple, range_contains) == 2

def test_day04_task1(input_long: list[str]) -> None:
    assert count_of_assignments(input_long, range_contains) == 582

def test_day04_simple2(input_simple: list[str]) -> None:
    assert count_of_assignments(input_simple, range_overlaps) == 4

def test_day04_task2(input_long: list[str]) -> None:
    assert count_of_assignments(input_long, range_overlaps) == 893