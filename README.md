# Polymarket Withdrawal Floor Calculator (CLI)

Answers the question every profitable trader eventually asks: **"How much
can I actually withdraw right now?"**

Polymarket's withdrawal mechanics hold back capital in three places:
live positions locked until resolution, the 10% withdrawal floor, and
redeemed-but-claimable wins nobody clicked yet. This tool reads your public
positions and computes the realistic floor in one call.

**Read-only. No wallet connection, no keys** — positions are public data.

## Usage

```bash
git clone https://github.com/tradingbotsbuilder/withdrawal-floor.git
cd withdrawal-floor
python3 withdrawal_floor.py --address 0xYourWallet
```

## Sample output

```
Address            : 0xabc...
Open positions     : 4 (value $1,240.50) — locked until resolution
Redeemable wins    : 2 (value $310.00)
10% floor          : $155.05
Withdrawable now   : $154.95
```

## How to read it

- **Locked** capital isn't lost — winning legs redeem at $1.00/share at
  resolution; losing legs redeem at $0.00.
- **The 10% floor** scales with total portfolio value — it shrinks as
  positions resolve. Don't plan cash-out dates around your full balance.
- **Claimable wins** are the easiest money left on the table: redeem before
  you calculate anything else.

Full write-ups from the same author:
- [Withdrawable amount calculator: the full subtraction chain](https://brainresearchhub.net/research/withdrawal/withdrawable-amount-calculator)

- [Polymarket withdrawals guide](https://brainresearchhub.net/research/withdrawal/polymarket-withdrawals-guide)
- [pUSD-era withdrawals](https://brainresearchhub.net/research/withdrawal/pusd-era-withdrawals)
- [pUSD deposits](https://brainresearchhub.net/research/withdrawal/polymarket-pusd-deposits)
- [Taxes: reporting with no 1099](https://brainresearchhub.net/research/sdk/polymarket-taxes-no-1099) — what withdrawal records you'll need at filing time

Live web version (same math, interactive):
**[polymarket-perps-calculator (HuggingFace Space)](https://ahmedtrading90-polymarket-perps-calculator.static.hf.space/index.html)**

## License

MIT.

*Educational tool. Rules drift — verify current platform terms before
planning withdrawals.*
