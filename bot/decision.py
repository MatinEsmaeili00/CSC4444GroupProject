"""Turn a ParsedState + equity into a legal (action, amount) pair."""

N_SIMS_BY_PHASE = {
    "PREFLOP": 3000,
    "FLOP":    3000,
    "TURN":    2000,
    "RIVER":   2000,
}


def legal_raise_target(st, desired_total):
    """Clamp a desired total street bet to a legal raise target."""
    lo = st.current_bet + st.minimum_raise
    hi = st.me_bet + st.me_stack
    if hi < lo:                       # only legal "raise" is a short all-in
        return hi
    return max(lo, min(desired_total, hi))


def choose_action(st, equity):
    """
    Returns (action: str, amount: int).
    action in {"check","call","fold","raise"}.
    For raise, amount is the TOTAL street bet target.
    """
    to_call = max(st.current_bet - st.me_bet, 0)

    # No bet to face -> check or open-raise
    if to_call == 0:
        if st.can_raise and equity > 0.70:
            pot_after = st.pot + int(0.5 * st.pot)
            target = legal_raise_target(st, st.current_bet + pot_after // 2)
            if target > st.current_bet:
                return ("raise", target)
        return ("check", 0)

    # Facing a bet
    required = to_call / (st.pot + to_call)
    margin = equity - required

    if margin < -0.05:
        return ("fold", 0)

    if margin < 0.05:
        return ("call", 0)

    if st.can_raise and equity > 0.60:
        pot_after_call = st.pot + to_call
        target = legal_raise_target(
            st, st.current_bet + int(0.66 * pot_after_call)
        )
        if target > st.current_bet:
            return ("raise", target)

    return ("call", 0)


def fallback_action(st):
    """Used if equity computation fails / times out."""
    if st.me_bet == st.current_bet:
        return ("check", 0)
    return ("fold", 0)