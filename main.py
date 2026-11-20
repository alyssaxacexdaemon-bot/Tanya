#!/usr/bin/env python3
"""
Sum up 19 November 2026 world news in one image.
make.fun bounty: news-image-20261119, $250, 50 places paid.
Deadline: Sat 21 Nov 2026 00:00 UTC.

Deterministic: no network, no random, no timestamps, no external files.
Draws a 1024x1024 newspaper front page with Pillow only and writes
one PNG to /output/entry.png (and a local copy entry.png beside this file).

Run: python3 main.py
Requires: Pillow (PIL). Fonts: DejaVu Sans if present, else Pillow default.
"""

import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

NAVY = (15, 42, 68)
NAVY_LIGHT = (27, 68, 102)
RED = (192, 57, 43)
TEAL = (14, 124, 123)
AMBER = (176, 124, 0)
DARK = (20, 20, 20)
GREY = (90, 90, 90)
LIGHT_BLUE = (234, 242, 248)
LIGHT_GREY = (245, 245, 244)
LIGHT_TEAL = (232, 244, 243)
LIGHT_AMBER = (253, 243, 220)
WHITE = (255, 255, 255)
BORDER = (15, 42, 68)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def load_font(name, size):
    path = os.path.join(FONT_DIR, name)
    try:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    except Exception:
        pass
    try:
        return ImageFont.truetype(name, size)
    except Exception:
        return ImageFont.load_default()


F_TITLE = lambda s: load_font("DejaVuSans-Bold.ttf", s)
F_BODY = lambda s: load_font("DejaVuSans.ttf", s)
F_BODY_B = lambda s: load_font("DejaVuSans-Bold.ttf", s)


def wrap(draw, text, font, max_width):
    """Wrap text into lines that fit max_width, using measured widths."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, font, color, max_width, line_h):
    for line in wrap(draw, text, font, max_width):
        draw.text((x, y), line, font=font, fill=color)
        y += line_h
    return y


def panel(draw, x, y, w, h, fill, accent):
    draw.rectangle([x, y, x + w, y + h], fill=fill, outline=BORDER, width=2)
    draw.rectangle([x, y, x + w, y + 8], fill=accent)


def draw():
    img = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(img)

    # Outer border
    d.rectangle([4, 4, W - 5, H - 5], outline=NAVY, width=4)

    # ---- Masthead ----
    d.rectangle([8, 8, W - 9, 148], fill=NAVY)
    d.text((32, 22), "WORLD NEWS IN ONE IMAGE", font=F_TITLE(48), fill=WHITE)
    d.text((32, 88), "THURSDAY  •  19 NOVEMBER 2026", font=F_BODY_B(28), fill=(255, 214, 90))
    d.text((748, 88), "THE WORLD, TODAY", font=F_BODY(22), fill=(200, 220, 235))

    # ---- Panel 1: Lead — Trump, Xi, Putin (full width) ----
    px, py, pw, ph = 24, 164, 976, 208
    panel(d, px, py, pw, ph, LIGHT_BLUE, RED)
    # Icon: three overlapping circles with initials
    cx, cy, r = 880, 250, 34
    for i, (ox, letter) in enumerate([(-64, "T"), (0, "X"), (64, "P")]):
        x0 = cx + ox - r
        d.ellipse([x0, cy - r, x0 + 2 * r, cy + r], outline=NAVY, width=4, fill=WHITE)
        tw = d.textlength(letter, font=F_TITLE(30))
        d.text((x0 + r - tw / 2, cy - 21), letter, font=F_TITLE(30), fill=NAVY)
    d.text((48, 186), "1  •  SHENZHEN SUMMIT", font=F_BODY_B(20), fill=RED)
    y = draw_wrapped(d, 48, 214, "TRUMP, XI & PUTIN MEET", F_TITLE(38), NAVY, 820, 46)
    y = draw_wrapped(d, 48, y + 2, "IN SHENZHEN", F_TITLE(38), NAVY, 820, 46)
    draw_wrapped(
        d, 48, y + 6,
        "First three-way summit at APEC. Joint peace declaration,",
        F_BODY(23), DARK, 820, 30,
    )
    draw_wrapped(
        d, 48, y + 36,
        "talks on nuclear risks and stable energy flows.",
        F_BODY(23), DARK, 820, 30,
    )

    # ---- Panel 2: ICJ Myanmar (left, middle) ----
    px, py, pw, ph = 24, 388, 480, 248
    panel(d, px, py, pw, ph, WHITE, NAVY)
    # Scales of justice icon (top-right, clear of the headline)
    ix, iy = 468, 414
    d.line([(ix, iy), (ix, iy + 38)], fill=NAVY, width=4)
    d.line([(ix - 24, iy + 9), (ix + 24, iy + 9)], fill=NAVY, width=4)
    d.polygon([(ix - 34, iy + 38), (ix - 14, iy + 38), (ix - 24, iy + 23)], outline=NAVY, width=3)
    d.polygon([(ix + 14, iy + 38), (ix + 34, iy + 38), (ix + 24, iy + 23)], outline=NAVY, width=3)
    d.text((48, 410), "2  •  THE HAGUE", font=F_BODY_B(20), fill=NAVY)
    y = draw_wrapped(d, 48, 440, "COURT: MYANMAR", F_TITLE(31), NAVY, 380, 38)
    y = draw_wrapped(d, 48, y, "GUILTY OF GENOCIDE", F_TITLE(29), NAVY, 432, 38)
    draw_wrapped(
        d, 48, y + 8,
        "UN court rules Myanmar committed state-sponsored genocide against Rohingya Muslims — a first.",
        F_BODY(22), DARK, 432, 29,
    )

    # ---- Panel 3: Cyclone Akvan (right, middle) ----
    px, py, pw, ph = 520, 388, 480, 248
    panel(d, px, py, pw, ph, LIGHT_TEAL, TEAL)
    # Cyclone spiral icon: concentric arcs
    ix, iy = 920, 432
    for rr in (44, 32, 20):
        d.arc([ix - rr, iy - rr, ix + rr, iy + rr], start=20, end=300, fill=TEAL, width=5)
    d.text((544, 410), "3  •  INDIA", font=F_BODY_B(20), fill=TEAL)
    y = draw_wrapped(d, 544, 440, "CYCLONE AKVAN", F_TITLE(31), NAVY, 432, 38)
    y = draw_wrapped(d, 544, y, "HEADS FOR COAST", F_TITLE(31), NAVY, 432, 38)
    draw_wrapped(
        d, 544, y + 8,
        "Severe storm due Fri 20 Nov on Andhra Pradesh–Odisha coast, winds 90–100 km/h, gusts to 110.",
        F_BODY(22), DARK, 432, 29,
    )

    # ---- Panel 4: Riyadh PIF Tower (full width, lower) ----
    px, py, pw, ph = 24, 652, 976, 196
    panel(d, px, py, pw, ph, LIGHT_AMBER, AMBER)
    # Tower icon: tall building with crack
    tx, ty = 908, 692
    d.rectangle([tx, ty, tx + 56, ty + 120], outline=NAVY, width=4, fill=WHITE)
    d.rectangle([tx + 8, ty + 12, tx + 20, ty + 24], fill=NAVY)
    d.rectangle([tx + 28, ty + 12, tx + 40, ty + 24], fill=NAVY)
    d.rectangle([tx + 8, ty + 36, tx + 20, ty + 48], fill=NAVY)
    d.rectangle([tx + 28, ty + 36, tx + 40, ty + 48], fill=NAVY)
    d.line([(tx + 10, ty + 60), (tx + 28, ty + 78), (tx + 14, ty + 92), (tx + 34, ty + 110)],
           fill=RED, width=5)
    d.text((48, 674), "4  •  RIYADH", font=F_BODY_B(20), fill=AMBER)
    y = draw_wrapped(d, 48, 702, "RIYADH TOWER HIT IN MISSILE ATTACK", F_TITLE(30), NAVY, 830, 38)
    y = draw_wrapped(
        d, 48, y + 8,
        "The PIF Tower, the city's tallest building, was damaged in an apparent Houthi missile attack.",
        F_BODY(23), DARK, 830, 30,
    )
    draw_wrapped(
        d, 48, y + 4,
        "Saudi Arabia reported renewed Houthi attacks on Thursday.",
        F_BODY(23), DARK, 830, 30,
    )

    # ---- Bottom strip: conflicts ----
    d.rectangle([24, 864, 1000, 956], fill=NAVY)
    d.text((44, 876), "ALSO TODAY", font=F_BODY_B(22), fill=(255, 214, 90))
    y = draw_wrapped(
        d, 44, 906,
        "Gaza: Israel operation in central Gaza  •  Ukraine: Crimea Bridge hit again",
        F_BODY(21), WHITE, 936, 27,
    )
    d.text((44, y + 2), "Iran tensions rise  •  North Korea expands enrichment at Yongbyon, IAEA says",
           font=F_BODY(21), fill=(200, 220, 235))

    # ---- Footer ----
    d.text((24, 972), "19 NOVEMBER 2026  •  WORLD NEWS IN ONE IMAGE",
           font=F_BODY_B(18), fill=GREY)
    foot = "CULTURE: GTA VI LAUNCH"
    fw = d.textlength(foot, font=F_BODY(18))
    d.text((1000 - fw, 972), foot, font=F_BODY(18), fill=GREY)

    return img


def main():
    img = draw()
    # Primary output for the make.fun sandbox
    out_dir = Path("/output")
    try:
        out_dir.mkdir(parents=True, exist_ok=True)
        primary = out_dir / "entry.png"
    except Exception:
        primary = Path(__file__).resolve().parent / "entry.png"
    # Save deterministically: fixed PNG settings, no metadata
    img.save(primary, format="PNG", compress_level=6, optimize=False)
    # Local copy beside this file (same bytes) for preview, when different
    local = Path(__file__).resolve().parent / "entry.png"
    if local.resolve() != primary.resolve():
        img.save(local, format="PNG", compress_level=6, optimize=False)
    print(f"Wrote {primary} ({primary.stat().st_size} bytes)")
    if local.resolve() != primary.resolve():
        print(f"Wrote {local} ({local.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
