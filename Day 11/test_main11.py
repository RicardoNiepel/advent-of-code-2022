from typing import Callable
import functools
import pytest


def get_numbers(string: str) -> list[int]:
    return [int(number) for number in string.split(", ")]


class Monkey:
    def __init__(self, monkey_str: list[str]) -> None:
        (items, operation_func, test_divisor, if_test_true_monkey, if_test_false_monkey) = self.parse(monkey_str)
        self.items: list[int] = items
        self.operation_func: Callable[[int], int] = operation_func
        self.test_divisor: int = test_divisor
        self.if_test_true_monkey: int = if_test_true_monkey
        self.if_test_false_monkey: int = if_test_false_monkey

    def parse(self, monkey_str: list[str]) -> tuple[list[int], Callable[[int], int], int, int, int]:
        items: list[int] = get_numbers(monkey_str[1][18:])

        expression: str = monkey_str[2][18:]
        operation_func: Callable[[int], int] = eval('lambda old:' + expression)

        test_divisor: int = int(monkey_str[3][21:])  # Callable[[int], bool] = lambda to_test:
        if_test_true_monkey: int = int(monkey_str[4][29:])
        if_test_false_monkey: int = int(monkey_str[5][30:])

        return (items, operation_func, test_divisor, if_test_true_monkey, if_test_false_monkey)


def parse_input(input_lines: list[str]) -> list[Monkey]:
    return [Monkey(input_lines[monkey_start_index:monkey_start_index+7]) for monkey_start_index in range(0, len(input_lines), 7)]


def level_of_monkey_business(monkeys: list[Monkey], rounds_count: int, very_worried: bool) -> int:
    inspections: list[int] = [0] * len(monkeys)

    all_test_divisors: list[int] = [monkey.test_divisor for monkey in monkeys]
    common_divisor: int = functools.reduce(lambda value, element: value * element, all_test_divisors)

    for _ in range(rounds_count):
        for monkey_idx, monkey in enumerate(monkeys):
            # for _ in range(len(monkey.items)):
            while monkey.items:
                item: int = monkey.items.pop(0)
                inspections[monkey_idx] += 1
                worry_level: int = monkey.operation_func(item)
                if not very_worried:
                    worry_level = int(worry_level / 3)
                else:  # needed to look at someoneelse
                    worry_level = worry_level % common_divisor

                if worry_level % monkey.test_divisor == 0:  # monkey.test_func(worry_level):
                    monkeys[monkey.if_test_true_monkey].items.append(worry_level)
                else:
                    monkeys[monkey.if_test_false_monkey].items.append(worry_level)

    inspections.sort()
    return inspections[-1] * inspections[-2]


@ pytest.fixture(name="simple_input")
def simple_input_fixture() -> list[str]:
    return open('Day 11/input_simple.txt', encoding="utf-8").readlines()


@ pytest.fixture(name="complete_input")
def complete_input_fixture() -> list[str]:
    return open('Day 11/input.txt', encoding="utf-8").readlines()


def test_simple1_parse_input(simple_input: list[str]) -> None:
    parsed: list[Monkey] = parse_input(simple_input)
    assert len(parsed[0].items) == 2
    assert parsed[0].operation_func(10) == 190


def test_simple1_execute_rounds(simple_input: list[str]) -> None:
    parsed: list[Monkey] = parse_input(simple_input)
    assert level_of_monkey_business(parsed, 20, False) == 10605


def test_task1_execute_rounds(complete_input: list[str]) -> None:
    parsed: list[Monkey] = parse_input(complete_input)
    assert level_of_monkey_business(parsed, 20, False) == 57348


def test_simple2_execute_1_rounds(simple_input: list[str]) -> None:
    parsed: list[Monkey] = parse_input(simple_input)
    assert level_of_monkey_business(parsed, 1, True) == 24


@pytest.mark.line_profile.with_args(level_of_monkey_business)
def test_simple2_execute_20_rounds(simple_input: list[str]) -> None:
    parsed: list[Monkey] = parse_input(simple_input)
    assert level_of_monkey_business(parsed, 20, True) == 10197


def test_simple2_execute_200_rounds(simple_input: list[str]) -> None:
    parsed: list[Monkey] = parse_input(simple_input)
    assert level_of_monkey_business(parsed, 200, True) == 1059870


def test_simple2_execute_1000_rounds(simple_input: list[str]) -> None:
    parsed: list[Monkey] = parse_input(simple_input)
    assert level_of_monkey_business(parsed, 1000, True) == 27019168


def test_simple2_execute_10000_rounds(simple_input: list[str]) -> None:
    parsed: list[Monkey] = parse_input(simple_input)
    assert level_of_monkey_business(parsed, 10000, True) == 2713310158


def test_task2_execute_rounds(complete_input: list[str]) -> None:
    parsed: list[Monkey] = parse_input(complete_input)
    assert level_of_monkey_business(parsed, 10000, True) == 14106266886
