import pytest


def has_only_unique_chars(array: list[str]) -> bool:
    unique_array: list[str] = set(array)  # type: ignore
    return len(unique_array) == len(array)


def endpos_of_marker(distinct_count: int, datastream: str) -> int:
    prev_chars: list[str] = []
    for index, character in enumerate(datastream):
        if len(prev_chars) >= distinct_count:
            del prev_chars[0]
        prev_chars.append(character)

        if len(prev_chars) == distinct_count and has_only_unique_chars(prev_chars):
            return index + 1
    return -1


@pytest.fixture(name="datastream")
def datastream_fixture() -> str:
    return open('Day 06/input.txt', encoding="utf-8").readline()


@pytest.mark.parametrize(
    "datastream, expected_endpos",
    [("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 7),
     ("bvwbjplbgvbhsrlpgdmjqwftvncz", 5),
     ("nppdvjthqldpwncqszvftbrmjlhg", 6),
     ("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 10),
     ("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 11)],
)
def test_day06_simple1(datastream: str, expected_endpos: int) -> None:
    assert endpos_of_marker(4, datastream) == expected_endpos


def test_day06_task1(datastream: str) -> None:
    assert endpos_of_marker(4, datastream) == 1361


@pytest.mark.parametrize(
    "datastream, expected_endpos",
    [("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 19),
     ("bvwbjplbgvbhsrlpgdmjqwftvncz", 23),
     ("nppdvjthqldpwncqszvftbrmjlhg", 23),
     ("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 29),
     ("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 26)],
)
def test_day06_simple2(datastream: str, expected_endpos: int) -> None:
    assert endpos_of_marker(14, datastream) == expected_endpos


def test_day06_task2(datastream: str) -> None:
    assert endpos_of_marker(14, datastream) == 3263
