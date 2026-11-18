"""Card encoding: server JSON <-> int 0..51 <-> treys."""

from treys import Card

SUIT_IDX = {"hearts": 0, "diamonds": 1, "clubs": 2, "spades": 3}
SUIT_CHR = "shdc"                # index -> char, matches SUIT_IDX ordering
RANK_CHR = "23456789TJQKA"       # (int - 2) -> char

FULL_DECK = list(range(52))


def to_int(card):
    """Server card dict -> int 0..51, or None if hidden/empty."""
    if not card or card.get("rank") == "?":
        return None
    r = card["rank"] - 2                         # 2..14 -> 0..12
    s = SUIT_IDX[card["suit"]]
    return r * 4 + s


def to_treys(c):
    """int 0..51 -> treys Card."""
    return Card.new(RANK_CHR[c // 4] + SUIT_CHR[c % 4])


def parse_hole(player):
    """Player dict -> list of ints, or None if hand not dealt / hidden."""
    cards = player.get("hole_cards") or []
    out = [to_int(c) for c in cards if c and c.get("rank") != "?"]
    if len(out) < 2:
        return None
    return out


def parse_board(state):
    """State dict -> list of revealed community cards as ints."""
    cards = state.get("community_cards") or []
    return [to_int(c) for c in cards if c and c.get("rank") != "?"]