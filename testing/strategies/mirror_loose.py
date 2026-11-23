from testing.strategies.mirror import make_strategy

choose_action = make_strategy(open_eq=0.60, raise_eq=0.55, fold_margin=-0.10)