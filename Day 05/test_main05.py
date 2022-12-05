import pytest
import re
import numpy

class Command:
    def __init__(self, count: str, stack_from:str, stack_to:str) -> None:
        self.count: int = int(count)
        self.stack_from: int = int(stack_from)
        self.stack_to: int = int(stack_to)

def parse_command(command_str: str) -> Command:
    (_, count_str, _, from_str, _, to_str) = command_str.split()
    return Command(count_str, from_str, to_str)

def parse_commands(input_simple_commands: list[str]) -> list[Command]:
    return [parse_command(command_str) for command_str in input_simple_commands]

def whats_on_the_top_stacks(input_simple_start: list[list[str]], input_simple_commands: list[str]) -> str:
    commands = parse_commands(input_simple_commands)
    for command in commands:
        for _ in range(command.count):
            input_simple_start[command.stack_to-1].append(input_simple_start[command.stack_from-1].pop())
    
    return ''.join([stack[-1] for stack in input_simple_start])

def whats_on_the_top_stacks_v2(input_simple_start: list[list[str]], input_simple_commands: list[str]) -> str:
    commands = parse_commands(input_simple_commands)
    for command in commands:
        input_simple_start[command.stack_to-1].extend(input_simple_start[command.stack_from-1][-command.count:])
        del input_simple_start[command.stack_from-1][len(input_simple_start[command.stack_from-1]) -command.count:]
    
    return ''.join([stack[-1] for stack in input_simple_start])

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
    assert whats_on_the_top_stacks(input_simple_start, input_simple_commands) == "CMZ"

def test_day05_task1(input_long_start: list[list[str]], input_long_commands: list[str]) -> None:
    assert whats_on_the_top_stacks(input_long_start, input_long_commands) == "JRVNHHCSJ"    

def test_day05_simple2(input_simple_start: list[list[str]], input_simple_commands: list[str]) -> None:
    assert whats_on_the_top_stacks_v2(input_simple_start, input_simple_commands) == "MCD" 

def test_day05_task2(input_long_start: list[list[str]], input_long_commands: list[str]) -> None:
    assert whats_on_the_top_stacks_v2(input_long_start, input_long_commands) == "GNFBSBJLH"        