#!/usr/bin/env python3
"""The World in One Day - 25 November 2026.
A dense one-page newspaper front page, drawn from scratch with the Python
standard library only (zlib + struct for the PNG encoder, no fonts, no
network, no files read at run time). The program is fully deterministic:
the same bytes come out of every run.

Layout: masthead, six-number strip, one lead story, two big stories,
ten grid stories, a world map with numbered pins, a 22-more-stories list,
a DATE CHECK box listing the stale stories deliberately left out, footer.
35 stories in all, every one dated 25 November 2026.
"""

import os
import struct
import zlib

W, H = 1024, 1024
INK = (0, 0, 0)
PAPER = (255, 255, 255)
GRAY = (205, 205, 205)
LIGHT = (238, 238, 238)
DARK = (105, 105, 105)

# ---------------------------------------------------------------- font
# 5x7 bitmap font, one int per row, bit 4 = leftmost pixel. Written from
# scratch for this page; every letter, digit and mark below is hand-set.
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
    "W": (0x11, 0x11, 0x11, 0x15, 0x15, 0x15, 0x0A),
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
    ":": (0, 0x0C, 0x0C, 0, 0x0C, 0x0C, 0),
    ";": (0, 0x0C, 0x0C, 0, 0x0C, 0x04, 0x08),
    "!": (0x04, 0x04, 0x04, 0x04, 0x04, 0, 0x04),
    "?": (0x0E, 0x11, 0x01, 0x02, 0x04, 0, 0x04),
    "'": (0x04, 0x04, 0x08, 0, 0, 0, 0),
    '"': (0x0A, 0x0A, 0x0A, 0, 0, 0, 0),
    "-": (0, 0, 0, 0x1F, 0, 0, 0),
    "(": (0x02, 0x04, 0x08, 0x08, 0x08, 0x04, 0x02),
    ")": (0x08, 0x04, 0x02, 0x02, 0x02, 0x04, 0x08),
    "/": (0x01, 0x01, 0x02, 0x04, 0x08, 0x10, 0x10),
    "&": (0x0C, 0x12, 0x14, 0x08, 0x15, 0x12, 0x0D),
    "%": (0x19, 0x19, 0x02, 0x04, 0x08, 0x13, 0x13),
    "$": (0x04, 0x0F, 0x14, 0x0E, 0x05, 0x1E, 0x04),
    "#": (0x0A, 0x0A, 0x1F, 0x0A, 0x1F, 0x0A, 0x0A),
    "@": (0x0E, 0x11, 0x17, 0x15, 0x16, 0x10, 0x0E),
    "+": (0, 0x04, 0x04, 0x1F, 0x04, 0x04, 0),
    "=": (0, 0, 0x1F, 0, 0x1F, 0, 0),
    "*": (0, 0x04, 0x15, 0x0E, 0x15, 0x04, 0),
    "_": (0, 0, 0, 0, 0, 0, 0x1F),
    "[": (0x0E, 0x08, 0x08, 0x08, 0x08, 0x08, 0x0E),
    "]": (0x0E, 0x02, 0x02, 0x02, 0x02, 0x02, 0x0E),
    "<": (0x02, 0x04, 0x08, 0x10, 0x08, 0x04, 0x02),
    ">": (0x08, 0x04, 0x02, 0x01, 0x02, 0x04, 0x08),
    "|": (0x04, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04),
    "·": (0, 0, 0x0C, 0x0C, 0, 0, 0),
}

_ACCENTS = str.maketrans({
    "é": "E", "è": "E", "ê": "E", "ë": "E", "á": "A", "à": "A", "â": "A",
    "ä": "A", "ö": "O", "ô": "O", "ó": "O", "ò": "O", "ü": "U", "û": "U",
    "ú": "U", "ù": "U", "ñ": "N", "ç": "C", "í": "I", "ì": "I", "ş": "S",
    "ğ": "G", "ı": "I", "’": "'", "‘": "'", "“": '"', "”": '"',
    "–": "-", "—": "-", "…": ".", "×": "X", "°": "",
})


def normalize(s):
    """Uppercase, fold accents and curly punctuation into the font's set."""
    s = s.translate(_ACCENTS).upper()
    out = []
    for ch in s:
        out.append(ch if ch in FONT else "?")
    return "".join(out)


def text_w(s, scale=1):
    return len(normalize(s)) * 6 * scale


def wrap(s, width, scale=1):
    """Greedy word wrap of normalized text to a pixel width."""
    words = normalize(s).split(" ")
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if text_w(trial, scale) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


# ---------------------------------------------------------------- canvas
class Page:
    def __init__(self):
        self.px = [bytearray(PAPER * W) for _ in range(H)]

    def fill(self, x, y, w, h, color=INK):
        x0 = max(0, x)
        y0 = max(0, y)
        x1 = min(W, x + w)
        y1 = min(H, y + h)
        if x1 <= x0 or y1 <= y0:
            return
        pat = bytes(color) * (x1 - x0)
        for yy in range(y0, y1):
            row = self.px[yy]
            row[x0 * 3:x1 * 3] = pat

    def hline(self, x, y, w, color=INK, t=1):
        self.fill(x, y, w, t, color)

    def vline(self, x, y, h, color=INK, t=1):
        self.fill(x, y, t, h, color)

    def box(self, x, y, w, h, color=INK, t=1):
        self.hline(x, y, w, color, t)
        self.hline(x, y + h - t, w, color, t)
        self.vline(x, y, h, color, t)
        self.vline(x + w - t, y, h, color, t)

    def text(self, x, y, s, scale=1, color=INK):
        s = normalize(s)
        cx = x
        cb = bytes(color)
        for ch in s:
            g = FONT.get(ch)
            if g:
                for r, bits in enumerate(g):
                    if not bits:
                        continue
                    for col in range(5):
                        if (bits >> (4 - col)) & 1:
                            px0 = cx + col * scale
                            for sy in range(scale):
                                yy = y + r * scale + sy
                                if 0 <= yy < H:
                                    row = self.px[yy]
                                    row[px0 * 3:(px0 + scale) * 3] = cb * scale
            cx += 6 * scale
        return cx

    def ctext(self, x, y, w, s, scale=1, color=INK):
        tw = text_w(s, scale)
        self.text(x + max(0, (w - tw) // 2), y, s, scale, color)

    def para(self, x, y, w, s, scale=1, color=INK, lh=None):
        """Wrapped paragraph; returns y just past the last line."""
        lh = lh or (9 * scale)
        for line in wrap(s, w, scale):
            self.text(x, y, line, scale, color)
            y += lh
        return y

    def circle(self, cx, cy, r, color=INK, fill=True):
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                d = (xx - cx) ** 2 + (yy - cy) ** 2
                if fill:
                    if d <= r * r:
                        self.fill(xx, yy, 1, 1, color)
                else:
                    if r * r - 2 * r <= d <= r * r:
                        self.fill(xx, yy, 1, 1, color)

    def png_bytes(self):
        raw = b"".join(b"\x00" + bytes(row) for row in self.px)
        def chunk(typ, data):
            return (struct.pack(">I", len(data)) + typ + data +
                    struct.pack(">I", zlib.crc32(typ + data) & 0xFFFFFFFF))
        ihdr = struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0)
        return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr) +
                chunk(b"IDAT", zlib.compress(raw, 6)) + chunk(b"IEND", b""))

# ---------------------------------------------------------------- stories
# Every story below was first reported on Wednesday 25 November 2026
# (Reuters, RFE/RL, DW, UEFA, Jagran Josh, Starlit Daily). Older news is
# NOT in the main list: it is named in the DATE CHECK box instead.

LEAD = {
    "kicker": "UKRAINE · BLACK SEA · LIBYA",
    "head": "KYIV SAYS IT SANK A RUSSIAN WARSHIP OFF LIBYA",
    "body": ("President Volodymyr Zelenskyy confirmed Ukrainian forces struck "
             "two Russian vessels off the Libyan coast near Benghazi, sinking "
             "a warship. It is the furthest Kyiv has taken its strikes "
             "beyond Europe. Moscow did not immediately confirm the loss."),
    "src": "RFE/RL · REUTERS",
}

BIG = [
    {
        "kicker": "THE WAR · THE TOLL",
        "head": "700,000 RUSSIAN SOLDIERS KILLED, NEW COUNT SAYS",
        "body": ("More than 700,000 Russian soldiers have been killed in the "
                 "nearly five-year war on Ukraine, a new analysis finds, a "
                 "toll that underlines Moscow's drive to take ground at any "
                 "cost."),
        "src": "RFE/RL",
    },
    {
        "kicker": "YEMEN · SAUDI ARABIA",
        "head": "HOUTHI MISSILE HITS RIYADH'S TALLEST TOWER",
        "body": ("A Houthi missile struck the tallest tower in Riyadh, "
                 "wounding 11 people, Saudi civil defence said, as the "
                 "rebels push toward Aden. Britain sanctioned the Houthis "
                 "and four of their leaders."),
        "src": "REUTERS",
    },
]

GRID = [
    ("KYIV FLAT HIT, 11 DEAD",
     "Rescuers pulled bodies from a Kyiv-region apartment block hit by "
     "Russian drones; the toll reached 11.", "RFE/RL"),
    ("TURKEYS FREEDOM AND FEATHERS SPARED",
     "President Trump pardoned two turkeys at the White House on the eve "
     "of Thanksgiving.", "REUTERS"),
    ("DOLLAR PAUSES; FED HIKE SEEN 97% CERTAIN",
     "The dollar steadied before US inflation and growth data; traders "
     "price a December hike at 97%.", "REUTERS"),
    ("BITCOIN $59,508",
     "Bitcoin slipped 0.52% to $59,507.77; ether fell 0.54% to "
     "$1,669.73.", "REUTERS"),
    ("NIKKEI SEEN AT 67,500 BY END OF 2027",
     "A Reuters poll sees Japan's Nikkei at 65,000 by June 2027; it "
     "closed Tuesday at 58,644.63.", "REUTERS"),
    ("IRAQ MOVES ON KURDISH OILFIELDS",
     "Prime Minister Ali al-Zaidi ordered federal forces to seize "
     "oilfields and crossings in Kurdish-run areas.", "STARLIT DAILY"),
    ("BRITAIN SANCTIONS HOUTHIS",
     "London sanctioned the Houthi movement and four of its top "
     "officials.", "STARLIT DAILY"),
    ("CAR BOMB IN COLOMBIA WOUNDS 23",
     "A car bomb injured at least 23 people, officials said.",
     "STARLIT DAILY"),
    ("HAMAS SECURITY CHIEF KILLED IN GAZA",
     "A top Hamas security figure died in Israeli drone strikes in "
     "Gaza.", "STARLIT DAILY"),
    ("ENGLAND LEVEL T20 SERIES",
     "England beat Australia by eight wickets chasing 185 in the second "
     "T20 international.", "JAGRAN JOSH"),
]

MORE = [
    ("Iran gas crisis deepens as war damage bites", "RFE/RL"),
    ("Iran pharmacies run dry; patients hunt for medicine", "DW"),
    ("NATO plans early-warning jets for Poland", "JAGRAN JOSH"),
    ("Three tankers hit by mines in Strait of Hormuz", "JAGRAN JOSH"),
    ("UN warns of deepening Gaza humanitarian crisis", "JAGRAN JOSH"),
    ("EU announces fresh sanctions on Russia", "JAGRAN JOSH"),
    ("US and Qatar discuss strategic cooperation", "JAGRAN JOSH"),
    ("BJP and Akali Dal ally for 2027 Punjab polls", "JAGRAN JOSH"),
    ("FBI crime database hit in suspected breach", "STARLIT DAILY"),
    ("Gunmen hold dozens hostage in Cartagena shop", "STARLIT DAILY"),
    ("Rebels pull back in DR Congo after clashes", "STARLIT DAILY"),
    ("Xiamen Airlines orders 50 Boeing 737-8 jets", "STARLIT DAILY"),
    ("Bangladesh opens trade office in Guangzhou", "STARLIT DAILY"),
    ("Nigerian emir suspended over assault claim", "STARLIT DAILY"),
    ("RFE/RL back on shortwave for Afghan schoolgirls", "RFE/RL"),
    ("Trump gives Giuliani the Medal of Freedom", "REUTERS"),
    ("Iran FM: nuclear doctrine rethink has strong logic", "RFE/RL"),
    ("US bill would track Russian hybrid attacks", "RFE/RL"),
    ("US envoy unsure Israel military aid ends this year", "REUTERS"),
    ("S&P 500 seen up 12% by end of 2027 in poll", "REUTERS"),
    ("Zelenskyy presses NATO on membership", "STARLIT DAILY"),
    ("Kyiv's strikes reach beyond Europe", "STARLIT DAILY"),
]

NUMBERS = [
    ("700,000", "RUSSIAN SOLDIERS KILLED"),
    ("11", "DEAD IN KYIV STRIKE"),
    ("$59,508", "BITCOIN, USD"),
    ("103.85", "DOLLAR INDEX"),
    ("97%", "DEC FED HIKE ODDS"),
    ("50", "BOEING JETS ORDERED"),
]

DATE_CHECK = (
    "LEFT OUT AS OLDER NEWS: the missile that landed in Poland (20 NOV) - "
    "GTA 6 launch (19 NOV) - Nvidia's Huang returns as CEO (23 NOV) - "
    "Real Madrid 5-1 PSV (24 NOV) - Senegal's AFCON title restored by CAS "
    "(24 NOV) - Indonesia's VP Gibran resigned (12 NOV) - Sarkozy trial "
    "ordered (24 NOV) - Nepal PM's India visit (22-23 NOV)"
)

# ---------------------------------------------------------------- layout
MX = 16          # side margin
CW = W - 2 * MX  # content width


def draw_masthead(p, y):
    p.hline(MX, y, CW, INK, 3)
    p.hline(MX, y + 5, CW, INK, 1)
    y += 12
    p.ctext(MX, y, CW, "THE WORLD IN ONE DAY", 4)
    y += 34
    p.ctext(MX, y, CW, "WEDNESDAY, 25 NOVEMBER 2026  -  ONE DAY, ONE PAGE, EVERY STORY CHECKED",
            1)
    y += 12
    p.ctext(MX, y, CW, "35 STORIES  -  SIX CONTINENTS  -  EVERY STORY DATED 25 NOVEMBER 2026",
            1, DARK)
    y += 14
    p.hline(MX, y, CW, INK, 3)
    return y + 12


def draw_numbers(p, y):
    cell = CW // 6
    p.box(MX, y, CW, 50, INK, 2)
    for i, (num, lab) in enumerate(NUMBERS):
        x = MX + i * cell
        if i:
            p.vline(x, y, 50, INK, 1)
        p.ctext(x, y + 6, cell, num, 2)
        p.ctext(x, y + 30, cell, lab, 1, DARK)
    return y + 50 + 8


def draw_ship(p, x, y, w, h):
    """Simple ship pictogram: sea, tapered hull, funnel, mast, smoke."""
    p.fill(x, y, w, h, LIGHT)
    p.box(x, y, w, h, INK, 1)
    sea = y + h - 26
    p.fill(x + 1, sea, w - 2, 25, GRAY)
    p.hline(x + 1, sea, w - 2, INK, 1)
    # hull: short main block, deck, tapered bow to the right, stern left
    p.fill(x + 70, sea - 10, 150, 10, INK)
    p.fill(x + 85, sea - 19, 120, 9, INK)
    p.fill(x + 220, sea - 10, 30, 10, INK)
    p.fill(x + 240, sea - 6, 12, 6, INK)
    p.fill(x + 55, sea - 10, 15, 10, INK)
    # portholes along the hull
    for px in (95, 125, 155, 185):
        p.circle(x + px, sea - 5, 2, PAPER)
    # funnel with smoke
    p.fill(x + 120, sea - 40, 14, 21, INK)
    p.circle(x + 127, sea - 46, 4, DARK)
    p.circle(x + 118, sea - 53, 3, DARK)
    # mast and flag near the bow
    p.fill(x + 235, sea - 38, 2, 19, INK)
    p.fill(x + 237, sea - 38, 16, 8, INK)
    # wave lines
    p.hline(x + 10, sea + 8, 60, INK, 1)
    p.hline(x + w - 90, sea + 14, 70, INK, 1)
    p.text(x + 6, y + 6, "BENGHAZI, LIBYA", 1, DARK)


def draw_lead(p, y):
    y0 = y
    p.text(MX, y, LEAD["kicker"], 1, DARK)
    y += 11
    y = p.para(MX, y, 640, LEAD["head"], 2, INK, 17)
    y += 4
    y = p.para(MX, y, 640, LEAD["body"], 1, INK, 10)
    y += 3
    p.text(MX, y, "- " + LEAD["src"], 1, DARK)
    pic_x, pic_y, pic_w, pic_h = 676, y0, 332, 136
    draw_ship(p, pic_x, pic_y, pic_w, pic_h)
    return max(y + 12, pic_y + pic_h + 4)


def draw_big(p, y):
    colw = (CW - 12) // 2
    maxy = y
    for i, s in enumerate(BIG):
        x = MX + i * (colw + 12)
        p.hline(x, y, colw, INK, 2)
        yy = y + 6
        p.text(x, yy, s["kicker"], 1, DARK)
        yy += 11
        yy = p.para(x, yy, colw, s["head"], 2, INK, 17)
        yy += 3
        yy = p.para(x, yy, colw, s["body"], 1, INK, 10)
        yy += 3
        p.text(x, yy, "- " + s["src"], 1, DARK)
        maxy = max(maxy, yy + 10)
    return maxy


def draw_grid(p, y):
    p.hline(MX, y, CW, INK, 2)
    y += 6
    colw = (CW - 12) // 2
    row_h = 47
    for r in range(5):
        for c in range(2):
            head, body, src = GRID[r * 2 + c]
            x = MX + c * (colw + 12)
            yy = y + r * row_h
            p.text(x, yy, str(r * 2 + c + 4) + ". " + head, 1, INK)
            p.para(x, yy + 10, colw, body + " - " + src, 1, DARK, 9)
        if r < 4:
            p.hline(MX, y + (r + 1) * row_h - 5, CW, GRAY, 1)
    return y + 5 * row_h + 2

# ---------------------------------------------------------------- map
# Schematic world map: continents as blocks on a 56x28 grid, 5 px a cell.
# Pins mark the numbered stories; the legend below names them.
LAND = [
    (3, 3, 13, 5), (4, 8, 11, 3), (6, 11, 6, 2),      # N America
    (19, 3, 3, 2),                                       # Greenland
    (12, 14, 5, 3), (13, 17, 4, 4), (14, 21, 2, 2),     # S America
    (26, 4, 2, 2), (28, 4, 6, 4),                       # UK + Europe
    (27, 9, 8, 4), (28, 13, 6, 4), (29, 17, 4, 2),      # Africa
    (35, 4, 18, 5), (36, 9, 15, 3), (40, 12, 3, 3),     # Asia + India
    (45, 11, 4, 3), (46, 14, 6, 1),                     # SE Asia + isles
    (46, 18, 6, 3),                                      # Australia
    (53, 7, 2, 3),                                       # Japan
]
PINS = [
    (1, "BENGHAZI", 30, 10),
    (2, "KYIV", 32, 5),
    (3, "RIYADH", 36, 13),
    (4, "GAZA", 33, 11),
    (5, "HORMUZ", 39, 12),
    (6, "BAGHDAD", 35, 10),
    (7, "CARTAGENA", 13, 14),
    (8, "KINSHASA", 30, 16),
]
MAP_CELL = 6


def draw_map_panel(p, x, y, w):
    p.hline(x, y, w, INK, 2)
    p.text(x, y + 6, "WHERE IT HAPPENED", 1, INK)
    my = y + 20
    mx = x + 2
    for bx, by, bw, bh in LAND:
        p.fill(mx + bx * MAP_CELL, my + by * MAP_CELL,
               bw * MAP_CELL, bh * MAP_CELL, GRAY)
    p.text(mx + 2, my + 2, "ARCTIC", 1, DARK)
    p.text(mx + 2, my + 108, "PACIFIC", 1, DARK)
    p.text(mx + 118, my + 115, "ATLANTIC", 1, DARK)
    p.text(mx + 196, my + 130, "INDIAN OCEAN", 1, DARK)
    for num, _name, gx, gy in PINS:
        cx = mx + gx * MAP_CELL + MAP_CELL // 2
        cy = my + gy * MAP_CELL + MAP_CELL // 2
        p.circle(cx, cy, 5, INK)
        p.text(cx - 2, cy - 3, str(num), 1, PAPER)
    ly = my + 28 * MAP_CELL + 6
    leg = "  ".join("%d %s" % (n, nm) for n, nm, _, _ in PINS)
    ly = p.para(x, ly, w, leg, 1, DARK, 10)
    return ly + 4


def draw_more(p, x, y, w):
    p.hline(x, y, w, INK, 2)
    p.text(x, y + 6, "22 MORE STORIES", 1, INK)
    y += 20
    colw = (w - 12) // 2
    for i, (head, src) in enumerate(MORE):
        c = 0 if i < 11 else 1
        r = i if i < 11 else i - 11
        xx = x + c * (colw + 12)
        yy = y + r * 20
        p.text(xx, yy, "- " + head, 1, INK)
        p.text(xx, yy + 9, "  " + src, 1, DARK)
    return y + 11 * 20 + 2


def draw_datecheck(p, y):
    p.box(MX, y, CW, 64, INK, 2)
    p.text(MX + 8, y + 6, "DATE CHECK - LEFT OUT ON PURPOSE", 1, INK)
    p.para(MX + 8, y + 18, CW - 16, DATE_CHECK, 1, DARK, 10)
    return y + 64 + 8


def draw_footer(p, y):
    p.hline(MX, y, CW, INK, 3)
    y += 8
    p.ctext(MX, y, CW,
            "EVERY STORY HERE HAPPENED, OR WAS FIRST REPORTED, ON WEDNESDAY 25 NOVEMBER 2026",
            1)
    y += 11
    p.ctext(MX, y, CW,
            "SOURCES: REUTERS - RFE/RL - DW - UEFA - JAGRAN JOSH - STARLIT DAILY",
            1, DARK)
    y += 11
    p.ctext(MX, y, CW, "THE WORLD IN ONE DAY - 25 NOVEMBER 2026", 1, DARK)
    return y + 12


# ---------------------------------------------------------------- main
def build():
    p = Page()
    y = 10
    y = draw_masthead(p, y)
    y = draw_numbers(p, y)
    y = draw_lead(p, y)
    p.hline(MX, y, CW, INK, 1)
    y += 6
    y = draw_big(p, y)
    y = draw_grid(p, y)
    map_y = y + 4
    more_y = y + 4
    y1 = draw_map_panel(p, MX, map_y, 340)
    y2 = draw_more(p, MX + 352, more_y, CW - 352)
    y = max(y1, y2) + 6
    y = draw_datecheck(p, y)
    y = draw_footer(p, y)
    return p


def main():
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(outdir, exist_ok=True)
    data = build().png_bytes()
    path = os.path.join(outdir, "entry.png")
    with open(path, "wb") as f:
        f.write(data)
    import hashlib
    print("wrote %s %d bytes sha256=%s" %
          (path, len(data), hashlib.sha256(data).hexdigest()))


if __name__ == "__main__":
    main()
