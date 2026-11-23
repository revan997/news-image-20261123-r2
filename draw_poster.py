#!/usr/bin/env python3
"""Render the news-image-20261123 front page: THE WORLD IN ONE DAY.

Flat PIL illustration, no generated imagery, no text inside the
illustrations. Stories are the verified 23 November 2026 items from the
build brief: COP31 collapse (lead), tankers in the Strait, the Merkury
at Benghazi, Dymer, Poland, El Chapo Isidro, BepiColombo, sport, plus
a footer strip. Output: entry.png, 1024x1024 RGB.
"""

import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 243, 231)
INK = (20, 20, 20)
RED = (178, 34, 34)
NAVY = (31, 58, 95)
TEAL = (18, 105, 105)
GOLD = (176, 124, 24)
GREY = (90, 90, 90)
RULE = (120, 110, 95)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = "DejaVuSerif-Bold.ttf"
SERIF = "DejaVuSerif.ttf"
SANS = "DejaVuSans.ttf"
SANS_B = "DejaVuSans-Bold.ttf"


def wrap(draw, text, fnt, max_w, max_lines):
    """Wrap text to max_w; clamp to max_lines, ellipsis on the last."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        while lines and draw.textlength(lines[-1] + " ...", font=fnt) > max_w:
            lines[-1] = lines[-1].rsplit(" ", 1)[0] if " " in lines[-1] else ""
        lines[-1] = (lines[-1] + " ...").strip()
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def hline(draw, x0, x1, y, fill=INK, width=2):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def globe(draw, cx, cy, r):
    """Cracked globe: blue ocean, green land blobs, dark jagged crack."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(46, 111, 176),
                 outline=(20, 40, 70), width=4)
    land = [
        [(cx - 62, cy - 42), (cx - 18, cy - 58), (cx + 8, cy - 30),
         (cx - 12, cy - 6), (cx - 52, cy - 8)],
        [(cx + 22, cy + 6), (cx + 66, cy - 8), (cx + 72, cy + 30),
         (cx + 38, cy + 52), (cx + 14, cy + 34)],
        [(cx - 58, cy + 34), (cx - 26, cy + 30), (cx - 18, cy + 62),
         (cx - 48, cy + 74), (cx - 66, cy + 56)],
    ]
    for blob in land:
        draw.polygon(blob, fill=(62, 155, 79))
    crack = [(cx - 70, cy - 66), (cx - 38, cy - 34), (cx - 52, cy - 2),
             (cx - 14, cy + 18), (cx - 30, cy + 52), (cx + 6, cy + 78),
             (cx + 34, cy + 58)]
    draw.line(crack, fill=(20, 20, 20), width=6, joint="curve")
    draw.line([(cx - 38, cy - 34), (cx - 6, cy - 44), (cx + 18, cy - 30)],
              fill=(20, 20, 20), width=4, joint="curve")
    draw.line([(cx - 14, cy + 18), (cx + 22, cy + 6), (cx + 48, cy + 16)],
              fill=(20, 20, 20), width=4, joint="curve")
    draw.arc([cx - r - 14, cy - r - 14, cx + r + 14, cy + r + 14],
             start=200, end=340, fill=(176, 124, 24), width=5)


def icon_tanker(draw, x, y, s):
    draw.rectangle([x, y + s * 0.55, x + s, y + s * 0.72], fill=(40, 40, 40))
    draw.rectangle([x + s * 0.62, y + s * 0.30, x + s * 0.82, y + s * 0.55],
                   fill=(120, 30, 30))
    draw.polygon([(x + s * 0.18, y + s * 0.55), (x + s * 0.30, y + s * 0.10),
                  (x + s * 0.42, y + s * 0.55)], fill=(232, 120, 30))
    draw.polygon([(x + s * 0.42, y + s * 0.55), (x + s * 0.54, y + s * 0.18),
                  (x + s * 0.66, y + s * 0.55)], fill=(240, 180, 40))
    draw.line([(x, y + s * 0.82), (x + s, y + s * 0.82)], fill=TEAL, width=3)
    draw.line([(x + s * 0.1, y + s * 0.92), (x + s * 0.9, y + s * 0.92)],
              fill=TEAL, width=3)


def icon_ship_tilt(draw, x, y, s):
    draw.polygon([(x + s * 0.05, y + s * 0.55), (x + s * 0.95, y + s * 0.25),
                  (x + s * 0.95, y + s * 0.48), (x + s * 0.05, y + s * 0.78)],
                 fill=(70, 70, 90))
    draw.rectangle([x + s * 0.45, y + s * 0.05, x + s * 0.60, y + s * 0.30],
                   fill=(90, 90, 90))
    draw.line([(x, y + s * 0.88), (x + s, y + s * 0.88)], fill=TEAL, width=3)


def icon_building(draw, x, y, s):
    draw.rectangle([x + s * 0.15, y + s * 0.10, x + s * 0.85, y + s * 0.90],
                   fill=(150, 120, 90))
    for r in range(3):
        for c in range(3):
            draw.rectangle([x + s * (0.25 + c * 0.22), y + s * (0.20 + r * 0.24),
                            x + s * (0.38 + c * 0.22), y + s * (0.33 + r * 0.24)],
                           fill=(248, 243, 231))
    draw.line([(x + s * 0.5, y + s * 0.10), (x + s * 0.42, y + s * 0.45),
               (x + s * 0.58, y + s * 0.62), (x + s * 0.48, y + s * 0.90)],
              fill=(20, 20, 20), width=3)


def icon_missile(draw, x, y, s):
    draw.line([(x + s * 0.10, y + s * 0.85), (x + s * 0.80, y + s * 0.15)],
              fill=(60, 60, 60), width=7)
    draw.polygon([(x + s * 0.80, y + s * 0.15), (x + s * 0.95, y + s * 0.05),
                  (x + s * 0.88, y + s * 0.32)], fill=RED)
    draw.line([(x + s * 0.10, y + s * 0.85), (x + s * 0.02, y + s * 0.95)],
              fill=(232, 120, 30), width=4)


def icon_cuffs(draw, x, y, s):
    draw.ellipse([x + s * 0.05, y + s * 0.30, x + s * 0.45, y + s * 0.70],
                 outline=NAVY, width=6)
    draw.ellipse([x + s * 0.55, y + s * 0.30, x + s * 0.95, y + s * 0.70],
                 outline=NAVY, width=6)
    draw.line([(x + s * 0.45, y + s * 0.50), (x + s * 0.55, y + s * 0.50)],
              fill=NAVY, width=6)


def icon_planet(draw, x, y, s):
    draw.ellipse([x + s * 0.15, y + s * 0.15, x + s * 0.85, y + s * 0.85],
                 fill=(176, 124, 24))
    draw.ellipse([x + s * 0.30, y + s * 0.30, x + s * 0.45, y + s * 0.45],
                 fill=(120, 84, 16))
    draw.ellipse([x + s * 0.55, y + s * 0.55, x + s * 0.70, y + s * 0.70],
                 fill=(120, 84, 16))
    draw.ellipse([x + s * 0.02, y + s * 0.42, x + s * 0.98, y + s * 0.58],
                 outline=GOLD, width=3)


def icon_flag(draw, x, y, s):
    draw.line([(x + s * 0.10, y), (x + s * 0.10, y + s)], fill=INK, width=4)
    for r in range(3):
        for c in range(4):
            if (r + c) % 2 == 0:
                draw.rectangle([x + s * (0.15 + c * 0.20), y + s * (r * 0.18),
                                x + s * (0.35 + c * 0.20), y + s * ((r + 1) * 0.18)],
                               fill=INK)


def card(draw, x, y, w, h, kicker, kcolor, headline, body, icon):
    draw.rectangle([x, y, x + w, y + h], outline=RULE, width=1)
    draw.rectangle([x, y, x + w, y + 5], fill=kcolor)
    pad = 14
    tx, ty = x + pad, y + 14
    draw.text((tx, ty), kicker, font=font(SANS_B, 15), fill=kcolor)
    ty += 24
    icon(draw, x + w - pad - 46, ty, 46)
    hl = wrap(draw, headline, font(SANS_B, 21), w - 2 * pad - 56, 2)
    ty = draw_lines(draw, hl, tx, ty, font(SANS_B, 21), INK, 25)
    ty += 4
    bl = wrap(draw, body, font(SANS, 16), w - 2 * pad, 3)
    draw_lines(draw, bl, tx, ty, font(SANS, 16), (50, 50, 50), 21)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 36

    # Masthead
    title = "THE WORLD IN ONE DAY"
    tf = font(SERIF_B, 62)
    d.text(((W - d.textlength(title, font=tf)) / 2, 26), title,
           font=tf, fill=INK)
    hline(d, mx, W - mx, 108, width=3)
    hline(d, mx, W - mx, 114, width=1)
    date = "MONDAY, 23 NOVEMBER 2026"
    df = font(SANS_B, 22)
    d.text(((W - d.textlength(date, font=df)) / 2, 124), date,
           font=df, fill=RED)
    sub = "THE DAY'S NEWS FROM EVERY CORNER OF THE EARTH — IN ONE PAGE"
    sf = font(SANS, 15)
    d.text(((W - d.textlength(sub, font=sf)) / 2, 154), sub,
           font=sf, fill=GREY)

    # Lead story: COP31
    ly = 186
    d.text((mx, ly), "CLIMATE  •  ANTALYA", font=font(SANS_B, 19), fill=RED)
    head = "COP31 COLLAPSES"
    hf = font(SERIF_B, 50)
    d.text((mx, ly + 28), head, font=hf, fill=INK)
    deck = ("Climate talks in Antalya end with no deal after two days of "
            "overtime. The EU, Britain and island states reject the "
            "Antalya Pact: its final draft says nothing about fossil "
            "fuels. Saudi Arabia and Russia blocked the language; the "
            "$120bn fund was dropped. Longest COP ever; first collapse "
            "since Copenhagen 2009.")
    dl = wrap(d, deck, font(SERIF, 19), 560, 6)
    draw_lines(d, dl, mx, ly + 102, font(SERIF, 19), (40, 40, 40), 25)

    # Lead illustration: cracked globe in a dusk panel (no text in it)
    gx0, gy0, gx1, gy1 = 624, ly, 988, ly + 236
    d.rectangle([gx0, gy0, gx1, gy1], fill=(39, 75, 115))
    d.ellipse([gx0 + 22, gy0 + 18, gx0 + 78, gy0 + 74], fill=(232, 163, 76))
    globe(d, (gx0 + gx1) // 2, (gy0 + gy1) // 2 + 8, 92)
    d.rectangle([gx0, gy0, gx1, gy1], outline=INK, width=2)

    hline(d, mx, W - mx, 448, width=2)

    # Grid: 6 cards, 3 x 2
    cw, ch, gap = 304, 178, 20
    gy = 462
    cards = [
        (0, 0, "THE STRAIT  •  WAR AT SEA", RED,
         "TANKERS BURN IN THE STRAIT",
         "Three hit near Oman Fri–Sat; two more struck mines Sunday; "
         "a sixth claimed Monday.",
         icon_tanker),
        (1, 0, "LIBYA  •  BENGHAZI", NAVY,
         "WARSHIP CAPSIZES",
         "Ukrainian sea drones hit the corvette Merkury; 10 hurt.",
         icon_ship_tilt),
        (2, 0, "UKRAINE  •  NEAR KYIV", NAVY,
         "FLATS HIT IN DYMER",
         "Russian drone hits a block; 2 dead, 11 missing.",
         icon_building),
        (0, 1, "POLAND  •  NATO TO MEET", RED,
         "FALLEN OBJECTS WERE MISSILES",
         "Three fallen objects were Russian cruise missiles.",
         icon_missile),
        (1, 1, "MEXICO  •  CAPTURED", TEAL,
         "'EL CHAPO ISIDRO' CAPTURED",
         "FBI most-wanted boss captured; 11 dead.",
         icon_cuffs),
        (2, 1, "SPACE  •  MERCURY", GOLD,
         "PROBE ORBITS MERCURY",
         "BepiColombo enters orbit — only the 2nd ever.",
         icon_planet),
    ]
    for col, row, kicker, kcolor, headline, body, icon in cards:
        card(d, mx + col * (cw + gap), gy + row * (ch + 14),
             cw, ch, kicker, kcolor, headline, body, icon)

    # Sport strip
    sy = 852
    d.rectangle([mx, sy, W - mx, sy + 74], outline=RULE, width=1)
    d.rectangle([mx, sy, W - mx, sy + 5], fill=TEAL)
    icon_flag(d, mx + 16, sy + 22, 40)
    d.text((mx + 72, sy + 16), "SPORT", font=font(SANS_B, 15), fill=TEAL)
    d.text((mx + 72, sy + 38), "MÁRQUEZ TAKES AN 8TH MOTOGP TITLE",
           font=font(SANS_B, 23), fill=INK)
    d.text((W - mx - 14 - d.textlength("Alcaraz takes the ATP Finals.",
           font=font(SANS, 18)), sy + 42), "Alcaraz takes the ATP Finals.",
           font=font(SANS, 18), fill=(50, 50, 50))

    # Footer
    fy = 946
    hline(d, mx, W - mx, fy, width=2)
    f1 = ("MARKETS PLUNGE — US stocks down; Taiwan −17.5% in a week   •   "
          "LAHORE AIR: AQI 538")
    f2 = ("SHURI CASTLE REOPENS   •   FIFA TO CONFIRM UK AS 2035 "
          "WOMEN'S WORLD CUP HOST")
    ff = font(SANS_B, 16)
    d.text((mx, fy + 10), f1, font=ff, fill=INK)
    d.text((mx, fy + 34), f2, font=ff, fill=INK)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG")
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
