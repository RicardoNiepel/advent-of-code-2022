def parse_play(playstring):
    switch_playstring = {
        "A": "ROCK",
        "X": "ROCK",
        "B": "PAPER",
        "Y": "PAPER",
        "C": "SCISSORS",
        "Z": "SCISSORS"
    }
    return switch_playstring.get(playstring)

def parse_outcome(outcomestring):
    switch_outcomestring = {
        "X": "LOSE",
        "Y": "DRAW",
        "Z": "WIN"
    }
    return switch_outcomestring.get(outcomestring)    

def get_myselected_score(play):
    switch_playscore = {
        "ROCK": 1,
        "PAPER": 2,
        "SCISSORS": 3,
    }
    return switch_playscore.get(play)

def i_won(opponent_play, me_play):
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

def get_outcome_score(opponent_play, me_play):
    if opponent_play == me_play:
        return 3 # draw
    if i_won(opponent_play, me_play):
        return 6 # won
    else:
        return 0 # lost

def score_by_strategy_guide(turn):
    plays = turn.split()

    opponent = parse_play(plays[0])
    me = parse_play(plays[1])
    
    return get_myselected_score(me) + get_outcome_score(opponent, me)

def total_score_by_strategy_guide(game_list):
    score = 0

    for turn in game_list:
        score += score_by_strategy_guide(turn)

    return score

def get_play(opponent, outcome):
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

def score_by_strategy_guide_v2(turn):
    plays = turn.split()

    opponent = parse_play(plays[0])
    outcome = parse_outcome(plays[1])
    me = get_play(opponent, outcome)
    
    return get_myselected_score(me) + get_outcome_score(opponent, me)

def total_score_by_strategy_guide_v2(game_list):
    score = 0

    for turn in game_list:
        score += score_by_strategy_guide_v2(turn)

    return score

def test_day02_simple1():
    with open('Day 02/input_simple.txt') as f:
        input = f.readlines()
    assert total_score_by_strategy_guide(input) == 15

def test_day02_task1():
    with open('Day 02/input.txt') as f:
        input = f.readlines()
    assert total_score_by_strategy_guide(input) == 12535    

def test_day02_simple2():
    with open('Day 02/input_simple.txt') as f:
        input = f.readlines()
    assert total_score_by_strategy_guide_v2(input) == 12

def test_day02_task2():
    with open('Day 02/input.txt') as f:
        input = f.readlines()
    assert total_score_by_strategy_guide_v2(input) == 15457 