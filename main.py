#!/usr/bin/env python3
"""News poster for Friday 27 November 2026.

Draws a newspaper front page summing up the day's world news with pure
Python 3.13 stdlib (zlib + struct for PNG encoding, a hand-built 5x7
bitmap font for text). Writes /output/entry.png (or $MAKEFUN_OUTPUT_DIR).
Deterministic: identical bytes on every run.
"""
import os
import struct
import zlib

W, H = 1024, 1024

# ---------------------------------------------------------------- font --
# 5x7 bitmap glyphs: each row is a 5-bit integer, MSB = leftmost pixel.
FONT = {
    "A": (0x0E, 0x11, 0x11, 0x1F, 0x11, 0x11, 0x11),
    "B": (0x1E, 0x11, 0x11, 0x1E, 0x11, 0x11, 0x1E),
    "C": (0x0E, 0x11, 0x10, 0x10, 0x10, 0x11, 0x0E),
    "D": (0x1E, 0x11, 0x11, 0x11, 0x11, 0x11, 0x1E),
    "E": (0x1F, 0x10, 0x10, 0x1E, 0x10, 0x10, 0x1F),
    "F": (0x1F, 0x10, 0x10, 0x1E, 0x10, 0x10, 0x10),
    "G": (0x0E, 0x11, 0x10, 0x17, 0x11, 0x11, 0x0F),
    "H": (0x11, 0x11, 0x11, 0x1F, 0x11, 0x11, 0x11),
    "I": (0x0E, 0x04, 0x04, 0x04, 0x04, 0x04, 0x0E),
    "J": (0x07, 0x02, 0x02, 0x02, 0x02, 0x12, 0x0C),
    "K": (0x11, 0x12, 0x14, 0x18, 0x14, 0x12, 0x11),
    "L": (0x10, 0x10, 0x10, 0x10, 0x10, 0x10, 0x1F),
    "M": (0x11, 0x1B, 0x15, 0x15, 0x11, 0x11, 0x11),
    "N": (0x11, 0x19, 0x15, 0x13, 0x11, 0x11, 0x11),
    "O": (0x0E, 0x11, 0x11, 0x11, 0x11, 0x11, 0x0E),
    "P": (0x1E, 0x11, 0x11, 0x1E, 0x10, 0x10, 0x10),
    "Q": (0x0E, 0x11, 0x11, 0x11, 0x15, 0x12, 0x0D),
    "R": (0x1E, 0x11, 0x11, 0x1E, 0x14, 0x12, 0x11),
    "S": (0x0F, 0x10, 0x10, 0x0E, 0x01, 0x01, 0x1E),
    "T": (0x1F, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04),
    "U": (0x11, 0x11, 0x11, 0x11, 0x11, 0x11, 0x0E),
    "V": (0x11, 0x11, 0x11, 0x11, 0x11, 0x0A, 0x04),
    "W": (0x11, 0x11, 0x11, 0x15, 0x15, 0x1B, 0x11),
    "X": (0x11, 0x11, 0x0A, 0x04, 0x0A, 0x11, 0x11),
    "Y": (0x11, 0x11, 0x0A, 0x04, 0x04, 0x04, 0x04),
    "Z": (0x1F, 0x01, 0x02, 0x04, 0x08, 0x10, 0x1F),
    "0": (0x0E, 0x11, 0x13, 0x15, 0x19, 0x11, 0x0E),
    "1": (0x04, 0x0C, 0x04, 0x04, 0x04, 0x04, 0x0E),
    "2": (0x0E, 0x11, 0x01, 0x06, 0x08, 0x10, 0x1F),
    "3": (0x1F, 0x02, 0x04, 0x02, 0x01, 0x11, 0x0E),
    "4": (0x02, 0x06, 0x0A, 0x12, 0x1F, 0x02, 0x02),
    "5": (0x1F, 0x10, 0x1E, 0x01, 0x01, 0x11, 0x0E),
    "6": (0x06, 0x08, 0x10, 0x1E, 0x11, 0x11, 0x0E),
    "7": (0x1F, 0x01, 0x02, 0x04, 0x08, 0x08, 0x08),
    "8": (0x0E, 0x11, 0x11, 0x0E, 0x11, 0x11, 0x0E),
    "9": (0x0E, 0x11, 0x11, 0x0F, 0x01, 0x02, 0x0C),
    " ": (0, 0, 0, 0, 0, 0, 0),
    ".": (0, 0, 0, 0, 0, 0x0C, 0x0C),
    ",": (0, 0, 0, 0, 0x0C, 0x04, 0x08),
    "'": (0x04, 0x04, 0x08, 0, 0, 0, 0),
    "-": (0, 0, 0, 0x0E, 0, 0, 0),
    ":": (0, 0x0C, 0x0C, 0, 0x0C, 0x0C, 0),
    ";": (0, 0x0C, 0x0C, 0, 0x0C, 0x04, 0x08),
    "!": (0x04, 0x04, 0x04, 0x04, 0x04, 0, 0x04),
    "?": (0x0E, 0x11, 0x01, 0x02, 0x04, 0, 0x04),
    "(": (0x02, 0x04, 0x08, 0x08, 0x08, 0x04, 0x02),
    ")": (0x08, 0x04, 0x02, 0x02, 0x02, 0x04, 0x08),
    "/": (0x01, 0x01, 0x02, 0x04, 0x08, 0x10, 0x10),
    "&": (0x0C, 0x12, 0x14, 0x08, 0x15, 0x12, 0x0D),
    "+": (0, 0x04, 0x04, 0x0E, 0x04, 0x04, 0),
    "%": (0x18, 0x19, 0x02, 0x04, 0x08, 0x13, 0x03),
    "=": (0, 0, 0x1F, 0, 0x1F, 0, 0),
    "*": (0, 0x04, 0x15, 0x0E, 0x15, 0x04, 0),
    "<": (0x02, 0x04, 0x08, 0x10, 0x08, 0x04, 0x02),
    ">": (0x08, 0x04, 0x02, 0x01, 0x02, 0x04, 0x08),
}


def char_w(scale):
    return 6 * scale


def text_w(s, scale):
    return len(s) * char_w(scale) - scale


# ------------------------------------------------------------- canvas --
class Canvas:
    def __init__(self, w, h, bg):
        self.w, self.h = w, h
        self.px = bytearray(bg * (w * h))

    def set(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i:i + 3] = c

    def rect(self, x0, y0, x1, y1, c):
        for y in range(max(0, y0), min(self.h, y1)):
            for x in range(max(0, x0), min(self.w, x1)):
                self.set(x, y, c)

    def hline(self, x0, x1, y, c, t=1):
        for yy in range(y, y + t):
            for x in range(x0, x1):
                self.set(x, yy, c)

    def vline(self, x, y0, y1, c, t=1):
        for xx in range(x, x + t):
            for y in range(y0, y1):
                self.set(xx, y, c)

    def circle(self, cx, cy, r, c, fill=True):
        for y in range(cy - r, cy + r + 1):
            for x in range(cx - r, cx + r + 1):
                d = (x - cx) ** 2 + (y - cy) ** 2
                if fill and d <= r * r:
                    self.set(x, y, c)
                elif not fill and abs(d - r * r) <= r:
                    self.set(x, y, c)

    def disc(self, cx, cy, r, c):
        self.circle(cx, cy, r, c, fill=True)

    def line(self, x0, y0, x1, y1, c, t=1):
        dx, dy = abs(x1 - x0), abs(y1 - y0)
        n = max(dx, dy, 1)
        for i in range(n + 1):
            x = x0 + (x1 - x0) * i // n
            y = y0 + (y1 - y0) * i // n
            for a in range(t):
                self.set(x + a, y, c)

    def text(self, x, y, s, scale, c):
        s = s.upper()
        cx = x
        for ch in s:
            g = FONT.get(ch, FONT[" "])
            for r in range(7):
                row = g[r]
                for col in range(5):
                    if row & (0x10 >> col):
                        for dy in range(scale):
                            for dx in range(scale):
                                self.set(cx + col * scale + dx,
                                         y + r * scale + dy, c)
            cx += char_w(scale)
        return cx

    def text_center(self, cx, y, s, scale, c):
        self.text(cx - text_w(s, scale) // 2, y, s, scale, c)

    def wrap(self, s, max_w, scale):
        words, lines, cur = s.split(), [], ""
        for wd in words:
            trial = (cur + " " + wd).strip()
            if text_w(trial, scale) <= max_w or not cur:
                cur = trial
            else:
                lines.append(cur)
                cur = wd
        if cur:
            lines.append(cur)
        return lines


# ------------------------------------------------------------- colors --
PAPER = bytes((247, 242, 231))
INK = bytes((18, 18, 18))
RED = bytes((178, 34, 28))
NAVY = bytes((24, 48, 92))
GOLD = bytes((196, 148, 44))
GREY = bytes((105, 105, 100))
LIGHT = bytes((232, 226, 210))
SKY = bytes((58, 90, 128))
DARK = bytes((30, 34, 44))
ORANGE = bytes((214, 110, 30))
GREEN = bytes((46, 125, 70))
WHITE = bytes((255, 255, 255))

# ------------------------------------------------------------- drawing --


def panel(cv, x0, y0, x1, y1, border=INK):
    cv.rect(x0, y0, x1, y1, PAPER)
    cv.hline(x0, x1, y0, border, 3)
    cv.hline(x0, x1, y1 - 3, border, 3)
    cv.vline(x0, y0, y1, border, 3)
    cv.vline(x1 - 3, y0, y1, border, 3)


def kicker(cv, x, y, s, c=RED):
    cv.text(x, y, s, 2, c)


def headline(cv, x, y, lines, scale=3, c=INK, gap=None):
    gap = gap if gap is not None else 7 * scale + 6
    for ln in lines:
        cv.text(x, y, ln, scale, c)
        y += gap
    return y


def draw_masthead(cv):
    cv.hline(24, 1000, 26, INK, 4)
    cv.text_center(512, 44, "THE WORLD IN ONE PAGE", 2, GREY)
    cv.text_center(512, 66, "FRIDAY 27 NOVEMBER 2026", 5, INK)
    cv.hline(24, 1000, 118, INK, 2)
    cv.text_center(512, 128, "ONE DAY  -  ONE PICTURE  -  THE NEWS THAT MATTERED",
                   2, RED)


def draw_lead(cv):
    # Lead story panel: x 24..1000, y 152..396
    panel(cv, 24, 152, 1000, 396)
    kicker(cv, 44, 166, "GULF IN CRISIS  -  LEAD STORY")
    y = headline(cv, 44, 182, ["DRONE STRIKE IN", "KUWAIT KILLS TWO"], 4)
    cv.text(44, 250, "ITALIANS", 4, RED)
    body = [
        "Two Italian technicians died",
        "when drones blamed on Iran",
        "hit an air-defence station.",
        "Tehran denies any role.",
    ]
    yy = 306
    for ln in body:
        cv.text(44, yy, ln, 2, INK)
        yy += 17
    # illustration: night sky over a radar station
    ix0, iy0, ix1, iy1 = 560, 168, 984, 380
    cv.rect(ix0, iy0, ix1, iy1, DARK)
    # stars
    for sx, sy in [(600, 190), (660, 210), (720, 185), (800, 205), (880, 190),
                   (940, 220), (640, 240), (760, 235), (900, 250), (580, 260)]:
        cv.disc(sx, sy, 2, WHITE)
    # ground + radar tower
    cv.rect(ix0, 330, ix1, iy1, bytes((52, 58, 66)))
    cv.rect(700, 250, 716, 330, GREY)
    cv.disc(708, 244, 16, GOLD)
    cv.line(708, 244, 760, 210, GOLD, 3)
    cv.line(708, 244, 656, 212, GOLD, 3)
    # explosion burst
    for dx, dy, r in [(0, 0, 26), (-22, 10, 14), (24, 12, 15), (-8, -20, 12),
                      (14, -16, 10)]:
        cv.disc(880 + dx, 300 + dy, r, ORANGE)
    cv.disc(880, 300, 12, GOLD)
    # drone silhouettes
    for dx, dy in [(620, 200), (830, 225), (920, 270)]:
        cv.rect(dx - 14, dy - 2, dx + 14, dy + 3, WHITE)
        cv.disc(dx - 16, dy, 4, WHITE)
        cv.disc(dx + 16, dy, 4, WHITE)
    cv.text(ix0 + 12, iy1 - 22, "KUWAIT  -  AIR DEFENCE SITE", 2, WHITE)


def draw_nz(cv):
    # x 24..500, y 408..648
    panel(cv, 24, 408, 500, 648)
    kicker(cv, 44, 424, "NEW ZEALAND  -  ELECTION")
    y = headline(cv, 44, 444, ["HUNG PARLIAMENT:", "65 - 65 DEADLOCK"], 3)
    body = [
        "The final count wipes out the",
        "coalition majority. National",
        "falls to 40 seats; Labour 36.",
        "Opportunity, with 7, holds power.",
    ]
    yy = 512
    for ln in body:
        cv.text(44, yy, ln, 2, INK)
        yy += 17
    # bar chart: two equal bars, 65 seats each (label left, bar right)
    cv.text(44, 594, "RIGHT 65", 2, NAVY)
    cv.rect(210, 592, 410, 608, NAVY)
    cv.text(44, 622, "LEFT+OPP 65", 2, RED)
    cv.rect(210, 620, 410, 636, RED)


def draw_storm(cv):
    # x 524..1000, y 408..648
    panel(cv, 524, 408, 1000, 648)
    kicker(cv, 544, 424, "UNITED STATES  -  WEATHER")
    y = headline(cv, 544, 444, ["THANKSGIVING STORM", "BLACKS OUT 900,000"], 3)
    body = [
        "A nor'easter knocks out power",
        "across the East Coast. The",
        "Macy's parade is postponed",
        "for the first time ever.",
    ]
    yy = 516
    for ln in body:
        cv.text(544, yy, ln, 2, INK)
        yy += 17
    # storm cloud (bottom right) + grounded balloon (bottom left)
    cv.disc(890, 606, 26, SKY)
    cv.disc(858, 616, 20, SKY)
    cv.disc(922, 616, 20, SKY)
    cv.rect(846, 606, 934, 624, SKY)
    for rx in range(852, 934, 16):
        cv.line(rx, 628, rx - 5, 642, SKY, 3)
    cv.disc(580, 612, 20, ORANGE)
    cv.text(612, 596, "PARADE", 2, INK)
    cv.text(612, 614, "GROUNDED", 2, RED)


def draw_odesa(cv):
    # x 24..348, y 660..900
    panel(cv, 24, 660, 348, 900)
    kicker(cv, 40, 676, "UKRAINE  -  BLACK SEA")
    y = headline(cv, 40, 696, ["GRAIN SHIPS", "HIT OFF ODESA"], 3)
    body = [
        "Russia hits two foreign",
        "carriers, 100,000 tonnes",
        "aboard.",
    ]
    yy = 770
    for ln in body:
        cv.text(40, yy, ln, 2, INK)
        yy += 17
    # sea + ship (bottom strip only)
    cv.rect(40, 852, 332, 884, SKY)
    cv.rect(120, 824, 260, 852, DARK)
    cv.rect(168, 808, 182, 824, DARK)
    cv.line(175, 806, 175, 824, DARK, 3)
    cv.disc(292, 838, 9, ORANGE)
    cv.disc(292, 838, 4, GOLD)


def draw_tariffs(cv):
    # x 360..664, y 660..900
    panel(cv, 360, 660, 664, 900)
    kicker(cv, 376, 676, "UNITED STATES  -  TRADE")
    y = headline(cv, 376, 696, ["TRUMP'S TARIFF", "BLITZ"], 3)
    body = [
        "New tariffs proposed on",
        "14 economies for excess",
        "industrial capacity.",
    ]
    yy = 782
    for ln in body:
        cv.text(376, yy, ln, 2, INK)
        yy += 17
    # tariff bars (bottom strip only)
    cv.text(376, 840, "CHINA 20%", 2, RED)
    cv.rect(376, 856, 376 + 130, 870, RED)
    cv.text(376, 878, "INDIA 25%  VIETNAM 35%", 2, INK)


def draw_sport(cv):
    # x 676..1000, y 660..900
    panel(cv, 676, 660, 1000, 900)
    kicker(cv, 692, 676, "SPORT")
    # tennis ball tucked in the kicker row, clear of the headline
    cv.disc(968, 682, 12, GREEN)
    cv.line(960, 674, 976, 690, WHITE, 2)
    y = headline(cv, 692, 696, ["SINNER OUT OF", "AUSTRALIAN OPEN"], 3)
    body = [
        "Jannik Sinner misses the",
        "2027 Grand Slam after",
        "knee surgery.",
        "",
        "Steelers release Aaron",
        "Rodgers after his blast",
        "at coach McCarthy.",
    ]
    yy = 780
    for ln in body:
        cv.text(692, yy, ln, 2, INK)
        yy += 17


def draw_footer(cv):
    cv.hline(24, 1000, 912, INK, 2)
    cv.text_center(512, 928, "BLACK FRIDAY: SHOPPERS OUT AS DISCOUNTS DEEPEN", 2, INK)
    cv.text_center(512, 956,
                   "REPORTED FRIDAY 27 NOVEMBER 2026  -  SOURCES: REUTERS, CNN, THE TIMES, AP",
                   2, GREY)
    cv.hline(24, 1000, 986, INK, 4)


def build():
    cv = Canvas(W, H, PAPER)
    draw_masthead(cv)
    draw_lead(cv)
    draw_nz(cv)
    draw_storm(cv)
    draw_odesa(cv)
    draw_tariffs(cv)
    draw_sport(cv)
    draw_footer(cv)
    return cv


def write_png(cv, path):
    raw = bytearray()
    for y in range(cv.h):
        raw.append(0)
        raw += cv.px[y * cv.w * 3:(y + 1) * cv.w * 3]

    def chunk(typ, data):
        c = struct.pack(">I", len(data)) + typ + data
        return c + struct.pack(">I", zlib.crc32(typ + data) & 0xFFFFFFFF)

    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", cv.w, cv.h, 8, 2, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    png += chunk(b"IEND", b"")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(png)
    return len(png)


def main():
    out = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    path = os.path.join(out, "entry.png")
    cv = build()
    n = write_png(cv, path)
    print(f"wrote {path} {n} bytes {cv.w}x{cv.h}")


if __name__ == "__main__":
    main()
