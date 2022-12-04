import numpy
import pytest

def top3_elves_with_most_calories(calories_list: list[str]) -> list[int]:
    elves: list[int] = [0]

    for calories in calories_list:
        if calories == "\n":
            elves.append(0)
        else:
            elves[len(elves) - 1] += int(calories)

    elves.sort(reverse=True)
    return elves[:3]

def how_much_elf_with_most_calories(calories_list: list[str]) -> int:
    return numpy.max(top3_elves_with_most_calories(calories_list))

def how_much_top3_elves_with_most_calories(calories_list: list[str]) -> int:
    return numpy.sum(top3_elves_with_most_calories(calories_list))

@pytest.fixture
def input_long() -> list[str]:
    return open('Day 01/input.txt').readlines()

def test_simple1() -> None:
    input: list[str] = ["1000", "2000", "3000", "\n", "4000", "\n", "5000", "6000", "\n", "7000", "8000", "9000", "\n", "10000"]
    assert how_much_elf_with_most_calories(input) == 24000

def test_task1(input_long: list[str]) -> None:
    assert how_much_elf_with_most_calories(input_long) == 67633

def test_simple2_list() -> None:
    input: list[str] = ["1000", "2000", "3000", "\n", "4000", "\n", "5000", "6000", "\n", "7000", "8000", "9000", "\n", "10000"]
    assert top3_elves_with_most_calories(input) == [24000, 11000, 10000]

def test_simple2_item() -> None:
    input: list[str] = ["1000", "2000", "3000", "\n", "4000", "\n", "5000", "6000", "\n", "7000", "8000", "9000", "\n", "10000"]
    assert how_much_top3_elves_with_most_calories(input) == 45000

def test_task2(input_long: list[str]) -> None:
    assert how_much_top3_elves_with_most_calories(input_long) == 199628