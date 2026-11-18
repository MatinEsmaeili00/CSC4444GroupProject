import argparse
import asyncio

from bot.client import run_bot


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("player_id")
    ap.add_argument("url", nargs="?", default="ws://localhost:8000/ws")
    args = ap.parse_args()
    asyncio.run(run_bot(args.player_id, args.url))


if __name__ == "__main__":
    main()