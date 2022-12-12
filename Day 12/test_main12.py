from __future__ import annotations
from typing import Generic, TypeVar
import sys
import pytest


class Pos:
    def __init__(self, x: int, y: int) -> None:  # pylint: disable=C0103
        self.x: int = x  # pylint: disable=C0103
        self.y: int = y  # pylint: disable=C0103

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Pos):
            return self.x == other.x and self.y == other.y
        return NotImplemented

    def __hash__(self):
        return hash(tuple(sorted(self.__dict__.items())))

    def __repr__(self) -> str:
        return f"Post({self.x},{self.y})"

    def __str__(self) -> str:
        return f"Post({self.x},{self.y})"


class Square:

    def __init__(self, pos: Pos, height_str: str) -> None:
        self.pos: Pos = pos
        self.neighbours: list[Square] = []
        self.height_str: str = height_str

        if height_str == "S":
            self.height: int = 0
        elif height_str == "E":
            self.height: int = 25
        else:
            self.height: int = ord(height_str) - 97

    def __repr__(self) -> str:
        return f"Square({self.pos}, {self.height_str})"


_IT = TypeVar("_IT")


class Graph(Generic[_IT]):
    def __init__(self, nodes: list[_IT], graph: dict[_IT, dict[_IT, int]]) -> None:
        self.nodes: list[_IT] = nodes
        self.graph: dict[_IT, dict[_IT, int]] = graph

    def get_nodes(self) -> list[_IT]:
        "Returns the nodes of the graph."
        return self.nodes

    def get_outgoing_edges(self, node: _IT) -> list[_IT]:
        "Returns the neighbors of a node."
        connections: list[_IT] = []
        for out_node in self.nodes:
            if self.graph[node].get(out_node, False) is not False:
                connections.append(out_node)
        return connections

    def value(self, node1: _IT, node2: _IT) -> int:
        "Returns the value of an edge between two nodes."
        return self.graph[node1][node2]


def dijkstra_algorithm(graph: Graph[_IT], start_node: _IT) -> tuple[dict[_IT, _IT], dict[_IT, int]]:
    unvisited_nodes: list[_IT] = list(graph.get_nodes())

    # We'll use this dict to save the cost of visiting each node and update it as we move along the graph
    shortest_path: dict[_IT, int] = {}

    # We'll use this dict to save the shortest known path to a node found so far
    previous_nodes: dict[_IT, _IT] = {}

    # We'll use max_value to initialize the "infinity" value of the unvisited nodes
    max_value: int = sys.maxsize
    for node in unvisited_nodes:
        shortest_path[node] = max_value
    # However, we initialize the starting node's value with 0
    shortest_path[start_node] = 0

    # The algorithm executes until we visit all nodes
    while unvisited_nodes:
        # The code block below finds the node with the lowest score
        current_min_node: _IT | None = None
        for node in unvisited_nodes:  # Iterate over the nodes
            if current_min_node is None:
                current_min_node = node
            elif shortest_path[node] < shortest_path[current_min_node]:
                current_min_node = node

        # The code block below retrieves the current node's neighbors and updates their distances
        neighbors: list[_IT] = graph.get_outgoing_edges(current_min_node)  # type: ignore
        for neighbor in neighbors:
            tentative_value: int = shortest_path[current_min_node] + graph.value(current_min_node, neighbor)  # type: ignore
            if tentative_value < shortest_path[neighbor]:
                shortest_path[neighbor] = tentative_value
                # We also update the best path to the current node
                previous_nodes[neighbor] = current_min_node  # type: ignore

        # After visiting its neighbors, we mark the node as "visited"
        unvisited_nodes.remove(current_min_node)  # type: ignore

    return previous_nodes, shortest_path


def parse_heightmap_graph(heightmap_lines: list[str]) -> dict[Pos, Square]:
    heightmap: dict[Pos, Square] = {}

    for y_idx, line in enumerate(heightmap_lines):
        for x_idx, char in enumerate(line.strip()):
            heightmap[Pos(x_idx, y_idx)] = Square(Pos(x_idx, y_idx), char)

    for item in heightmap.values():
        add_neighbour_if_exists(heightmap, item, Pos(item.pos.x, item.pos.y - 1))
        add_neighbour_if_exists(heightmap, item, Pos(item.pos.x + 1, item.pos.y))
        add_neighbour_if_exists(heightmap, item, Pos(item.pos.x, item.pos.y + 1))
        add_neighbour_if_exists(heightmap, item, Pos(item.pos.x - 1, item.pos.y))

    return heightmap


def add_neighbour_if_exists(heightmap: dict[Pos, Square], item: Square, neighbour_pos: Pos) -> None:
    neighbour: Square | None = heightmap.get(neighbour_pos)
    if neighbour:
        item.neighbours.append(neighbour)


def get_path_grid_to_display(previous_nodes: dict[Pos, Pos], start_node: Pos, target_node: Pos) -> str:
    path: list[Pos] = []
    node: Pos = target_node

    while node != start_node:
        path.append(node)
        node = previous_nodes[node]

    # Add the start node manually
    path.append(start_node)

    max_x: int = max(pos.x for pos in path)
    max_y: int = max(pos.y for pos in path)

    grid: list[list[str]] = []
    for x_idx in range(max_x + 1):
        grid.append([])
        for _ in range(max_y + 1):
            grid[x_idx].append(".")

    for path_item_idx, path_item in enumerate(path):
        grid[path_item.x][path_item.y] = get_direction_str(path_item_idx, path)

    grid[start_node.x][start_node.y] = "E"
    grid[target_node.x][target_node.y] = "S"

    grid_str: str = ""
    for y_idx in range(len(grid[0])):
        for x_item in grid:
            grid_str += x_item[y_idx]
        grid_str += "\n"

    return grid_str


def get_direction_str(path_item_idx: int, path: list[Pos]) -> str:
    if path_item_idx+1 >= len(path):
        return "S"

    current_item: Pos = path[path_item_idx]
    next_item = path[path_item_idx+1]
    if next_item.y < current_item.y:
        return "^"
    elif next_item.y > current_item.y:
        return "v"
    elif next_item.x < current_item.x:
        return "<"
    elif next_item.x > current_item.x:
        return ">"

    raise NotImplementedError()


def get_shortest_path_length(heightmap: dict[Pos, Square], start_node: Square) -> tuple[dict[Pos, Pos], dict[Pos, int]]:
    nodes: list[Pos] = list(heightmap.keys())

    graph: dict[Pos, dict[Pos, int]] = {}
    for node in nodes:
        graph[node] = {}

    for square in heightmap.values():
        for neighbour in square.neighbours:
            if neighbour.height <= square.height + 1:
                graph[neighbour.pos][square.pos] = 1  # reverse path as we always search from end to start

    return dijkstra_algorithm(Graph(nodes, graph), start_node.pos)


def get_shortest_path_length_for_all(heightmap: dict[Pos, Square], possible_start_height_str: list[str], print_grid: bool = False) -> int | None:
    start_node: Square = next(square for square in heightmap.values() if square.height_str == "E")
    end_nodes: list[Square] = [square for square in heightmap.values() if square.height_str in possible_start_height_str]

    previous_nodes, shortest_path = get_shortest_path_length(heightmap, start_node)

    shortest_path_length: int = sys.maxsize
    for end_node in end_nodes:
        shortest_path_length = min(shortest_path_length, shortest_path[end_node.pos])

        if print_grid and shortest_path[end_node.pos] != sys.maxsize:
            path_grid: str = get_path_grid_to_display(previous_nodes, start_node=start_node.pos, target_node=end_node.pos)
            print(path_grid)

    return shortest_path_length if shortest_path_length != sys.maxsize else None


@ pytest.fixture(name="simple_input")
def simple_input_fixture() -> list[str]:
    return open('Day 12/input_simple.txt', encoding="utf-8").readlines()


@ pytest.fixture(name="simple_input_not_possible")
def simple_input_not_possible_fixture() -> list[str]:
    return open('Day 12/input_simple_not_possible.txt', encoding="utf-8").readlines()


@ pytest.fixture(name="complete_input")
def complete_input_fixture() -> list[str]:
    return open('Day 12/input.txt', encoding="utf-8").readlines()


def test_simple1_parse_heightmap(simple_input: list[str]) -> None:
    heightmap: dict[Pos, Square] = parse_heightmap_graph(simple_input)
    assert len(heightmap) == 40
    assert heightmap[Pos(0, 0)].height_str == "S"
    assert heightmap[Pos(0, 0)].height == 0
    assert heightmap[Pos(0, 1)].height_str == "a"
    assert heightmap[Pos(0, 1)].height == 0
    assert heightmap[Pos(5, 2)].height_str == "E"
    assert heightmap[Pos(5, 2)].height == 25
    assert heightmap[Pos(5, 2)].neighbours[0].height_str == "x"
    assert heightmap[Pos(5, 2)].neighbours[1].height_str == "x"
    assert heightmap[Pos(5, 2)].neighbours[2].height_str == "v"
    assert heightmap[Pos(5, 2)].neighbours[3].height_str == "z"


def test_simple1_shortest_path(simple_input: list[str]) -> None:
    heightmap: dict[Pos, Square] = parse_heightmap_graph(simple_input)
    shortest_path_length: int | None = get_shortest_path_length_for_all(heightmap, ["S"], print_grid=True)
    assert shortest_path_length == 31


def test_simple1_shortest_path_not_possible(simple_input_not_possible: list[str]) -> None:
    heightmap: dict[Pos, Square] = parse_heightmap_graph(simple_input_not_possible)
    shortest_path_length: int | None = get_shortest_path_length_for_all(heightmap, ["S"])
    assert shortest_path_length is None


def test_task1_shortest_path(complete_input: list[str]) -> None:
    heightmap: dict[Pos, Square] = parse_heightmap_graph(complete_input)
    shortest_path_length: int | None = get_shortest_path_length_for_all(heightmap, ["S"])
    assert shortest_path_length == 361


def test_simple2_shortest_path(simple_input: list[str]) -> None:
    heightmap: dict[Pos, Square] = parse_heightmap_graph(simple_input)
    shortest_path_length: int | None = get_shortest_path_length_for_all(heightmap, ["S", "a"], print_grid=True)
    assert shortest_path_length == 29


def test_task2_shortest_path(complete_input: list[str]) -> None:
    heightmap: dict[Pos, Square] = parse_heightmap_graph(complete_input)
    shortest_path_length: int | None = get_shortest_path_length_for_all(heightmap, ["S", "a"])
    assert shortest_path_length == 354
