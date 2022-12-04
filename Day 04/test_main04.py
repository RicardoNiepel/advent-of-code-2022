def range_contains(r1, r2):
    if r1[0] in r2 and r1[-1] in r2:
        return r1
    if r2[0] in r1 and r2[-1] in r1:
        return r2
    return None

def range_overlaps(r1, r2):
    return range(max(r1.start,r2.start), min(r1.stop,r2.stop)) or None

def create_range(elf_string):
    elf = elf_string.split("-")
    return range(int(elf[0]), int(elf[1])+1) # +1 because we need inclusive ranges

def check_assignment(assignment, range_check_func):
    elves = assignment.split(",")
    return range_check_func(create_range(elves[0]), create_range(elves[1]))

def count_of_assignments(assignments, filter_func):
    count = 0
    for assignment in assignments:
        count += 1 if check_assignment(assignment, filter_func) != None else 0
    return count

# Tests

def test_day04_simple1():
    with open('Day 04/input_simple.txt') as f:
        input = f.readlines()
    assert count_of_assignments(input, range_contains) == 2

def test_day04_task1():
    with open('Day 04/input.txt') as f:
        input = f.readlines()
    assert count_of_assignments(input, range_contains) == 582

def test_day04_simple2():
    with open('Day 04/input_simple.txt') as f:
        input = f.readlines()
    assert count_of_assignments(input, range_overlaps) == 4

def test_day04_task2():
    with open('Day 04/input.txt') as f:
        input = f.readlines()
    assert count_of_assignments(input, range_overlaps) == 893