#!/usr/bin/env python3
"""Draw the 24 November 2026 front page: "THE WORLD IN ONE PAGE".

One 1024x1024 newspaper-style PNG, drawn with Pillow and the DejaVu
fonts on this machine. Every story below was first reported on
Tuesday 24 November 2026 (live web research this session, Reuters /
AP / WSJ / CNN / TOI digests):

  Lead 1 (Indonesia): a candy-factory fire's death toll climbs to
  24, with around 30 workers still missing as rescuers search the
  rubble.
  Lead 2 (tech/markets): Nvidia's board reinstates Jensen Huang as
  CEO 11 days after he quit; shares leap a third, the Nasdaq rallies
  6%, and the US blacklists Megaspeed, the firm tied to the spy row.
  Grid (24): Russian drone and missile attacks kill people in the
  Kyiv region; the Russian cargo ship Sparta II still burning in the
  Gulf of Finland after a drone strike; India and Nepal sign 8 MoUs
  with a Rs 15,000 crore package; China sets 2030 elderly-care and
  childcare targets; Bangladesh vows to arrest ex-PM Hasina if she
  returns; Armenia proposes a new constitution to advance peace with
  Azerbaijan; Denmark's top court backs the hardline "ghetto law";
  450 German schools get bomb threats by email; Lahore tops the
  world pollution ranking with AQI past 500; a US appeals court gives
  Trump a path to erasing his hush-money conviction; Trump blames
  Democrats for a $1tn market sell-off after the midterms; Chicago's
  O'Hare halts flights briefly over staffing in the Thanksgiving
  rush; Trump attacks Newsom over 548 death-row commutations; Kash
  Patel's $41m fraud probe raids child centres in Minnesota; a former
  Mississippi mayor is jailed 37 months for bribery; 25 tankers hit
  in a week in the Strait of Hormuz as traffic falls 20%; a former
  Mossad chief says Israel saved Taylor Swift's Vienna concerts from
  an ISIS-inspired plot; a Chinese official is sentenced to death for
  leaking 100 intelligence reports; South Korea's president names a
  new foreign minister and intelligence chief; the India-New Zealand
  first Test ends in a draw at Wellington; Gukesh begins his world
  title defence against Sindarov in Geneva; Alcaraz wins a maiden ATP
  Finals title over Zverev; FIFA picks hosts for the 2031 and 2035
  Women's World Cups; India's Sensex sinks 1,484 points.
  Ticker: King Charles reaches out to Meghan, Modi opens an AI
  centre at IIT Patna, India-China talks in Arunachal, a Godhra bail,
  a Dutch activist dying by euthanasia at 28, and Pakistan inviting
  India to an SCO meet.

Tile bodies are capped at two lines at 11px; the script prints
OVERFLOW for anything that does not fit, so a bad tile is caught
before the image ships.

Run:  python3 build_image.py   (writes entry.png next to it)
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = Path(__file__).resolve().parent / "entry.png"

PAPER = (250, 246, 236)
INK = (22, 22, 26)
NAVY = (18, 38, 66)
RED = (178, 34, 34)
STEEL = (70, 90, 115)
MUTED = (90, 86, 76)
RULE = (205, 198, 184)
CARD = (255, 253, 247)
DARK = (18, 38, 66)
SEA = (16, 42, 74)
SKY = (214, 228, 238)
GREEN = (34, 120, 70)

FONTS = Path("/usr/share/fonts/truetype/dejavu")
SERIF_B = str(FONTS / "DejaVuSerif-Bold.ttf")
SERIF_R = str(FONTS / "DejaVuSerif.ttf")
SANS_R = str(FONTS / "DejaVuSans.ttf")
SANS_B = str(FONTS / "DejaVuSans-Bold.ttf")


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, width):
    """Greedy word wrap to a pixel width."""
    out, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                out.append(cur)
            cur = word
    if cur:
        out.append(cur)
    return out


def capped(d, text, fnt, width, most):
    """Wrap text, report whether it exceeds `most` lines."""
    lines = wrap(d, text, fnt, width)
    return lines, len(lines) > most


# ------------------------------------------------------------------ stories
LEAD_STORIES = [
    {
        "kicker": "INDONESIA  ·  FACTORY FIRE",
        "headline": "Factory fire toll climbs to 24 as rescuers search for 30 missing",
        "body": ("A candy-factory blaze leaves at least 24 dead; rescuers "
                 "keep digging for around 30 workers still missing."),
        "art": "fire",
    },
    {
        "kicker": "TECH  ·  HUANG IS BACK",
        "headline": "Nvidia brings Huang back as shares leap a third",
        "body": ("The board reinstates Jensen Huang 11 days after he quit; "
                 "the Nasdaq rallies 6% and the US blacklists Megaspeed."),
        "art": "chip",
    },
]

# (tag, headline, body) -- bodies trimmed to two lines at 11px.
GRID = [
    ("UKRAINE", "Kyiv region strikes kill",
     "Russian drone and missile attacks hit a building in Dymer."),
    ("BALTIC", "Sparta II still burning",
     "Russian cargo ship ablaze in the Gulf of Finland after a drone strike."),
    ("ASIA", "India\u2013Nepal sign 8 pacts",
     "Modi and Balendra Shah agree a Rs 15,000 crore package."),
    ("ASIA", "China's 2030 care targets",
     "Beijing sets elderly-care and childcare goals for 2030."),
    ("ASIA", "Dhaka: arrest Hasina",
     "Bangladesh vows to arrest the ex-PM if she returns from India."),
    ("EUROPE", "Armenia's new charter",
     "Yerevan proposes a constitution to advance Azerbaijan peace."),
    ("EUROPE", "Denmark backs 'ghetto law'",
     "Top court upholds the hardline immigration law."),
    ("EUROPE", "450 German schools threatened",
     "Bomb threats emailed to schools across Germany."),
    ("ASIA", "Lahore chokes at AQI 500+",
     "Lahore tops the world pollution ranking; eight cities worst."),
    ("AMERICAS", "Trump hush-money path",
     "Appeals court gives Trump a path to erase his conviction."),
    ("AMERICAS", "Trump blames Democrats",
     "Trump blames Democrats for a $1tn sell-off after midterms."),
    ("AMERICAS", "O'Hare ground stop",
     "Chicago airport halts flights briefly over staffing."),
    ("AMERICAS", "Newsom's 548 commutations",
     "Trump attacks Newsom in a DOJ speech over death-row clemency."),
    ("AMERICAS", "Minnesota fraud raids",
     "Kash Patel's $41m probe raids child centres in Minnesota."),
    ("AMERICAS", "Ex-mayor jailed 37 months",
     "Former Jackson mayor sentenced in a bribery scheme."),
    ("MIDEAST", "Gulf tanker toll mounts",
     "25 tankers hit in a week in Hormuz; traffic falls 20%."),
    ("MIDEAST", "Mossad saved Swift shows",
     "Ex-Mossad chief: Vienna concerts saved from an ISIS plot."),
    ("ASIA", "China official faces death",
     "Official sentenced to death for leaking 100 intel reports."),
    ("ASIA", "Seoul's new envoys",
     "South Korea names a new foreign minister and spy chief."),
    ("SPORT", "India\u2013NZ Test drawn",
     "First Test ends in a draw at Wellington's Basin Reserve."),
    ("SPORT", "Chess worlds begin",
     "Gukesh defends his title against Sindarov in Geneva."),
    ("SPORT", "Alcaraz takes ATP Finals",
     "Spaniard beats Zverev for a maiden title in Turin."),
    ("SPORT", "FIFA picks Women's WC hosts",
     "Congress selects hosts for the 2031 and 2035 World Cups."),
    ("BUSINESS", "Sensex sinks 1,484",
     "Indian markets fall 1.77% to 82,435; Nifty drops 451."),
]

TICKER = ("KING CHARLES REACHES OUT TO MEGHAN  \u00b7  MODI OPENS AI "
           "CENTRE AT IIT PATNA  \u00b7  INDIA\u2013CHINA TALKS IN "
           "ARUNACHAL  \u00b7  GODHRA BAIL GRANTED  \u00b7  DUTCH ACTIVIST "
           "DIES BY EUTHANASIA AT 28  \u00b7  PAKISTAN TO INVITE INDIA TO "
           "SCO MEET")


# ---------------------------------------------------------------------- art
def art_fire(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(40, 26, 22))
    # factory silhouette
    d.rectangle([x + 14, y + h - 34, x + 150, y + h], fill=(90, 70, 60))
    d.rectangle([x + 160, y + h - 48, x + 172, y + h], fill=(90, 70, 60))
    d.rectangle([x + 176, y + h - 40, x + 188, y + h], fill=(90, 70, 60))
    d.rectangle([x + 24, y + h - 26, x + 44, y + h - 10], fill=(232, 120, 40))
    d.rectangle([x + 56, y + h - 26, x + 76, y + h - 10], fill=(232, 120, 40))
    # flames licking up
    d.ellipse([x + 210, y + 8, x + 250, y + 48], fill=(232, 120, 40))
    d.ellipse([x + 222, y + 18, x + 240, y + 38], fill=(250, 200, 90))
    d.ellipse([x + 280, y + 2, x + 306, y + 30], fill=(232, 120, 40))
    d.ellipse([x + 288, y + 10, x + 300, y + 24], fill=(250, 200, 90))
    # smoke
    d.ellipse([x + 300, y + 30, x + 340, y + 52], fill=(120, 110, 100))
    d.ellipse([x + 330, y + 18, x + 360, y + 40], fill=(140, 130, 120))


def art_chip(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    # rising market bars, green, last one tallest
    bars = [10, 16, 14, 24, 34]
    bx = x + 16
    for i, bh in enumerate(bars):
        col = GREEN if i == len(bars) - 1 else STEEL
        d.rectangle([bx + i * 44, y + h - 10 - bh, bx + i * 44 + 28,
                     y + h - 10], fill=col)
    d.line([x + 8, y + h - 10, x + w - 8, y + h - 10], fill=NAVY, width=2)
    # arrow up over the bars, stopping short of the chip
    d.line([x + 20, y + h - 26, x + w - 150, y + 14], fill=GREEN, width=3)
    d.line([x + w - 150, y + 14, x + w - 172, y + 16], fill=GREEN, width=3)
    d.line([x + w - 150, y + 14, x + w - 152, y + 36], fill=GREEN, width=3)
    # chip, right
    cx, cy = x + w - 96, y + h // 2
    d.rectangle([cx - 34, cy - 20, cx + 34, cy + 20], fill=NAVY)
    d.rectangle([cx - 18, cy - 10, cx + 18, cy + 10], fill=GREEN)
    for k in range(4):
        d.line([cx - 34, cy - 14 + k * 9, cx - 42, cy - 14 + k * 9],
               fill=NAVY, width=2)
        d.line([cx + 34, cy - 14 + k * 9, cx + 42, cy - 14 + k * 9],
               fill=NAVY, width=2)


# --------------------------------------------------------------------- page
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 28
    cw = W - 2 * mx  # 968

    # ---- masthead
    d.text((W // 2, 16), "THE WORLD IN ONE PAGE", font=F(SERIF_B, 56),
           fill=INK, anchor="mt")
    d.line([mx, 80, W - mx, 80], fill=INK, width=3)
    d.line([mx, 85, W - mx, 85], fill=INK, width=1)
    d.text((W // 2, 92), "TUESDAY 24 NOVEMBER 2026", font=F(SANS_B, 21),
           fill=RED, anchor="mt")
    d.text((W // 2, 120), "32 stories  \u00b7  one day  \u00b7  No. 329",
           font=F(SANS_R, 15), fill=MUTED, anchor="mt")

    # ---- leads: two cards, art strip on top
    ly, lh = 150, 220
    lw = (cw - 16) // 2
    problems = []
    for i, lead in enumerate(LEAD_STORIES):
        x0 = mx + i * (lw + 16)
        d.rectangle([x0, ly, x0 + lw, ly + lh], outline=INK, width=2,
                    fill=CARD)
        (art_fire if lead["art"] == "fire" else art_chip)(
            d, x0 + 2, ly + 2, lw - 4, 58)
        ty = ly + 68
        d.text((x0 + 12, ty), lead["kicker"], font=F(SANS_B, 13), fill=RED)
        hy = ty + 20
        for ln in wrap(d, lead["headline"], F(SERIF_B, 25), lw - 24):
            d.text((x0 + 12, hy), ln, font=F(SERIF_B, 25), fill=INK)
            hy += 30
        by = hy + 6
        for ln in wrap(d, lead["body"], F(SERIF_R, 14), lw - 24):
            d.text((x0 + 12, by), ln, font=F(SERIF_R, 14), fill=INK)
            by += 18

    # ---- grid: 4 columns x 6 rows
    gy, gh = 384, 560
    cols, rows = 4, 6
    gap = 12
    tw = (cw - (cols - 1) * gap) // cols
    th = (gh - (rows - 1) * 10) // rows
    for idx, (tag, head, body) in enumerate(GRID):
        r, c = divmod(idx, cols)
        x0 = mx + c * (tw + gap)
        y0 = gy + r * (th + 10)
        d.rectangle([x0, y0, x0 + tw, y0 + th], outline=RULE, width=1,
                    fill=CARD)
        d.text((x0 + 9, y0 + 6), tag, font=F(SANS_B, 10), fill=NAVY)
        hl, hov = capped(d, head, F(SANS_B, 14), tw - 18, 2)
        if hov:
            problems.append(("headline", head))
        hy = y0 + 21
        for ln in hl:
            d.text((x0 + 9, hy), ln, font=F(SANS_B, 14), fill=INK)
            hy += 17
        bl, bov = capped(d, body, F(SANS_R, 11), tw - 18, 2)
        if bov:
            problems.append(("body", body))
        by = hy + 2
        for ln in bl[:2]:
            d.text((x0 + 9, by), ln, font=F(SANS_R, 11), fill=(40, 40, 44))
            by += 14

    # ---- footer ticker + sources
    fy = 962
    d.rectangle([mx, fy, W - mx, fy + 38], fill=DARK)
    tl = wrap(d, TICKER, F(SANS_B, 12), cw - 20)
    if len(tl) > 2:
        problems.append(("ticker", f"{len(tl)} lines"))
    ty = fy + 5
    for ln in tl[:2]:
        d.text((W // 2, ty), ln, font=F(SANS_B, 12),
               fill=(250, 246, 236), anchor="mt")
        ty += 15
    d.text((W // 2, fy + 42),
           "Sources: Reuters  \u00b7  AP  \u00b7  WSJ  \u00b7  CNN  \u00b7  BBC  \u2014  "
           "All stories first reported on Tuesday 24 November 2026.",
           font=F(SANS_R, 11), fill=MUTED, anchor="mt")

    for kind, text in problems:
        print(f"OVERFLOW {kind}: {text[:60]}")
    img.save(OUT, "PNG")
    print(f"wrote {OUT} {img.size} tile={tw}x{th}")
    return problems


if __name__ == "__main__":
    build()
