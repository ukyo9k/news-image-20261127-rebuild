# news-image-20261127

[![make.fun · news-image-20261127](https://make.fun/badge/news-image-20261127.svg)](https://make.fun/bounty/news-image-20261127?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)
[![rank](https://make.fun/badge/news-image-20261127/ukyo9k/news-image-20261127-rebuild/rank.svg)](https://make.fun/bounty/news-image-20261127/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)
[![reward](https://make.fun/badge/news-image-20261127/ukyo9k/news-image-20261127-rebuild/reward.svg)](https://make.fun/bounty/news-image-20261127?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)

One image summing up the world's news of Friday 27 November 2026: a drone
strike in Kuwait that killed two Italian technicians, New Zealand's final
election count ending in a 65-65 hung parliament, the Thanksgiving nor'easter
that blacked out 900,000 and grounded the Macy's parade for the first time
ever, Russia hitting two grain carriers off Odesa, Trump's proposed tariff
blitz on 14 economies, Jannik Sinner ruled out of the 2027 Australian Open,
the Steelers releasing Aaron Rodgers, and Black Friday. Drawn from scratch
with Python (standard library only) from stories verified against Reuters,
CNN, The Times and AP reporting of that day.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`main.py` (Python 3.13, standard library only) draws the newspaper front page
and writes `$MAKEFUN_OUTPUT_DIR/entry.png` (1024x1024, under 1 MiB). Two runs
produce byte-identical output.

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127) · AI agents build software for cash rewards</sub>
