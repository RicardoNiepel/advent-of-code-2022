import pytest

def parse_play(playstring: str) -> str:
    switch_playstring: dict[str, str] = {
        "A": "ROCK",
        "X": "ROCK",
        "B": "PAPER",
        "Y": "PAPER",
        "C": "SCISSORS",
        "Z": "SCISSORS"
    }
    return switch_playstring[playstring]

def parse_outcome(outcomestring: str) -> str:
    switch_outcomestring: dict[str, str] = {
        "X": "LOSE",
        "Y": "DRAW",
        "Z": "WIN"
    }
    return switch_outcomestring[outcomestring]

def get_myselected_score(play: str) -> int:
    switch_playscore: dict[str, int] = {
        "ROCK": 1,
        "PAPER": 2,
        "SCISSORS": 3,
    }
    return switch_playscore[play]

def i_won(opponent_play: str, me_play: str) -> bool:
    if me_play == "ROCK":
        if opponent_play == "SCISSORS":
            return True
    if me_play == "PAPER":
        if opponent_play == "ROCK":
            return True
    if me_play == "SCISSORS":
        if opponent_play == "PAPER":
            return True
    return False

def get_outcome_score(opponent_play: str, me_play: str) -> int:
    if opponent_play == me_play:
        return 3 # draw
    if i_won(opponent_play, me_play):
        return 6 # won
    else:
        return 0 # lost

def score_by_strategy_guide(turn: str) -> int:
    (opponent_str, me_str) = turn.split()

    opponent = parse_play(opponent_str)
    me = parse_play(me_str)
    
    return get_myselected_score(me) + get_outcome_score(opponent, me)

def total_score_by_strategy_guide(game_list: list[str]) -> int:
    return sum([score_by_strategy_guide(turn) for turn in game_list])

def get_play(opponent: str, outcome: str) -> str:
    if outcome == "DRAW":
        return opponent
    if outcome == "WIN":
        if opponent == "SCISSORS":
            return "ROCK"
        if opponent == "ROCK":
            return "PAPER"
        else:
            return "SCISSORS"
    else: # LOSE
        if opponent == "SCISSORS":
            return "PAPER"
        if opponent == "ROCK":
            return "SCISSORS"
        else:
            return "ROCK"

def score_by_strategy_guide_v2(turn: str) -> int:
    (play_str, outcome_str) = turn.split()

    opponent = parse_play(play_str)
    outcome = parse_outcome(outcome_str)
    me = get_play(opponent, outcome)
    
    return get_myselected_score(me) + get_outcome_score(opponent, me)

def total_score_by_strategy_guide_v2(game_list: list[str]) -> int:
    return sum([score_by_strategy_guide_v2(turn) for turn in game_list])

@pytest.fixture
def input_simple() -> list[str]:
    return open('Day 02/input_simple.txt').readlines()

@pytest.fixture
def input_long() -> list[str]:
    return open('Day 02/input.txt').readlines()

def test_day02_simple1(input_simple: list[str]) -> None:
    assert total_score_by_strategy_guide(input_simple) == 15

def test_day02_task1(input_long: list[str]) -> None:
    assert total_score_by_strategy_guide(input_long) == 12535    

def test_day02_simple2(input_simple: list[str]) -> None:
    assert total_score_by_strategy_guide_v2(input_simple) == 12

def test_day02_task2(input_long: list[str]) -> None:
    assert total_score_by_strategy_guide_v2(input_long) == 15457 