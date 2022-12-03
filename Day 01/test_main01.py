import numpy

def top3_elves_with_most_calories(calories_list):
    elves = [0]

    for calories in calories_list:
        if calories == "\n":
            elves.append(0)
        else:
            elves[len(elves) - 1] += int(calories)

    elves.sort(reverse=True)
    return elves[:3]

def how_much_elf_with_most_calories(calories_list):
    return numpy.max(top3_elves_with_most_calories(calories_list))

def how_much_top3_elves_with_most_calories(calories_list):
    return numpy.sum(top3_elves_with_most_calories(calories_list))



def test_simple1():
    input = [1000, 2000, 3000, "\n", 4000, "\n", 5000, 6000, "\n", 7000, 8000, 9000, "\n", 10000]
    assert how_much_elf_with_most_calories(input) == 24000

def test_task1():
    with open('Day 01/input.txt') as f:
        input = f.readlines()
    assert how_much_elf_with_most_calories(input) == 67633

def test_simple2_list():
    input = [1000, 2000, 3000, "\n", 4000, "\n", 5000, 6000, "\n", 7000, 8000, 9000, "\n", 10000]
    assert top3_elves_with_most_calories(input) == [24000, 11000, 10000]

def test_simple2_item():
    input = [1000, 2000, 3000, "\n", 4000, "\n", 5000, 6000, "\n", 7000, 8000, 9000, "\n", 10000]
    assert how_much_top3_elves_with_most_calories(input) == 45000

def test_task2():
    with open('Day 01/input.txt') as f:
        input = f.readlines()
    assert how_much_top3_elves_with_most_calories(input) == 199628