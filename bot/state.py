"""Parse raw server JSON into a plain object with typed fields."""

from dataclasses import dataclass, field
from .cards import parse_hole, parse_board


@dataclass
class ParsedState:
    player_id: str
    phase: str
    hand_number: int
    current_turn: str | None
    pot: int
    current_bet: int
    minimum_raise: int
    community: list[int]                 # revealed board cards as ints
    hole: list[int] | None               # your own cards
    me_bet: int
    me_stack: int
    me_folded: bool
    me_all_in: bool
    opp_count: int                       # players still in hand (not folded)
    can_raise: bool
    players_raw: list[dict] = field(default_factory=list)


def parse_state(raw_payload, player_id):
    me = next((p for p in raw_payload["players"] if p["id"] == player_id), None)
    if me is None:
        return None

    opps_live = [p for p in raw_payload["players"]
                 if p["id"] != player_id and not p["folded"]]
    opps_non_allin = [p for p in opps_live if not p["all_in"]]

    can_raise = (
        me["stack"] > 0
        and not me["all_in"]
        and len(opps_non_allin) >= 1     # can't raise vs. only-all-in opponents
    )

    return ParsedState(
        player_id=player_id,
        phase=raw_payload["phase"],
        hand_number=raw_payload["hand_number"],
        current_turn=raw_payload.get("current_turn"),
        pot=raw_payload["pot"],
        current_bet=raw_payload["current_bet"],
        minimum_raise=raw_payload["minimum_raise"],
        community=parse_board(raw_payload),
        hole=parse_hole(me),
        me_bet=me["bet"],
        me_stack=me["stack"],
        me_folded=me["folded"],
        me_all_in=me["all_in"],
        opp_count=len(opps_live),
        can_raise=can_raise,
        players_raw=raw_payload["players"],
    )