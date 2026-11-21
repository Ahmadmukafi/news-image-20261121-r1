#!/usr/bin/env python3
"""Draw THE WORLD TODAY — Saturday 21 November 2026 front page (1024x1024).

PIL-only, build-time script. Run: python3 render.py  -> writes entry.png
All stories are real news of 21 Nov 2026 (lead verified vs CNN/Reuters/Fox).
"""
import random
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (20, 20, 20)
NAVY = (16, 38, 63)
NAVY2 = (24, 56, 90)
GOLD = (201, 162, 39)
RED = (179, 32, 44)
RED_DK = (140, 20, 30)
GREY = (90, 90, 88)
LINE = (200, 192, 175)

F = "/usr/share/fonts/truetype/dejavu/"
def font(name, size):
    return ImageFont.truetype(F + name, size)

SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img, "RGBA")

def wrap(text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines

def center(y, text, fnt, fill, x0=0, x1=W):
    w_ = d.textlength(text, font=fnt)
    d.text(((x0 + x1 - w_) / 2, y), text, font=fnt, fill=fill)

# ---------------- masthead ----------------
d.rectangle([0, 0, W, 116], fill=NAVY)
d.rectangle([0, 116, W, 120], fill=GOLD)
center(14, "THE WORLD TODAY", SERIF_B(62), (250, 247, 238))
d.line([24, 96, 1000, 96], fill=GOLD, width=1)
center(98, "S A T U R D A Y ,  2 1  N O V E M B E R  2 0 2 6", SANS_B(15), (216, 194, 122))
d.text((24, 98), "No. 325", font=SANS(13), fill=(180, 190, 200))
d.text((1000 - d.textlength("ONE PAGE  •  THE DAY", font=SANS(13)), 98),
       "ONE PAGE  •  THE DAY", font=SANS(13), fill=(180, 190, 200))

# ---------------- lead art panel ----------------
AX, AY, AW, AH = 20, 132, 580, 396
# night sky gradient
for i in range(AH):
    t = i / AH
    r = int(10 + (27 - 10) * t)
    g = int(22 + (58 - 22) * t)
    b = int(44 + (92 - 44) * t)
    d.line([AX, AY + i, AX + AW, AY + i], fill=(r, g, b))
rnd = random.Random(21112026)
for _ in range(90):
    x = AX + rnd.randint(4, AW - 4)
    y = AY + rnd.randint(4, AH - 120)
    s = rnd.choice([1, 1, 2])
    d.ellipse([x, y, x + s, y + s], fill=(235, 235, 220))
# moon
d.ellipse([AX + AW - 96, AY + 22, AX + AW - 48, AY + 70], fill=(238, 232, 200))
d.ellipse([AX + AW - 88, AY + 30, AX + AW - 56, AY + 62], fill=(210, 204, 175))
# missile trails (arcs) with bright heads
def trail(x0, y0, x1, y1, ctrl, col=(255, 214, 130)):
    pts = []
    for k in range(41):
        t = k / 40
        x = (1 - t) ** 2 * x0 + 2 * (1 - t) * t * ctrl[0] + t * t * x1
        y = (1 - t) ** 2 * y0 + 2 * (1 - t) * t * ctrl[1] + t * t * y1
        pts.append((x, y))
    for w_, a in ((7, 60), (4, 130), (2, 255)):
        d.line(pts, fill=col + (a,), width=w_, joint="curve")
    d.ellipse([x1 - 5, y1 - 5, x1 + 5, y1 + 5], fill=(255, 240, 200))
    d.ellipse([x1 - 11, y1 - 11, x1 + 11, y1 + 11], outline=(255, 200, 90), width=2)

trail(AX + 40, AY + 330, AX + 240, AY + 150, (AX + 120, AY + 180))
trail(AX + 120, AY + 350, AX + 380, AY + 120, (AX + 260, AY + 210))
trail(AX + 300, AY + 360, AX + 500, AY + 190, (AX + 420, AY + 250))
# skyline silhouette
base = AY + AH
for bx, bw, bh in [(0, 70, 60), (70, 46, 96), (116, 60, 52), (176, 40, 110),
                   (216, 66, 70), (282, 44, 92), (326, 58, 58), (384, 42, 118),
                   (426, 64, 66), (490, 90, 84)]:
    d.rectangle([AX + bx, base - bh, AX + bx + bw, base], fill=(8, 16, 28))
    for wy in range(base - bh + 10, base - 8, 16):
        for wx in range(AX + bx + 8, AX + bx + bw - 6, 14):
            if rnd.random() < 0.45:
                d.rectangle([wx, wy, wx + 4, wy + 6], fill=(255, 190, 90))
# bridge over the river (Dnipro) with arches
d.rectangle([AX, base - 26, AX + AW, base - 20], fill=(8, 16, 28))
for cx in range(AX + 30, AX + AW - 30, 90):
    d.arc([cx, base - 74, cx + 90, base - 14], 180, 360, fill=(8, 16, 28), width=6)
d.rectangle([AX, base - 20, AX + AW, base], fill=(16, 30, 50))
# explosions
def burst(cx, cy, r0, r1):
    for r, col in ((r1, (255, 122, 26)), (int(r1 * 0.62), (255, 194, 51)),
                   (int(r1 * 0.34), (255, 240, 180))):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
    for k in range(10):
        ang = rnd.uniform(0, 6.283)
        ex = cx + int((r1 + 14) * 0.9 * rnd.random() * 0.9 + 6)
        d.line([cx, cy, cx + int((r1 + 16) * 0.95 * __import__("math").cos(ang)),
                cy + int((r1 + 16) * 0.95 * __import__("math").sin(ang))],
               fill=(255, 160, 60), width=3)

burst(AX + 150, base - 150, 0, 34)
burst(AX + 330, base - 120, 0, 26)
burst(AX + 470, base - 190, 0, 20)
# smoke
for sx, sy, sr in [(AX + 150, base - 190, 46), (AX + 330, base - 155, 36),
                   (AX + 470, base - 220, 28)]:
    d.ellipse([sx - sr, sy - sr // 2, sx + sr, sy + sr // 2], fill=(120, 120, 125, 90))
# caption inside panel
d.rectangle([AX, base - 30, AX + AW, base], fill=(0, 0, 0, 110))
d.text((AX + 12, base - 26), "KYIV UNDER FIRE — MISSILE TRAILS OVER THE DNIPRO",
       font=SANS_B(14), fill=(255, 255, 255))
d.rectangle([AX, AY, AX + AW, AY + AH], outline=(0, 0, 0), width=2)

# ---------------- lead text (right column) ----------------
RX, RW = 620, 384
y = 136
d.text((RX, y), "WAR IN UKRAINE  •  KYIV", font=SANS_B(18), fill=RED)
y += 30
d.line([RX, y, RX + RW, y], fill=RED, width=3)
y += 12
for ln in ["RUSSIA'S", "BIGGEST", "BARRAGE YET"]:
    d.text((RX, y), ln, font=SERIF_B(38), fill=INK)
    y += 46
y += 4
deck = ("400+ drones and 110+ missiles rained on Ukraine overnight. "
        "Three Dnipro bridges hit, at least eight killed — and Russian "
        "missiles fell in Poland.")
for ln in wrap(deck, SANS(17), RW):
    d.text((RX, y), ln, font=SANS(17), fill=(40, 40, 40))
    y += 22
y += 10
# stat chips 2x2
stats = [("400+", "DRONES FIRED"), ("110+", "MISSILES FIRED"),
         ("8+", "PEOPLE KILLED"), ("3", "BRIDGES HIT")]
cw, ch, gap = 186, 54, 6
for i, (num, lab) in enumerate(stats):
    cx = RX + (i % 2) * (cw + gap)
    cy = y + (i // 2) * (ch + gap)
    d.rectangle([cx, cy, cx + cw, cy + ch], fill=NAVY)
    d.text((cx + 12, cy + 5), num, font=SANS_B(26), fill=(255, 255, 255))
    d.text((cx + 12, cy + 34), lab, font=SANS_B(12), fill=(216, 194, 122))

# ---------------- ticker strip ----------------
TY = 548
d.rectangle([0, TY, W, TY + 42], fill=RED_DK)
center(TY + 10, "MISSILES LAND IN NATO POLAND  —  TUSK CALLS IT A DELIBERATE PROVOCATION",
       SANS_B(19), (255, 255, 255))

# ---------------- story grid (3 cols x 2 rows) ----------------
def story(x, y, w, h, kicker, head, deck, kcol=RED):
    d.rectangle([x, y, x + w, y + h], outline=LINE, width=1)
    d.text((x + 12, y + 10), kicker, font=SANS_B(14), fill=kcol)
    hy = y + 32
    for ln in wrap(head, SERIF_B(22), w - 24):
        d.text((x + 12, hy), ln, font=SERIF_B(22), fill=INK)
        hy += 27
    dy = hy + 4
    for ln in wrap(deck, SANS(14), w - 24):
        d.text((x + 12, dy), ln, font=SANS(14), fill=(60, 60, 60))
        dy += 18

GY = 602
COLS = [20, 351, 682]
CW = 322
story(COLS[0], GY, CW, 158, "MARKETS",
      "AI sell-off pushes S&P 500 into correction",
      "Wall Street fell 3.7%; Nasdaq lost 5.3% and its 2026 gains.")
story(COLS[1], GY, CW, 158, "JUSTICE",
      "Court finds Myanmar guilty of genocide",
      "The UN's top court rules against Myanmar over the Rohingya.")
story(COLS[2], GY, CW, 158, "CLIMATE  •  ANTALYA",
      "COP31 talks run past deadline",
      "Nearly 200 nations deadlocked over fossil fuels in Antalya.")
story(COLS[0], GY + 164, CW, 158, "HEALTH",
      "Pill makes tumours undetectable in 1 in 12",
      "Trial drug daraxonrasib's big step against pancreatic cancer.")
story(COLS[1], GY + 164, CW, 158, "EUROPE",
      "UK and EU sign biggest post-Brexit deals",
      "Deals on food exports, carbon markets and youth mobility.")
story(COLS[2], GY + 164, CW, 158, "CULTURE",
      "GTA 6 smashes records on day one",
      "$4.9bn in first-day sales — the biggest launch ever.")

# ---------------- footer strip ----------------
FY = 936
d.line([20, FY, 1004, FY], fill=INK, width=2)
d.text((20, FY + 10), "IN BRIEF", font=SANS_B(15), fill=RED)
brief = ("Strong quake shakes Peru's Andes  •  FBI and US farm dept hacked  •  "
         "Gen Z protests in 25 European states")
d.text((118, FY + 10), brief, font=SANS(15), fill=(40, 40, 40))
d.text((20, FY + 38), "Sources: Reuters, CNN, AP, France 24, UN — all stories reported on 21 November 2026.",
       font=SANS(12), fill=GREY)

img.save("entry.png", optimize=True)
print("saved entry.png")
