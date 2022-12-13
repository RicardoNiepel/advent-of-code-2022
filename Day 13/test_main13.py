from functools import cmp_to_key
from typing import Any
import collections.abc
import pytest


def parse(lines: list[str]) -> list[Any]:
    pairs: list[Any] = []
    for pair_idx in range(0, len(lines), 3):
        pairs.append([eval(lines[pair_idx].strip()), eval(lines[pair_idx+1].strip())])

    return pairs


def parse_v2(lines: list[str]) -> list[Any]:
    return [eval(line.strip()) for line in lines if line != "\n"]


def is_right_order(left: Any, right: Any) -> bool | None:
    if not isinstance(left, collections.abc.Sequence) and not isinstance(right, collections.abc.Sequence):
        if left > right:
            return False
        if left < right:
            return True
        return None

    if isinstance(left, collections.abc.Sequence) and isinstance(right, collections.abc.Sequence):
        for index in range(max(len(left), len(right))):
            if index >= len(left):
                return True
            if index >= len(right):
                return False

            result: bool | None = is_right_order(left[index], right[index])
            if result is not None:
                return result
        return None

    if not isinstance(left, collections.abc.Sequence):
        left: list[Any] = [left]
    if not isinstance(right, collections.abc.Sequence):
        right: list[Any] = [right]

    return is_right_order(left, right)


def get_right_order_indices_sum(pairs: list[Any]) -> int:
    sum: int = 0
    for pair_idx, pair in enumerate(pairs):
        if is_right_order(pair[0], pair[1]):
            sum += pair_idx + 1
    return sum


def get_decoder_key(packages: list[Any]) -> int:
    packages.append([[2]])
    packages.append([[6]])

    def compare(item1, item2) -> int:
        if is_right_order(item1, item2):
            return -1
        elif is_right_order(item1, item2) is False:
            return 1
        else:
            return 0
    packages.sort(key=cmp_to_key(compare))

    def find_divider(packages: list[Any], divider_key: int):
        return next(idx + 1 for idx, package in enumerate(packages) if len(package) == 1 and isinstance(
            package[0], collections.abc.Sequence) and len(package[0]) == 1 and package[0][0] == divider_key)
    key1_idx = find_divider(packages, 2)
    key2_idx = find_divider(packages, 6)

    return key1_idx * key2_idx


@ pytest.fixture(name="simple_input")
def simple_input_fixture() -> list[str]:
    return open('Day 13/input_simple.txt', encoding="utf-8").readlines()


@ pytest.fixture(name="complete_input")
def complete_input_fixture() -> list[str]:
    return open('Day 13/input.txt', encoding="utf-8").readlines()


def test_parse(simple_input: list[str]) -> None:
    parsed: list[Any] = parse(simple_input)
    assert len(parsed) == 8


def test_simple1_right_order_indices(simple_input: list[str]) -> None:
    parsed: list[Any] = parse(simple_input)
    assert get_right_order_indices_sum(parsed) == 13


def test_task1_right_order_indices(complete_input: list[str]) -> None:
    parsed: list[Any] = parse(complete_input)
    assert get_right_order_indices_sum(parsed) == 5208


def test_simple2_order(simple_input: list[str]) -> None:
    parsed: list[Any] = parse_v2(simple_input)
    assert get_decoder_key(parsed) == 140


def test_task2_order(complete_input: list[str]) -> None:
    parsed: list[Any] = parse_v2(complete_input)
    assert get_decoder_key(parsed) == 25792
