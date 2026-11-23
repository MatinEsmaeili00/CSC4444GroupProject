from testing.strategies.mirror import make_strategy

choose_action = make_strategy(open_eq=0.80, raise_eq=0.70, fold_margin=0.0)