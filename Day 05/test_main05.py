from typing import Callable
from parse import * # type: ignore
import pytest

class Command:
    def __init__(self, command_str: str) -> None:
        (count_cmd, stack_from, stack_to) = search('move {:d} from {:d} to {:d}', command_str)  # type: ignore
        self.count: int = count_cmd
        self.stack_from: int = stack_from
        self.stack_to: int = stack_to

def parse_commands(input_simple_commands: list[str]) -> list[Command]:
    return [Command(command_str) for command_str in input_simple_commands]

def move_one_by_one(stacks: list[list[str]], command: Command) -> None:
    for _ in range(command.count):
        stacks[command.stack_to-1].append(stacks[command.stack_from-1].pop())

def move_complete_range(stacks: list[list[str]], command: Command) -> None:
    stacks[command.stack_to-1].extend(stacks[command.stack_from-1][-command.count:])
    del stacks[command.stack_from-1][len(stacks[command.stack_from-1]) -command.count:]        

def whats_on_the_top_stacks(stacks: list[list[str]], command_strings: list[str], move_func: Callable[[list[list[str]], Command], None]) -> str:
    commands: list[Command] = parse_commands(command_strings)
    for command in commands:
        move_func(stacks, command)
    
    return ''.join([stack[-1] for stack in stacks])    

@pytest.fixture
def input_simple_start() -> list[list[str]]:
    stacks:list[list[str]] = []
    stacks.append(["Z", "N"])
    stacks.append(["M", "C", "D"])
    stacks.append(["P"])
    return stacks

@pytest.fixture
def input_long_start() -> list[list[str]]:
    stacks:list[list[str]] = []
    stacks.append(["W", "D", "G", "B", "H", "R", "V"])
    stacks.append(["J", "N", "G", "C", "R", "F"])
    stacks.append(["L", "S", "F", "H", "D", "N", "J"])
    stacks.append(["J", "D", "S", "V"])
    stacks.append(["S", "H", "D", "R", "Q", "W", "N", "V"])
    stacks.append(["P", "G", "H", "C", "M"])
    stacks.append(["F", "J", "B", "G", "L", "Z", "H", "C"])
    stacks.append(["S", "J", "R"])
    stacks.append(["L", "G", "S", "R", "B", "N", "V", "M"])
    return stacks    

@pytest.fixture
def input_simple_commands() -> list[str]:
    return open('Day 05/input_simple.txt').readlines()

@pytest.fixture
def input_long_commands() -> list[str]:
    return open('Day 05/input.txt').readlines()

def test_day05_simple1(input_simple_start: list[list[str]], input_simple_commands: list[str]) -> None:
    assert whats_on_the_top_stacks(input_simple_start, input_simple_commands, move_one_by_one) == "CMZ"

def test_day05_task1(input_long_start: list[list[str]], input_long_commands: list[str]) -> None:
    assert whats_on_the_top_stacks(input_long_start, input_long_commands, move_one_by_one) == "JRVNHHCSJ"    

def test_day05_simple2(input_simple_start: list[list[str]], input_simple_commands: list[str]) -> None:
    assert whats_on_the_top_stacks(input_simple_start, input_simple_commands, move_complete_range) == "MCD" 

def test_day05_task2(input_long_start: list[list[str]], input_long_commands: list[str]) -> None:
    assert whats_on_the_top_stacks(input_long_start, input_long_commands, move_complete_range) == "GNFBSBJLH"        