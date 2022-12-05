from typing import Callable
from parse import parse  # type: ignore # pylint: disable=redefined-builtin
import pytest


class Command:
    def __init__(self, cmd_str: str) -> None:
        (count_cmd, from_nr, to_nr) = parse('move {:d} from {:d} to {:d}', cmd_str.strip())  # type: ignore
        self.count: int = count_cmd
        self.from_idx: int = from_nr - 1
        self.to_idx: int = to_nr - 1


def parse_cmds(cmd_strs: list[str]) -> list[Command]:
    return [Command(cmd_str) for cmd_str in cmd_strs]


def move_one_by_one(stacks: list[list[str]], cmd: Command) -> None:
    for _ in range(cmd.count):
        stacks[cmd.to_idx].append(stacks[cmd.from_idx].pop())


def move_complete_range(stacks: list[list[str]], cmd: Command) -> None:
    stacks[cmd.to_idx].extend(stacks[cmd.from_idx][-cmd.count:])
    del stacks[cmd.from_idx][-cmd.count:]


def get_stacks_top_after_move_cmds(stacks: list[list[str]], cmd_strs: list[str], move_func: Callable[[list[list[str]], Command], None]) -> str:
    for cmd in parse_cmds(cmd_strs):
        move_func(stacks, cmd)
    return ''.join([stack[-1] for stack in stacks])


@pytest.fixture(name="simple_stacks")
def simple_stacks_fixture() -> list[list[str]]:
    stacks: list[list[str]] = []
    stacks.append(["Z", "N"])
    stacks.append(["M", "C", "D"])
    stacks.append(["P"])
    return stacks


@pytest.fixture(name="all_stacks")
def all_stacks_fixture() -> list[list[str]]:
    stacks: list[list[str]] = []
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


@pytest.fixture(name="simple_cmds")
def simple_cmds_fixture() -> list[str]:
    return open('Day 05/input_simple.txt', encoding="utf-8").readlines()


@pytest.fixture(name="all_cmds")
def all_cmds_fixture() -> list[str]:
    return open('Day 05/input.txt', encoding="utf-8").readlines()


def test_day05_simple1(simple_stacks: list[list[str]], simple_cmds: list[str]) -> None:
    assert get_stacks_top_after_move_cmds(simple_stacks, simple_cmds, move_one_by_one) == "CMZ"


def test_day05_task1(all_stacks: list[list[str]], all_cmds: list[str]) -> None:
    assert get_stacks_top_after_move_cmds(all_stacks, all_cmds, move_one_by_one) == "JRVNHHCSJ"


def test_day05_simple2(simple_stacks: list[list[str]], simple_cmds: list[str]) -> None:
    assert get_stacks_top_after_move_cmds(simple_stacks, simple_cmds, move_complete_range) == "MCD"


def test_day05_task2(all_stacks: list[list[str]], all_cmds: list[str]) -> None:
    assert get_stacks_top_after_move_cmds(all_stacks, all_cmds, move_complete_range) == "GNFBSBJLH"
