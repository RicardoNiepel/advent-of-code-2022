import pytest

def priority(char: str) -> int:
    return ord(char)-38 if char.isupper() else ord(char)-96

def dublicated_item(rucksack: str) -> str:
    half = len(rucksack)//2
    comp1 = rucksack[:half]
    comp2 = rucksack[half:]

    for char in comp1:
        if char in comp2:
            return char
    return ""

def dublicated_items_priority(rucksack: str) -> int:
    item = dublicated_item(rucksack)
    return priority(item)

def items_appearing_in_both_priority(rucksacks: list[str]) -> int:
    return sum([dublicated_items_priority(rucksack) for rucksack in rucksacks])

def dublicated_items_priority_three(rucksack1: str, rucksack2: str, rucksack3: str) -> int:
    for char in rucksack1:
        if char in rucksack2 and char in rucksack3:
            return priority(char)
    return 0

def badge_items_priority(rucksacks: list[str]) -> int:
    return sum([dublicated_items_priority_three(rucksacks[x], rucksacks[x+1], rucksacks[x+2]) for x in range(0, len(rucksacks), 3)])


def test_day03_int() -> None:
    assert priority("a") == 1
    assert priority("z") == 26
    assert priority("A") == 27
    assert priority("Z") == 52

@pytest.fixture
def input_simple() -> list[str]:
    return open('Day 03/input_simple.txt').readlines()

@pytest.fixture
def input_long() -> list[str]:
    return open('Day 03/input.txt').readlines()     

def test_day03_simple1(input_simple: list[str]) -> None:
    assert items_appearing_in_both_priority(input_simple) == 157

def test_day03_task1(input_long: list[str]) -> None:
    assert items_appearing_in_both_priority(input_long) == 8298

def test_day03_simple2(input_simple: list[str]) -> None:
    assert badge_items_priority(input_simple) == 70      

def test_day03_task2(input_long: list[str]) -> None:
    assert badge_items_priority(input_long) == 2708      