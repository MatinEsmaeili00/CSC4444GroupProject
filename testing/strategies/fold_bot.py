def choose_action(st, equity):
    if st.me_bet == st.current_bet:
        return ("check", 0)
    return ("fold",0)