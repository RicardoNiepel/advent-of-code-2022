import pytest


def parse_tree_grid(tree_grid_str: str) -> list[list[int]]:
    grid: list[list[int]] = []

    for line in tree_grid_str:
        grid.append([int(char) for char in line.strip()])

    return grid


def is_visible(tree_tocheck_row: int, tree_tocheck_column: int, grid: list[list[int]]) -> bool:

    is_visible_left: bool = True
    for column in range(0, tree_tocheck_column):
        if grid[tree_tocheck_row][column] >= grid[tree_tocheck_row][tree_tocheck_column]:
            is_visible_left = False

    is_visible_right: bool = True
    for column in range(tree_tocheck_column + 1, len(grid[0])):
        if grid[tree_tocheck_row][column] >= grid[tree_tocheck_row][tree_tocheck_column]:
            is_visible_right = False

    is_visible_top: bool = True
    for row in range(0, tree_tocheck_row):
        if grid[row][tree_tocheck_column] >= grid[tree_tocheck_row][tree_tocheck_column]:
            is_visible_top = False

    is_visible_bottom: bool = True
    for row in range(tree_tocheck_row + 1, len(grid)):
        if grid[row][tree_tocheck_column] >= grid[tree_tocheck_row][tree_tocheck_column]:
            is_visible_bottom = False

    return is_visible_left or is_visible_right or is_visible_top or is_visible_bottom


def get_scenic_score(tree_tocheck_row: int, tree_tocheck_column: int, grid: list[list[int]]) -> int:

    trees_visible_left: int = 0
    for column in range(tree_tocheck_column - 1, -1, -1):
        trees_visible_left += 1
        if grid[tree_tocheck_row][column] >= grid[tree_tocheck_row][tree_tocheck_column]:
            break

    trees_visible_right: int = 0
    for column in range(tree_tocheck_column + 1, len(grid[0])):
        trees_visible_right += 1
        if grid[tree_tocheck_row][column] >= grid[tree_tocheck_row][tree_tocheck_column]:
            break

    trees_visible_top: int = 0
    for row in range(tree_tocheck_row - 1, -1, -1):
        trees_visible_top += 1
        if grid[row][tree_tocheck_column] >= grid[tree_tocheck_row][tree_tocheck_column]:
            break

    trees_visible_bottom: int = 0
    for row in range(tree_tocheck_row + 1, len(grid)):
        trees_visible_bottom += 1
        if grid[row][tree_tocheck_column] >= grid[tree_tocheck_row][tree_tocheck_column]:
            break

    return trees_visible_left * trees_visible_right * trees_visible_top * trees_visible_bottom


def how_many_trees_are_visible(grid: list[list[int]]) -> int:
    outside_trees_count: int = 2*len(grid) + 2*len(grid[0]) - 4

    visible_trees_inside_count: int = 0

    for row in range(1, len(grid) - 1):
        for column in range(1, len(grid[0]) - 1):
            visible_trees_inside_count += is_visible(row, column, grid)

    return outside_trees_count + visible_trees_inside_count


def max_scenic_score(grid: list[list[int]]) -> int:
    scenic_scores: list[int] = []

    for row in range(1, len(grid) - 1):
        for column in range(1, len(grid[0]) - 1):
            scenic_scores.append(get_scenic_score(row, column, grid))

    return max(scenic_scores)


@pytest.fixture(name="simple_tree_grid")
def simple_tree_grid_fixture() -> list[str]:
    return open('Day 08/input_simple.txt', encoding="utf-8").readlines()


@pytest.fixture(name="complete_tree_grid")
def complete_tree_grid_fixture() -> list[str]:
    return open('Day 08/input.txt', encoding="utf-8").readlines()


def test_day08_simple1_parse_grid(simple_tree_grid: str) -> None:
    grid: list[list[int]] = parse_tree_grid(simple_tree_grid)
    assert len(grid) == 5
    assert len(grid[0]) == 5
    assert grid[0][0] == 3
    assert grid[4][4] == 0


def test_day08_simple1_visible_trees(simple_tree_grid: str) -> None:
    grid: list[list[int]] = parse_tree_grid(simple_tree_grid)
    assert how_many_trees_are_visible(grid) == 21


def test_day08_task1_visible_trees(complete_tree_grid: str) -> None:
    grid: list[list[int]] = parse_tree_grid(complete_tree_grid)
    assert how_many_trees_are_visible(grid) == 1870


def test_day08_simple2_scenic_score(simple_tree_grid: str) -> None:
    grid: list[list[int]] = parse_tree_grid(simple_tree_grid)
    assert get_scenic_score(1, 2, grid) == 4
    assert get_scenic_score(3, 2, grid) == 8


def test_day08_task2_max_scenic_score(complete_tree_grid: str) -> None:
    grid: list[list[int]] = parse_tree_grid(complete_tree_grid)
    assert max_scenic_score(grid) == 517440
