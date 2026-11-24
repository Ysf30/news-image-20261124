#!/usr/bin/env python3
"""Draw the 24 November 2026 front page: THE WORLD IN ONE PAGE.

Own work, written fresh for news-image-20261124. Uses only Pillow and the
standard library. Deterministic: same input, same bytes every run.
"""
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = Path(__file__).resolve().parent / "entry.png"

INK = (24, 26, 32)
PAPER = (247, 243, 234)
NAVY = (18, 32, 61)
NAVY2 = (30, 52, 96)
RED = (178, 34, 34)
TEAL = (13, 110, 105)
GOLD = (198, 142, 22)
GREY = (96, 98, 104)
LIGHT_LINE = (205, 199, 186)
CARD = (255, 255, 255)


def font(name, size):
    base = Path("/usr/share/fonts/truetype/dejavu")
    try:
        return ImageFont.truetype(str(base / name), size)
    except OSError:
        return ImageFont.load_default()


F_TITLE = font("DejaVuSans-Bold.ttf", 58)
F_DATE = font("DejaVuSans.ttf", 21)
F_LEAD_K = font("DejaVuSans-Bold.ttf", 15)
F_LEAD_H = font("DejaVuSans-Bold.ttf", 24)
F_LEAD_B = font("DejaVuSans.ttf", 15)
F_KICK = font("DejaVuSans-Bold.ttf", 12)
F_HEAD = font("DejaVuSans-Bold.ttf", 15)
F_BODY = font("DejaVuSans.ttf", 12)
F_TICK = font("DejaVuSans.ttf", 14)
F_SRC = font("DejaVuSans-Bold.ttf", 13)


def wrap(draw, text, fnt, width):
    """Wrap text to fit pixel width, returning a list of lines."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        cur = ""
        for word in words:
            trial = (cur + " " + word).strip()
            if draw.textlength(trial, font=fnt) <= width:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
    return lines


LEADS = [
    ("INDONESIA  |  DISASTER", "Candy factory fire leaves 24 dead",
     "Rescuers search the burned Cikande sweet plant as about 30 workers stay missing."),
    ("MARKETS  |  TECH", "Huang returns to Nvidia; shares soar",
     "Eleven days after quitting, the founder is back; shares jump a third, Nasdaq +6%."),
]

# (kicker, headline, one-line body) — 24 stories, my own wording.
STORIES = [
    ("UKRAINE", "Russian drones and missiles strike Kyiv region",
     "Overnight strikes kill civilians and knock out power in the region."),
    ("BALTIC SEA", "Stricken tanker Sparta II still burning",
     "The damaged tanker smoulders in the Gulf of Finland."),
    ("SOUTH ASIA", "India and Nepal sign eight agreements",
     "A Rs 15,000 crore package covers energy, roads and trade."),
    ("CHINA", "Beijing sets 2030 care targets",
     "New goals promise wider elderly care and cheaper childcare."),
    ("BANGLADESH", "Dhaka vows to arrest Hasina on return",
     "The ex-PM faces trial if she returns home, Dhaka says."),
    ("ARMENIA", "A new constitution takes shape",
     "A rewritten basic law would reshape the presidency and courts."),
    ("DENMARK", "Copenhagen backs the 'ghetto law'",
     "Rules letting the state break up 'parallel' areas stay in force."),
    ("GERMANY", "Bomb threats hit 450 schools",
     "Police clear classrooms nationwide after emailed threats."),
    ("PAKISTAN", "Lahore chokes as smog tops AQI 500",
     "Winter haze leaves the city among the world's most polluted."),
    ("UNITED STATES", "Court opens a path to erase Trump conviction",
     "An appeals ruling could wipe the hush-money verdict."),
    ("UNITED STATES", "Trump blames Democrats for $1tn sell-off",
     "The president blames the opposition for a $1tn market fall."),
    ("UNITED STATES", "Ground stop snarls Chicago O'Hare",
     "Departures halt at one of the world's busiest airports."),
    ("UNITED STATES", "Newsom commutes 548 sentences",
     "Hundreds of prisoners can now seek earlier release."),
    ("UNITED STATES", "FBI raids target $41m Minnesota fraud",
     "Agents move on a network accused of siphoning federal aid."),
    ("UNITED STATES", "Ex-mayor jailed for 37 months",
     "A former Mississippi mayor is sentenced for corruption."),
    ("MIDDLE EAST", "25 tankers struck in a week in Hormuz",
     "Attacks on shipping rattle oil markets and insurers."),
    ("ISRAEL", "Ex-spy chief: Israel saved Swift shows",
     "Israeli intelligence helped foil the Vienna plot, he says."),
    ("CHINA", "Official sentenced to death for leaks",
     "A state official is condemned for passing on intel reports."),
    ("SOUTH KOREA", "Seoul names top diplomat and spy chief",
     "New faces take charge of foreign affairs and intelligence."),
    ("CRICKET", "India and New Zealand draw at Wellington",
     "Rain and stubborn batting leave the Test level."),
    ("CHESS", "Gukesh opens world title defence",
     "The champion begins his crown defence in Geneva."),
    ("TENNIS", "Alcaraz claims a first ATP Finals crown",
     "The Spaniard seals the season-ending title."),
    ("FOOTBALL", "FIFA names 2031 and 2035 Women's Cup hosts",
     "The next two tournaments get their homes."),
    ("INDIA", "Sensex slides 1,484 points",
     "Mumbai shares tumble in a broad sell-off."),
]

TICKER = (
    "LONDON — King Charles reaches out to Meghan  •  PATNA — Modi opens an AI centre at IIT  •  "
    "ARUNACHAL — India and China hold border talks  •  GODHRA — Bail granted in long-running case  •  "
    "THE NETHERLANDS — Dutch activist, 28, dies by euthanasia  •  ISLAMABAD — Pakistan to invite India to SCO meet"
)


def draw_masthead(d):
    d.rectangle([0, 0, W, 118], fill=NAVY)
    d.rectangle([0, 118, W, 122], fill=GOLD)
    # small globe mark left of the title
    cx, cy, r = 52, 59, 30
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=GOLD, width=3)
    d.ellipse([cx - r + 8, cy - r + 8, cx + r - 8, cy + r - 8], outline=(120, 150, 200), width=2)
    d.line([cx - r, cy, cx + r, cy], fill=(120, 150, 200), width=2)
    d.line([cx, cy - r, cx, cy + r], fill=(120, 150, 200), width=2)
    title = "THE WORLD IN ONE PAGE"
    tw = d.textlength(title, font=F_TITLE)
    d.text(((W - tw) / 2 + 18, 16), title, font=F_TITLE, fill=(255, 255, 255))
    date = "TUESDAY 24 NOVEMBER 2026  •  ALL THE DAY'S NEWS  •  ONE PAGE"
    dw = d.textlength(date, font=F_DATE)
    d.text(((W - dw) / 2 + 18, 84), date, font=F_DATE, fill=(214, 196, 130))


def draw_leads(d):
    y0, hgt = 132, 140
    for i, (kick, head, body) in enumerate(LEADS):
        x0 = 8 + i * 508
        d.rectangle([x0, y0, x0 + 496, y0 + hgt], fill=CARD, outline=LIGHT_LINE, width=1)
        d.rectangle([x0, y0, x0 + 6, y0 + hgt], fill=RED if i == 0 else TEAL)
        tx = x0 + 20
        d.text((tx, y0 + 10), kick, font=F_LEAD_K, fill=RED if i == 0 else TEAL)
        head_lines = wrap(d, head, F_LEAD_H, 456)[:2]
        for j, line in enumerate(head_lines):
            d.text((tx, y0 + 32 + j * 27), line, font=F_LEAD_H, fill=INK)
        # short rule sits below the headline, wherever it ends
        rule_y = y0 + 34 + len(head_lines) * 27
        d.rectangle([tx, rule_y, tx + 64, rule_y + 3], fill=RED if i == 0 else TEAL)
        for j, line in enumerate(wrap(d, body, F_LEAD_B, 456)[:2]):
            d.text((tx, rule_y + 12 + j * 18), line, font=F_LEAD_B, fill=GREY)


def draw_grid(d):
    x0, y0 = 8, 280
    cw, chh, gx, gy = 246, 100, 8, 7
    for idx, (kick, head, body) in enumerate(STORIES):
        row, col = divmod(idx, 4)
        x = x0 + col * (cw + gx)
        y = y0 + row * (chh + gy)
        d.rectangle([x, y, x + cw, y + chh], fill=CARD, outline=LIGHT_LINE, width=1)
        d.rectangle([x, y, x + cw, y + 3], fill=NAVY2 if idx % 2 == 0 else GOLD)
        tx = x + 10
        d.text((tx, y + 10), kick, font=F_KICK, fill=RED)
        lines = wrap(d, head, F_HEAD, cw - 20)[:2]
        for j, line in enumerate(lines):
            d.text((tx, y + 28 + j * 17), line, font=F_HEAD, fill=INK)
        blines = wrap(d, body, F_BODY, cw - 20)[:2]
        for j, line in enumerate(blines):
            d.text((tx, y + 64 + j * 15), line, font=F_BODY, fill=GREY)


def draw_footer(d):
    y0 = 924
    d.rectangle([0, y0, W, H], fill=NAVY)
    d.rectangle([0, y0, W, y0 + 3], fill=GOLD)
    lines = wrap(d, TICKER, F_TICK, W - 32)
    for j, line in enumerate(lines):
        d.text((16, y0 + 12 + j * 18), line, font=F_TICK, fill=(232, 230, 222))
    src = "SOURCES: REUTERS  •  AP  •  WSJ  •  CNN  •  BBC    —    32 STORIES  •  TUESDAY 24 NOVEMBER 2026"
    sw = d.textlength(src, font=F_SRC)
    d.text(((W - sw) / 2, y0 + 66), src, font=F_SRC, fill=(214, 196, 130))


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_masthead(d)
    draw_leads(d)
    draw_grid(d)
    draw_footer(d)
    img.save(OUT, format="PNG", optimize=True)
    return OUT


if __name__ == "__main__":
    path = build()
    print(f"wrote {path} ({path.stat().st_size} bytes)")
