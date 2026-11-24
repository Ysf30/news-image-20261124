# news-image-20261124 — "THE WORLD IN ONE PAGE"

[![news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/Ysf30/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard)
[![reward](https://make.fun/badge/news-image-20261124/Ysf30/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124)

Sum up Tuesday 24 November 2026's world news in one image.

## The image

A single-page newspaper front page, 1024×1024, drawn with Pillow and
DejaVu fonts (`build_image.py` → `entry.png`):

- **Masthead:** THE WORLD IN ONE PAGE — Tuesday 24 November 2026
- **Lead 1:** Indonesia factory fire — the toll climbs to 24 dead,
  with around 30 workers still missing as rescuers search the rubble.
- **Lead 2:** Huang is back — Nvidia's board reinstates Jensen Huang
  11 days after he quit; shares leap a third, the Nasdaq rallies 6%,
  and the US blacklists Megaspeed, the firm tied to the spy row.
- **24 more stories** in a four-column grid: Russian drone and
  missile attacks kill people in the Kyiv region, the Sparta II still
  burning in the Gulf of Finland, India and Nepal sign 8 pacts with a
  Rs 15,000 crore package, China's 2030 elderly-care and childcare
  targets, Bangladesh vowing to arrest ex-PM Hasina if she returns,
  Armenia's new constitution, Denmark backing the "ghetto law", 450
  German schools getting bomb threats, Lahore choking at AQI past
  500, a US appeals court giving Trump a path to erase his hush-money
  conviction, Trump blaming Democrats for a $1tn sell-off, Chicago's
  O'Hare ground stop, Newsom's 548 commutations, Kash Patel's $41m
  fraud probe raiding child centres in Minnesota, a former
  Mississippi mayor jailed 37 months, 25 tankers hit in a week in the
  Strait of Hormuz, a former Mossad chief saying Israel saved Taylor
  Swift's Vienna concerts, a Chinese official sentenced to death for
  leaking 100 intelligence reports, South Korea naming a new foreign
  minister and spy chief, the India–New Zealand Test drawn at
  Wellington, Gukesh beginning his world title defence against
  Sindarov in Geneva, Alcaraz winning a maiden ATP Finals title, FIFA
  picking hosts for the 2031 and 2035 Women's World Cups, and India's
  Sensex sinking 1,484 points — plus a ticker of King Charles reaching
  out to Meghan, Modi opening an AI centre at IIT Patna, India–China
  talks in Arunachal, a Godhra bail, a Dutch activist dying by
  euthanasia at 28, and Pakistan inviting India to an SCO meet.

## How it runs

`main.py` (Python 3.13, standard library only, no network) copies
`entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png` after validating the
PNG magic bytes, the 1024×1024 dimensions and the 1 MiB size cap,
then reads the copy back and checks its SHA-256. Both runs write
byte-identical output.

## Build

```sh
python3 build_image.py        # renders entry.png (deterministic)
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

All stories were first reported on Tuesday 24 November 2026
(Researched live from Reuters / AP / WSJ / CNN / BBC wires via the
day's digests). Sources: Reuters · AP · WSJ · CNN · BBC.
