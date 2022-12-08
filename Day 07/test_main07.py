from __future__ import annotations
from typing import Any, Callable, Iterable, TypeVar
import pytest
from parse import parse  # type: ignore # pylint: disable=redefined-builtin

# BEGIN missing things at Python, the language I don't like
_T = TypeVar("_T")


def first(__function: Callable[[_T], Any], __iterable: Iterable[_T]) -> _T:
    """Need to create this as Python does not have something like this built-in"""
    first_item: Any | None = next(filter(__function, __iterable), None)
    if first_item is None:
        raise Exception("No first item found with filter")
    return first_item

# END missing things at Python, the language I don't like


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


def parse_terminal_output(terminal_output: str) -> Folder:
    root: Folder = Folder("/", None, [])
    current_parent: Folder = root

    for line in terminal_output:
        line: str = line.strip()

        if line == "$ cd /":
            current_parent: Folder = root
        elif line == "$ cd ..":
            if current_parent.parent:
                current_parent: Folder = current_parent.parent
            else:
                raise Exception("Already at root folder")
        elif parsed := parse('$ cd {dir_name:w}', line):
            current_parent = [child for child in current_parent.childs if child.name == parsed["dir_name"]][0]  # type: ignore
        elif line == "$ ls":
            pass  # just ignore for now
        elif parsed := parse('dir {dir_name:w}', line):
            current_parent.childs.append(Folder(parsed["dir_name"], current_parent, []))  # type: ignore
        elif parsed := parse('{file_size:d} {file_name}', line):
            current_parent.childs.append(File(parsed["file_name"], parsed["file_size"]))  # type: ignore
        else:
            raise Exception("Cloud not be parsed: " + line)

    return root


def flat_folders(folder: Folder) -> list[Folder]:
    child_folders: list[Folder] = [child_child
                                   for child in folder.childs if isinstance(child, Folder)
                                   for child_child in flat_folders(child)]
    return [folder] + child_folders


def sizeof_folderswith_atmost100000(terminal_output: str) -> int:
    root_folder: Folder = parse_terminal_output(terminal_output)
    flatten_folders: list[Folder] = flat_folders(root_folder)
    return sum(folder.size() for folder in flatten_folders if folder.size() <= 100000)


def sizeof_folder_todelete(terminal_output: str) -> int:
    root_folder: Folder = parse_terminal_output(terminal_output)

    disk_space: int = 70000000
    required_space: int = 30000000
    needed_space: int = required_space - (disk_space - root_folder.size())

    flatten_folders: list[Folder] = flat_folders(root_folder)
    flatten_folders.sort(key=lambda f: f.size())

    # Ugly Python version 1: return [folder for folder in flatten_folders if folder.size() >= needed_space][0].size()
    # Ugly Python version 2: return [folder.size() for folder in flatten_folders if folder.size() >= needed_space][0]
    # Ugly Python version 3: return next(folder.size() for folder in flatten_folders if folder.size() >= needed_space)
    # Ugly Python version 4: return list(filter(lambda f: f.size() >= needed_space, flatten_folders))[0].size()
    # Ugly Python version 5: return next(filter(lambda f: f.size() >= needed_space, flatten_folders)).size()
    return first(lambda f: f.size() >= needed_space, flatten_folders).size()


@pytest.fixture(name="simple_terminal_output")
def simple_terminal_output_fixture() -> list[str]:
    return open('Day 07/input_simple.txt', encoding="utf-8").readlines()


@pytest.fixture(name="all_terminal_output")
def all_terminal_output_fixture() -> list[str]:
    return open('Day 07/input.txt', encoding="utf-8").readlines()


def test_day07_simple1_sizeof_allfiles(simple_terminal_output: str) -> None:
    root_folder: Folder = parse_terminal_output(simple_terminal_output)
    sizeof_allfiles: int = root_folder.size()
    assert sizeof_allfiles == 48381165


def test_day07_flat_folders(simple_terminal_output: str) -> None:
    root_folder: Folder = parse_terminal_output(simple_terminal_output)
    assert len(flat_folders(root_folder)) == 4


def test_day07_simple1_sizeof_folderswith_atmost100000(simple_terminal_output: str) -> None:
    assert sizeof_folderswith_atmost100000(simple_terminal_output) == 95437


def test_day07_task1_sizeof_folderswith_atmost100000(all_terminal_output: str) -> None:
    assert sizeof_folderswith_atmost100000(all_terminal_output) == 1444896


def test_day07_simple1_sizeof_folder_todelete(simple_terminal_output: str) -> None:
    assert sizeof_folder_todelete(simple_terminal_output) == 24933642


def test_day07_task1_sizeof_folder_todelete(all_terminal_output: str) -> None:
    assert sizeof_folder_todelete(all_terminal_output) == 404395
