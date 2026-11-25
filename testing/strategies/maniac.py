def choose_action(st, equity):
    if st.can_raise:
        return ("raise", st.me_bet + st.me_stack)
    elif st.me_bet == st.current_bet:
        return ("check", 0)
    return ("call", 0)