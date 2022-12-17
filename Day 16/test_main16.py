from __future__ import annotations
from collections import deque
import re
import pytest


class Valve:
    def __init__(self, name: str, flow_rate: int) -> None:
        self.name: str = name
        self.flow_rate: int = flow_rate
        self.tunnel_to: set[Valve] = set()

    def add_tunnel(self, other_valve: Valve) -> None:
        self.tunnel_to.add(other_valve)
        other_valve.tunnel_to.add(self)

    def __repr__(self) -> str:
        return f"{self.name}={self.flow_rate} => {', '.join(valve.name for valve in self.tunnel_to)}"


def parse(input_lines: list[str]) -> list[Valve]:
    valves: list[Valve] = []
    for line in input_lines:
        match: re.Match[str] = re.search(r'Valve ([A-Z]+) has flow rate=(\d+); tunnels? leads? to valves? ([A-Z,\s]*)', line.strip())  # type: ignore

        valve_to_add: Valve = Valve(match.group(1), int(match.group(2)))
        valves.append(valve_to_add)
        for tunnel_dest in match.group(3).split(", "):
            dest: Valve | None = next((valve for valve in valves if valve.name == tunnel_dest), None)
            if dest is not None:
                valve_to_add.add_tunnel(dest)

    return valves


def distances_for_useful_valves(valves: list[Valve]) -> dict[str, dict[str, int]]:
    distances: dict[str, dict[str, int]] = {}

    for start_valve in valves:
        if start_valve.name != "AA" and start_valve.flow_rate == 0:
            continue

        distances[start_valve.name] = {start_valve.name: 0, "AA": 0}
        visited_valves: set[Valve] = {start_valve}

        queue: deque[tuple[int, Valve]] = deque([(0, start_valve)])
        while queue:
            distance, last_end_valve = queue.popleft()
            for end_valve in last_end_valve.tunnel_to:
                if end_valve in visited_valves:
                    continue
                visited_valves.add(end_valve)
                if end_valve.flow_rate > 0:  # useful_valve
                    distances[start_valve.name][end_valve.name] = distance + 1
                queue.append((distance + 1, end_valve))

        del distances[start_valve.name][start_valve.name]
        if start_valve.name != "AA":
            del distances[start_valve.name]["AA"]

    return distances


def calc_most_pressure(valves: list[Valve], start: str, duration: int, with_elephant: bool) -> int:
    distances: dict[str, dict[str, int]] = distances_for_useful_valves(valves)

    cache: dict[tuple[int, str, int], int] = {}
    indices: dict[str, int] = {valve.name: index for index, valve in enumerate(val for val in valves if val.flow_rate > 0)}
    flow_rates: dict[str, int] = {valve.name: valve.flow_rate for valve in valves}

    def dfs(duration: int, valve_name: str, valve_opened_bitmask: int) -> int:
        if (duration, valve_name, valve_opened_bitmask) in cache:
            return cache[(duration, valve_name, valve_opened_bitmask)]

        maxval: int = 0
        for neighbor in distances[valve_name]:
            valve_bit: int = 1 << indices[neighbor]
            if valve_opened_bitmask & valve_bit:
                continue
            remaining_duration: int = duration - distances[valve_name][neighbor] - 1
            if remaining_duration <= 0:
                continue
            maxval = max(maxval, dfs(remaining_duration, neighbor, valve_opened_bitmask | valve_bit) + flow_rates[neighbor] * remaining_duration)

        cache[(duration, valve_name, valve_opened_bitmask)] = maxval
        return maxval

    if with_elephant:
        bitmask: int = (1 << len(indices)) - 1
        max_pressure: int = 0
        for i in range((bitmask + 1) // 2):
            max_pressure = max(max_pressure, dfs(duration, start, i) + dfs(duration, start, bitmask ^ i))
    else:
        max_pressure = dfs(duration, start, 0)

    return max_pressure


@ pytest.fixture(name="simple_input")  # type: ignore
def simple_input_fixture() -> list[str]:
    return open('Day 16/input_simple.txt', encoding="utf-8").readlines()


@ pytest.fixture(name="complete_input")  # type: ignore
def complete_input_fixture() -> list[str]:
    return open('Day 16/input.txt', encoding="utf-8").readlines()


def test_parse(simple_input: list[str]) -> None:
    parsed_valves: list[Valve] = parse(simple_input)
    assert len(parsed_valves) == 10
    assert parsed_valves[1].name == "BB"
    assert parsed_valves[9].name == "JJ"
    assert "II" in (valve.name for valve in parsed_valves[9].tunnel_to)


# @pytest.mark.line_profile.with_args(calc_most_pressure)
def test_simple1_calc_most_pressure(simple_input: list[str]) -> None:
    parsed_valves: list[Valve] = parse(simple_input)
    pressure = calc_most_pressure(parsed_valves, "AA", duration=30, with_elephant=False)
    assert pressure == 1651


def test_task1_calc_most_pressure(complete_input: list[str]) -> None:
    parsed_valves: list[Valve] = parse(complete_input)
    pressure = calc_most_pressure(parsed_valves, "AA", duration=30, with_elephant=False)
    assert pressure == 1986


def test_simple2_calc_most_pressure_elephant(simple_input: list[str]) -> None:
    parsed_valves: list[Valve] = parse(simple_input)
    pressure = calc_most_pressure(parsed_valves, "AA", duration=26, with_elephant=True)
    assert pressure == 1707


def test_task2_calc_most_pressure_elephant(complete_input: list[str]) -> None:
    parsed_valves: list[Valve] = parse(complete_input)
    pressure = calc_most_pressure(parsed_valves, "AA", duration=26, with_elephant=True)
    assert pressure == 2464
