from bot.decision import legal_raise_target


def make_strategy(open_eq=0.70, raise_eq=0.60, fold_margin=-0.05, call_margin=0.05):
    def choose_action(st, equity):
        to_call = max(st.current_bet - st.me_bet, 0)

        if to_call == 0:
            if st.can_raise and equity > open_eq:
                target = legal_raise_target(st, st.current_bet + int(0.75 * st.pot))
                if target > st.current_bet:
                    return ("raise", target)
            return ("check", 0)

        required = to_call / (st.pot + to_call)
        margin = equity - required

        if margin < fold_margin:
            return ("fold", 0)
        if margin < call_margin:
            return ("call", 0)

        if st.can_raise and equity > raise_eq:
            target = legal_raise_target(
                st, st.current_bet + int(0.66 * (st.pot + to_call))
            )
            if target > st.current_bet:
                return ("raise", target)
        return ("call", 0)

    return choose_action