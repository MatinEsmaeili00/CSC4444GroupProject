"""Monte Carlo equity estimation. No server, no JSON — just ints."""

import random
from treys import Evaluator
from .cards import FULL_DECK, to_treys

_evaluator = Evaluator()


def monte_carlo_equity(hole, board, n_opponents, n_sims=3000):
    """
    hole: list of 2 ints (0..51)
    board: list of 0, 3, 4, or 5 ints
    n_opponents: int >= 1
    Returns equity in [0, 1] = P(win) + 0.5 * P(tie).
    """
    if n_opponents < 1:
        return 1.0

    known = set(hole) | set(board)
    deck = [c for c in FULL_DECK if c not in known]

    board_needed = 5 - len(board)
    cards_to_draw = 2 * n_opponents + board_needed
    if cards_to_draw > len(deck):
        return 0.5  # shouldn't happen; defensive

    treys_hole = [to_treys(c) for c in hole]
    treys_board = [to_treys(c) for c in board]

    wins = ties = 0
    sample = random.sample

    for _ in range(n_sims):
        draws = sample(deck, cards_to_draw)

        idx = 0
        opp_hands = []
        for _ in range(n_opponents):
            opp_hands.append((to_treys(draws[idx]), to_treys(draws[idx + 1])))
            idx += 2
        full_board = treys_board + [to_treys(c) for c in draws[idx:]]

        my_score = _evaluator.evaluate(full_board, treys_hole)

        # Only compute opponent scores; skip if already lost
        beaten = False
        tied = False
        for oh in opp_hands:
            s = _evaluator.evaluate(full_board, list(oh))
            if s < my_score:            # treys: lower is better
                beaten = True
                break
            if s == my_score:
                tied = True
        if beaten:
            continue
        if tied:
            ties += 1
        else:
            wins += 1

    return (wins + 0.5 * ties) / n_sims