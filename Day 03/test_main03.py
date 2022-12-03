
def priority(char):
    if str(char).isupper():
        return ord(char)-38
    else:
        return ord(char)-96

def dublicated_item(rucksack):
    half = int(len(rucksack)/2)
    comp1 = rucksack[:half]
    comp2 = rucksack[half:]

    for char in comp1:
        if char in comp2:
            return char

def dublicated_items_priority(rucksack):
    item = dublicated_item(rucksack)
    return priority(item)

def items_appearing_in_both_priority(rucksacks):
    priority = 0

    for rucksack in rucksacks:
        priority += dublicated_items_priority(rucksack)

    return priority

def dublicated_items_priority_three(rucksack1, rucksack2, rucksack3):
    for char in rucksack1:
        if char in rucksack2 and char in rucksack3:
            return priority(char)

def badge_items_priority(rucksacks):
    priority = 0

    for x in range(0, len(rucksacks), 3):
        priority += dublicated_items_priority_three(rucksacks[x], rucksacks[x+1], rucksacks[x+2])

    return priority


def test_day03_int():
    assert priority("a") == 1
    assert priority("z") == 26
    assert priority("A") == 27
    assert priority("Z") == 52

def test_day03_simple1():
    with open('Day 03/input_simple.txt') as f:
        input = f.readlines()
    assert items_appearing_in_both_priority(input) == 157

def test_day03_task1():
    with open('Day 03/input.txt') as f:
        input = f.readlines()
    assert items_appearing_in_both_priority(input) == 8298

def test_day03_simple2():
    with open('Day 03/input_simple.txt') as f:
        input = f.readlines()
    assert badge_items_priority(input) == 70      

def test_day03_task2():
    with open('Day 03/input.txt') as f:
        input = f.readlines()
    assert badge_items_priority(input) == 2708      