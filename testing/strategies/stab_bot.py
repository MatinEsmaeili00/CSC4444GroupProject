from bot.decision import legal_raise_target

def choose_action(st, equity):
    if st.me_bet == st.current_bet:
        if st.can_raise:
            target = legal_raise_target(st, st.current_bet + st.pot // 2)
            if target > st.current_bet:
                return ("raise", target)
        return ("check", 0)
    return ("fold", 0)