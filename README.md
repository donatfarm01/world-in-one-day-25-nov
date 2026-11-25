# world-in-one-day-25-nov

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/donatfarm01/world-in-one-day-25-nov/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/donatfarm01/world-in-one-day-25-nov/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

The World in One Day — 25 November 2026. A dense one-page newspaper front
page that sums up the day's world news in a single image: 35 stories, all
of them dated 25 November 2026, with a source beside every story, a
six-number strip, a world map with numbered pins, and a DATE CHECK box
naming the older stories that were deliberately left out.

The program is Python 3.13, standard library only. It draws the whole
front page from scratch — a hand-written 5x7 bitmap font, a small
rasteriser, and a pure-Python PNG encoder — so the same bytes come out
of every run, with no network and no files read at run time.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

The image is written to `out/entry.png` (1024x1024, under 1 MiB).
