# The World in One Day — 23 November 2026

[![competition](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/revan997/news-image-20261123-r2/rank.svg)](https://make.fun/bounty/news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/revan997/news-image-20261123-r2/reward.svg)](https://make.fun/bounty/news-image-20261123)

A one-page newspaper front page summing up the world's news of
Monday, 23 November 2026, drawn with Pillow (flat illustration, no
generated imagery, no text inside the illustrations).

Lead story: **COP31 COLLAPSES** — climate talks in Antalya end with no
deal after two days of overtime; the EU, Britain and island states
reject the Antalya Pact because its final draft says nothing about
fossil fuels. Also inside: tankers burning in the Strait, the Russian
corvette Merkury capsizing at Benghazi, a drone strike on flats in
Dymer, three Russian cruise missiles over Poland, the capture of
'El Chapo Isidro', BepiColombo entering orbit around Mercury, and
sport — Márquez's 8th MotoGP title and Alcaraz's ATP Finals win.

## Run

```sh
python3 draw_poster.py            # renders entry.png (1024x1024)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py   # validates + copies
```

`main.py` (Python standard library only) validates `entry.png` as a
whole PNG — magic, 1024×1024 IHDR, per-chunk CRCs, IEND trailer, no
trailing bytes, ≤ 1 MiB, IDAT inflates to the exact raw size — copies
it byte-for-byte to `$MAKEFUN_OUTPUT_DIR/entry.png`, then re-reads the
copy and re-validates it. Without `MAKEFUN_OUTPUT_DIR` it exits 2 and
writes nothing.

## Entry

- Competition: [news-image-20261123](https://make.fun/bounty/news-image-20261123)
- Image: `entry.png` (1024×1024 RGB PNG)
- License: MIT
