from bot.decision import legal_raise_target

# card ints are 0..51: rank = c // 4 (0 = 2, ..., 12 = A), suit = c % 4
NINE, JACK, QUEEN, KING, ACE = 7, 9, 10, 11, 12

def is_premium(hole):
    r1, r2 = sorted((hole[0] // 4, hole[1] // 4), reverse=True)
    suited = hole[0] % 4 == hole[1] % 4

    # 99+
    if r1 == r2 and r1 >= NINE:
        return True
    # AK, AQ
    if r1 == ACE and r2 >= QUEEN:
        return True
    # AJs
    if suited and r1 == ACE and r2 == JACK:
        return True
    # KQs
    if suited and r1 == KING and r2 == QUEEN:
        return True
    return False


def choose_action(st, equity):
    free = st.me_bet == st.current_bet

    if st.phase == "PREFLOP":
        strong = is_premium(st.hole)
        desired = st.current_bet * 3
    else:
        strong = equity > 0.65
        desired = st.current_bet + int(0.75 * st.pot)

    if strong:
        if st.can_raise:
            target = legal_raise_target(st, desired)
            if target > st.current_bet:
                return ("raise", target)
        return ("check", 0) if free else ("call", 0)

    return ("check", 0) if free else ("fold", 0)