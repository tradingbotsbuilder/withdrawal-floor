#!/usr/bin/env python3
"""Polymarket Withdrawal Floor Calculator — Ahmed Trading.

Computes the realistic withdrawable balance ("floor") for a Polymarket
position: locked capital in open positions, unresolved markets, the 10%
withdrawal floor rule, and estimated network costs. Read-only public Data
API — the same math as the author's live HuggingFace Space, packaged for
CLI/local use.

Usage:
  python withdrawal_floor.py --address 0xYourAddress

Educational tool. Not financial advice.
"""

import argparse
import json
import sys
import urllib.request

DATA_API = "https://data-api.polymarket.com"
FLOOR_FRACTION = 0.10  # 10% of balance held back at withdrawal time


def http_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "withdrawal-floor/1.0"})
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.loads(r.read().decode())


def fetch_positions(address: str):
    url = f"{DATA_API}/positions?user={address}"
    try:
        return http_json(url)
    except Exception as e:
        sys.exit(f"[!] data-api error: {e}")


def main():
    ap = argparse.ArgumentParser(description="Polymarket withdrawal floor calculator")
    ap.add_argument("--address", required=True, help="wallet address (0x...)")
    args = ap.parse_args()

    positions = fetch_positions(args.address)
    if not positions:
        print("\n[i] No open positions found for this address.")
        print("    Withdrawable = full balance minus the 10% floor.")
        sys.exit(0)

    total_value = 0.0
    locked_open = 0.0   # capital in live, unresolved positions
    pending = 0.0       # value in resolved-but-unredeemed (claimable)
    n_open = n_pending = 0

    for pos in positions:
        size = float(pos.get("size", 0) or 0)
        cur = float(pos.get("curPrice", pos.get("avgPrice", 0)) or 0)
        value = size * cur
        total_value += value
        redeemable = bool(pos.get("redeemable", False))
        if redeemable:
            pending += value
            n_pending += 1
        else:
            locked_open += value
            n_open += 1

    floor = total_value * FLOOR_FRACTION
    withdrawable_now = pending - floor if pending > floor else 0.0

    print(f"\nAddress            : {args.address}")
    print(f"Open positions     : {n_open} (value ${locked_open:,.2f}) — locked until resolution")
    print(f"Redeemable wins    : {n_pending} (value ${pending:,.2f})")
    print(f"10% floor          : ${floor:,.2f}")
    print(f"Withdrawable now   : ${withdrawable_now:,.2f}")
    print("\nNotes:")
    print("  • 'Locked' capital returns at market resolution — winning legs")
    print("    pay $1.00/share, losing legs pay $0.00.")
    print("  • The 10% floor is held back at withdrawal time and settles after")
    print("    open positions resolve (per current platform rules).")
    print("\n  Full guide: https://brainresearchhub.net/research/withdrawal/polymarket-withdrawals-guide")
    print("  pUSD-era specifics: https://brainresearchhub.net/research/withdrawal/pusd-era-withdrawals")
    print("  More research: https://brainresearchhub.net\n")


if __name__ == "__main__":
    main()
