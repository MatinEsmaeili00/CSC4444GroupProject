"""WebSocket loop. Only file that knows about JSON in/out."""

import asyncio
import json
import time
import websockets

from .equity import monte_carlo_equity
from .state import parse_state
from .decision import N_SIMS_BY_PHASE, choose_action, fallback_action

TIME_BUDGET_S = 10.0   # leaves 5s of the 15s window for network + jitter


async def run_bot(player_id, url, verbose=True):
    async with websockets.connect(url) as ws:
        await ws.send(json.dumps({
            "type": "join",
            "player_id": player_id,
            "name": player_id,
        }))

        pending = False
        last_turn_sig = None

        async for raw in ws:
            msg = json.loads(raw)
            mtype = msg.get("type")

            if mtype == "error":
                print(f"[{player_id}] server error: {msg['message']}", flush=True)
                pending = False
                continue

            if mtype == "action_result":
                pending = False
                if not msg["payload"].get("ok"):
                    print(f"[{player_id}] rejected: "
                          f"{msg['payload'].get('error')}", flush=True)
                continue

            if mtype != "state":
                continue

            st = parse_state(msg["payload"], player_id)
            if st is None:
                continue
            if st.current_turn != player_id:
                pending = False
                continue
            if st.hole is None:
                # undealt hand — shouldn't be our turn, but skip safely
                continue

            # Dedup repeated broadcasts for the same turn
            sig = (st.hand_number, st.phase, st.current_bet, st.me_bet)
            if pending and sig == last_turn_sig:
                continue

            t0 = time.monotonic()
            try:
                n_sims = N_SIMS_BY_PHASE.get(st.phase, 2000)
                equity = monte_carlo_equity(
                    st.hole, st.community, max(st.opp_count, 1), n_sims=n_sims
                )
                if time.monotonic() - t0 > TIME_BUDGET_S:
                    action, amount = fallback_action(st)
                else:
                    action, amount = choose_action(st, equity)
            except Exception as e:
                print(f"[{player_id}] decision error: {e!r}", flush=True)
                action, amount = fallback_action(st)

            if verbose:
                print(f"[{player_id}] H{st.hand_number} {st.phase} "
                      f"eq={equity if 'equity' in dir() else float('nan'):.3f} "
                      f"to_call={max(st.current_bet-st.me_bet,0)} "
                      f"pot={st.pot} opps={st.opp_count} -> {action} {amount}",
                      flush=True)

            out = {"type": "action", "action": action}
            if action == "raise":
                out["amount"] = int(amount)
            await ws.send(json.dumps(out))
            pending = True
            last_turn_sig = sig