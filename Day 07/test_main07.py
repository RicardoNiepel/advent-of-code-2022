from __future__ import annotations
from typing import Any
import pytest
from parse import parse  # type: ignore # pylint: disable=redefined-builtin


class File:
    def __init__(self, name: str, size: int) -> None:
        self.name: str = name
        self.size_internal: int = size

    def __repr__(self) -> str:
        return f"{self.size_internal} {self.name}"

    def size(self) -> int:
        return self.size_internal


class Folder:
    def __init__(self, name: str, parent: Folder | None, childs: list[Folder | File]) -> None:
        self.name: str = name
        self.parent: Folder | None = parent
        self.childs: list[Folder | File] = childs

    def __repr__(self) -> str:
        return f"dir {self.name}"

    def size(self) -> int:
        return sum(child.size() for child in self.childs)

    def __eq__(self, other: object) -> bool:
        return self.name == other.name and self.parent == other.parent  # type: ignore

    def __hash__(self) -> int:
        return hash(('name', self.name))


def parse_output(terminal_output: str) -> Folder:
    root: Folder = Folder("/", None, [])
    current_parent: Folder = root

    for line in terminal_output:
        if line == "$ cd /\n":
            current_parent: Folder = root
            continue
        if line == "$ cd ..\n":
            current_parent: Folder = current_parent.parent  # type: ignore
            continue
        if line == "$ ls\n":
            continue
        if ls_dir := parse('dir {:w}\n', line):  # type: ignore
            ls_dir = ls_dir[0]  # type: ignore
            current_parent.childs.append(Folder(ls_dir, current_parent, []))  # type: ignore
        if change_dir := parse('$ cd {:w}\n', line):  # type: ignore
            change_dir = change_dir[0]  # type: ignore
            current_parent = [child for child in current_parent.childs if child.name == change_dir][0]  # type: ignore
        if result := parse('{:d} {}', line):  # type: ignore
            (file_size, file_name) = result  # type: ignore
            current_parent.childs.append(File(file_name, file_size))  # type: ignore

    return root


def sizeof_allfiles(terminal_output: str) -> int:
    root_folder: Folder = parse_output(terminal_output)
    return root_folder.size()


def flatten(l: list[list[Any]]) -> list[Any]:
    return [item for sublist in l for item in sublist]


def filter_folders(folder: Folder, max_size_filter: int) -> list[Folder]:
    child_folders = [child for child in folder.childs if isinstance(child, Folder) and child.size() <= max_size_filter]
    child_child_folders = [filter_folders(child, max_size_filter) for child in folder.childs if isinstance(child, Folder)]

    if folder.size() <= max_size_filter:
        child_folders.append(folder)
    return child_folders + flatten(child_child_folders)


def sizeof_folderswith_atmost100000(terminal_output: str) -> int:
    root_folder: Folder = parse_output(terminal_output)
    filtered_folders: list[Folder] = filter_folders(root_folder, 100000)
    unique = set(filtered_folders)
    return sum(folder.size() for folder in unique)


def flat_folders(folder: Folder) -> list[Folder]:
    child_folders: list[Folder] = [child for child in folder.childs if isinstance(child, Folder)]
    child_child_folders: list[list[Folder]] = [flat_folders(child) for child in child_folders]

    child_folders.append(folder)
    return child_folders + flatten(child_child_folders)


def sizeof_folder_todelete(terminal_output: str) -> int:
    root_folder: Folder = parse_output(terminal_output)
    disk_space: int = 70000000
    required_space: int = 30000000
    needed_space: int = required_space - (disk_space - root_folder.size())

    flatten_folders: list[Folder] = flat_folders(root_folder)

    def size(folder: Folder) -> int:
        return folder.size()
    flatten_folders.sort(key=size)

    return [folder for folder in flatten_folders if folder.size() >= needed_space][0].size()


@pytest.fixture(name="simple_terminal_output")
def simple_terminal_output_fixture() -> list[str]:
    return open('Day 07/input_simple.txt', encoding="utf-8").readlines()


@pytest.fixture(name="all_terminal_output")
def all_terminal_output_fixture() -> list[str]:
    return open('Day 07/input.txt', encoding="utf-8").readlines()


def test_day07_simple1_sizeof_allfiles(simple_terminal_output: str) -> None:
    assert sizeof_allfiles(simple_terminal_output) == 48381165


def test_day07_simple1_sizeof_folderswith_atmost100000(simple_terminal_output: str) -> None:
    assert sizeof_folderswith_atmost100000(simple_terminal_output) == 95437


def test_day07_task1_sizeof_folderswith_atmost100000(all_terminal_output: str) -> None:
    assert sizeof_folderswith_atmost100000(all_terminal_output) == 1444896


def test_day07_simple1_sizeof_folder_todelete(simple_terminal_output: str) -> None:
    assert sizeof_folder_todelete(simple_terminal_output) == 24933642


def test_day07_task1_sizeof_folder_todelete(all_terminal_output: str) -> None:
    assert sizeof_folder_todelete(all_terminal_output) == 404395
