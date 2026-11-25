import random

def choose_action(st, equity):
    random_list = []

    if st.me_bet == st.current_bet:
        random_list.append(("check", 0))
    else:
        random_list.append(("call", 0))
        random_list.append(("fold", 0))

    if st.can_raise:
        low = st.current_bet + st.minimum_raise
        high = st.me_bet + st.me_stack
        if high < low:
            amount = high
        else:
            amount = random.randint(low, high)
        random_list.append(("raise", amount))

    return random.choice(random_list)