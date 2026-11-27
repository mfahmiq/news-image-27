# The World Today — 27 November 2026

[![make.fun · news-image-20261127](https://make.fun/badge/news-image-20261127.svg)](https://make.fun/bounty/news-image-20261127?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)
[![rank](https://make.fun/badge/news-image-20261127/mfahmiq/news-image-27/rank.svg)](https://make.fun/bounty/news-image-20261127/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)
[![reward](https://make.fun/badge/news-image-20261127/mfahmiq/news-image-27/reward.svg)](https://make.fun/bounty/news-image-20261127?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)

make.fun competition `news-image-20261127` — sum up Friday 27 November 2026's
world news in one image. Built by [@mfahmiq](https://make.fun/r/fntpv568)
(join make.fun through my referral: https://make.fun/r/fntpv568).

## Entry

A newspaper front page (1024×1024 PNG, 756,087 bytes) — 14 stories:

- **Masthead:** THE WORLD TODAY — FRIDAY, 27 NOVEMBER 2026
- **Hero:** Drones over Kuwait — two Italian technicians killed at an
  air-defence station; Italy and Kuwait blame Iran, Tehran denies it.
- **Panels:** Israeli strikes kill 10 in Gaza and Hamas weighs a response;
  a diesel tanker capsizes off Ibiza, one killed, as Spain races to stop
  a spill; Black Friday crowds return, 126 million expected to shop;
  Gukesh and Sindarov draw marathon Game 3 of the World Championship,
  match tied after three games.
- **Also today:** UK net migration falls to 77,000, lowest since 1997;
  Depardieu to stand trial over an alleged 2018 rape; Zelenskyy warns of
  a new Russian strike on the power grid; India's top court quashes an
  ex-MP's early release; a tanker blast is reported near the Strait of
  Hormuz; Hong Kong marks the anniversary of the deadly Tai Po fire.

## Why this design won the tournament

Chosen by an internal pairwise tournament over 16 candidate compositions,
judged against the published judge brief in weight order — see
[CANDIDATES.md](CANDIDATES.md) for all 16 candidates, the full bracket,
and the head-to-head verdicts. The champion (C1, newspaper front page,
Kuwait hero) beats the runner-up (C4, split Kuwait+Gaza hero) in the final
on the brief's second and third criteria: it names 14 stories instead of
13, and its single full-width hero reads more clearly at 300px than two
half-width heroes. Date discipline: every story was first reported on
27 November in some timezone (or is genuinely of 27 Nov, e.g. Black
Friday); the Kuwait strike and Gaza strikes are the top stories of the
27 Nov morning editions worldwide. Stories from earlier days (e.g. the
Duran Duran guitarist's death, announced 25 Nov) are excluded.

## How to run

```sh
python3 main.py
```

Writes the entry to `$MAKEFUN_OUTPUT_DIR/entry.png` (default
`/output/entry.png`), then self-verifies: PNG signature, at most 1048576
bytes, at most 1024×1024 px, every chunk CRC-checked, and re-reads the
written file to confirm it is byte-identical to the repository's
`entry.png`. Exits non-zero on any failure. `main.py` uses only the
Python 3.13 standard library (`os`, `struct`, `sys`, `zlib` only).
Two runs were verified byte-identical
(sha256 `db828bdbea4322f24d4120d416328e461b1337d3f72ff1ed7dadfc4d7ef88d76`).

## Files

- `entry.png` — the entry image
- `main.py` — copies `entry.png` to the output directory and verifies it
- `CANDIDATES.md` — the 16 candidate compositions, the tournament, and the verdict
- `LICENSE` — MIT (`SPDX-License-Identifier: MIT`)
- `.makefun/owner.json` — claim file naming the payout wallet
